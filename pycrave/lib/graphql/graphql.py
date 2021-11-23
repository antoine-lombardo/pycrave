from copy import deepcopy
from datetime import datetime
import json
from ...common.serie_result_info import SerieResultInfo
from ...common.movie_result_info import MovieResultInfo
from ...common.search_result import SearchResult

import requests
from .consts import GRAPHQL_SUBS_ID, HEADERS, SEARCH_PAYLOAD, MEDIA_PAYLOAD
from typing import Any, Dict, List, Tuple, Union
from fuzzywuzzy import fuzz


class GraphQL():
  def __init__(self, session: requests.Session, url: str, tag: str, subscriptions: List[str] = []):
    self.session: requests.Session = session
    self.url: str = url
    self.tag: str = tag
    self.subscriptions: List[str] = subscriptions

  def get_graphql_subs(self) -> List[str]:
    graphql_subs = []
    for subscription in self.subscriptions:
      if subscription in GRAPHQL_SUBS_ID:
        graphql_subs.append(GRAPHQL_SUBS_ID[subscription])
    return graphql_subs

  # ===================================================================
  #   SEARCH
  # ===================================================================

  '''
  Searchs results
  '''
  def search(self, input) -> List[Tuple[int, SearchResult]]:
    print('Searching "{}" from provider "{}"...'.format(input, self.tag))
    # request
    print('-> Making GraphQL request...')
    payload = deepcopy(SEARCH_PAYLOAD)
    payload['variables']['searchTerm'] = input
    response = self._make_request(payload)
    if response.status_code != 200:
      print('---> Bad response ({}).'.format(response.status_code))
      return None
    print('-> Parsing response...')
    response_parsed = json.loads(response.text)
    response_parsed = response_parsed['data']['searchMedia']['page']['items']
    # parse results
    suggestions = []
    for item in response_parsed:
      result = SearchResult()
      result.title = item['title']
      if len(item['images']) > 0:
        result.image = item['images'][0]['url']
      req_ids = item['resourceCodes']
      result.requirements = []
      for req_id in req_ids:
        if req_id in GRAPHQL_SUBS_ID:
          result.requirements.append(GRAPHQL_SUBS_ID[req_id])
      result.platform_tag = self.tag
      result.search_title = result.title
      result.id = item['id']
      suggestions.append((fuzz.partial_ratio(result.title, input), result))
    print('-> Found {} matches!'.format(str(len(suggestions))))
    return suggestions

  # ===================================================================
  #   RESULT INFOS
  # ===================================================================

  '''
  Get detailed result infos
  '''
  def get_result_infos(self, result: SearchResult) -> List[Union[MovieResultInfo, SerieResultInfo]]:
    print('Getting infos for "{}" ({})...'.format(result.id, self.tag))
    # request
    payload = deepcopy(MEDIA_PAYLOAD)
    payload['variables']['id'] = result.id
    responses = {}
    print('-> Making GraphQL request (french)...')
    responses['fr'] = self._make_request(payload, playback_language='FRENCH')
    print('-> Making GraphQL request (english)...')
    responses['en'] = self._make_request(payload, playback_language='ENGLISH')
    if responses['fr'].status_code != 200 and responses['en'].status_code != 200:
      print('---> Bad responses.')
      return None
    infos = {}
    for lang, response in responses.items():
      try:
        if response.status_code != 200:
          print('-> Skipping {} response...'.format(lang))
          continue
        print('-> Parsing {} response...'.format(lang))
        response_parsed = json.loads(response.text)['data']['axisMedia']
        if response_parsed['mediaType'] == 'SERIES':
          infos[lang] = self._parse_serie_result(response_parsed)
        elif response_parsed['mediaType'] == 'MOVIE':
          infos[lang] = self._parse_movie_result(response_parsed)
      except:
        print('---> Unable to parse {} response...'.format(lang))
        continue
    print('-> Found {} versions!'.format(str(len(infos))))
    infos_formatted = []
    for version, info in infos.items():
      if version not in info.playback_languages:
        continue
      info.version = version
      infos_formatted.append(info)
    return infos_formatted


  '''
  Parse movie result infos
  '''
  def _parse_movie_result(self, result: Dict[str, Any]) -> MovieResultInfo:
    infos = MovieResultInfo()
    content = result['mainContents']['page']['items'][0]
    # Title
    infos.title = result['title']
    # Image
    for image in result['images']:
      if image['format'] == 'POSTER':
        infos.image = image['url']
        break
    infos.title = result['title']
    # Summary
    infos.summary = result['summary']
    # Description
    infos.description = result['description']
    # Playback Languages / Destinations
    infos.additionnal_infos['destinations'] = {}
    for lang in content['axisPlaybackLanguages']:
      infos.playback_languages.append(lang['language'].lower())
      infos.additionnal_infos['destinations'][lang['language'].lower()] = lang['destinationCode']
    # Play ID
    infos.play_id = str(content['axisId'])
    # Year
    try:
      date_str = content['broadcastDate']
      date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
      infos.year = date.year
    except:
      pass
    # Duration
    try:
      duration_str = content['duration']
      duration = 0
      if 'h' in duration_str:
        index = duration_str.index('h')
        value = duration_str[:index]
        duration_str = duration_str[index+1:]
        duration += int(value.strip()) * 3600
      if 'm' in duration_str:
        index = duration_str.index('m')
        value = duration_str[:index]
        duration_str = duration_str[index+1:]
        duration += int(value.strip()) * 60
      if 's' in duration_str:
        index = duration_str.index('s')
        value = duration_str[:index]
        duration_str = duration_str[index+1:]
        duration += int(value.strip())
      infos.duration = duration
    except:
      pass
    return infos


  '''
  Parse serie result infos
  '''
  def _parse_serie_result(self, result: Dict[str, Any]) -> SerieResultInfo:
      pass

  def _make_request(self, partial_data: Dict[str, Any], language: str = 'ENGLISH', playback_language: str = 'FRENCH') -> requests.Response:
    data = deepcopy(partial_data)
    data['variables']['subscriptions'] = self.get_graphql_subs()
    data['variables']['language'] = language
    data['variables']['playbackLanguage'] = playback_language
    return self.session.post(url=self.url, headers=HEADERS, json=data)
