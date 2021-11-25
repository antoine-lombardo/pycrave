# External stuff
from copy import copy
import json
from fuzzywuzzy import fuzz, process
import logging

# Common
from .common.play_infos import PlayInfos
from .common.result_info import ResultInfo
from .common.serie_result_info import SerieResultInfo
from .common.movie_result_info import MovieResultInfo
from .common.search_result import SearchResult
from .common.account import Account
from .common.platform import Platform

# Crave stuff
from .login_handler import CraveLoginHandler
from .consts import *
from typing import Any, Dict, List, Union

# Internal libs
from .lib.graphql.graphql import GraphQL
from .lib.capi.capi import CAPI

# Logger
logger = logging.getLogger(__name__)


class Crave(Platform):
    name = 'Crave'
    tag = 'crave'
    login_handler: CraveLoginHandler
    account_infos: Account = None

    def __init__(self, cache_dir: str, username: str = None, password: str = None, metadata_lang: str = 'fr'):
        '''
        Initialises the client.
            Args:
                cache_dir (str): Directory to store cache files
                username (str): Account username
                password (str): Account password
                metadata_lang (str): Language used to fetch metadata
        '''
        super().__init__(cache_dir)
        self.graphql = GraphQL(self.session, 'https://www.crave.ca/space-graphql/graphql/', self.tag, metadata_language=metadata_lang)
        self.login_handler = CraveLoginHandler(self.cache_dir, self.session, username, password)
        if self.login_handler.ensure_login():
            self.get_account_infos()
        else:
            logger.info('Unable to login')

    # ===================================================================
    #   SEARCH
    # ===================================================================

    def search(self, input: str)-> List[SearchResult]:
        '''
        Search a title.
            Args:
                input (str): The search terms
            Returns:
                List[SearchResult]: A list of all the search results. First element is the most relevent one.
        '''
        logger.debug('Making a search for "{}"...'.format(input))
        return self.graphql.search(input)

    # ===================================================================
    #   RESULT INFOS
    # ===================================================================

    def get_result_infos(self, result: SearchResult) -> Dict[str, Union[MovieResultInfo, SerieResultInfo]]:
        '''
        Get more infos about a specific search result
            Args:
                result (SearchResult): The search result
            Returns:
                Dict[str, Union[MovieResultInfo, SerieResultInfo]]: A dictionary of all the versions available (french/english) and corresponding infos
        '''
        logger.debug('Getting infos for "{}"...'.format(result.title))
        return self.graphql.get_result_infos(result)

    def get_result_infos_id(self, content_id: str) -> Dict[str, Union[MovieResultInfo, SerieResultInfo]]:
        '''
        Get more infos about a specific search result
            Args:
                id (str): The Content ID
            Returns:
                Dict[str, Union[MovieResultInfo, SerieResultInfo]]: A dictionary of all the versions available (french/english) and corresponding infos
        '''
        logger.debug('Getting infos for "{}"...'.format(content_id))
        return self.graphql.get_result_infos_id(content_id)

    # ===================================================================
    #   PLAY INFOS
    # ===================================================================

    '''
    Get play infos
    '''
    def get_play_infos(self, result_infos: ResultInfo, season: int = None, episode: int = None, language: str = 'fr'):
        if result_infos.type == 'movie':
            return self._get_play_infos_movie(result_infos, language)
        elif result_infos.type == 'serie':
            if season is None or episode is None:
                return None
            else:
                return self._get_play_infos_episode(result_infos, season, episode, language)
        return None

    '''
    Get play infos (movie)
    '''
    def _get_play_infos_movie(self, result_infos: MovieResultInfo, language: str = 'fr') -> PlayInfos:
        destination = result_infos.additionnal_infos['destinations'][language]
        return self._get_play_infos_id(result_infos.play_id, destination, language=language)

    '''
    Get play infos (episode)
    '''
    def _get_play_infos_episode(self, result_infos: SerieResultInfo, season: int, episode: int, language: str = 'fr') -> PlayInfos:
        pass

    '''
    Get play infos (id)
    '''
    def _get_play_infos_id(self, id: str, destination: str, language: str = 'fr') -> PlayInfos:
        if not self.ensure_login():
            return None
        return CAPI.get_play_infos(destination, id, language, token=self.login_handler.access_token, filter='0x14')

    # ===================================================================
    #   ACCOUNT
    # ===================================================================

    def login(self, username: str, password: str) -> bool:
        self.account_infos = None
        if not self.login_handler.login(username, password):
            return False
        if self._get_account_infos() is None:
            return False
        return True

    def logout(self) -> None:
        self.account_infos = None
        self.login_handler.logout()

    def ensure_login(self) -> bool:
        return self.login_handler.ensure_login()

    def get_account_infos(self) -> Account:
        if not self.login_handler.ensure_login():
            self.account_infos = None
            return None
        try:
            self.graphql.subscriptions = self.login_handler.subscriptions
            self.account_infos = Account()
            url = 'https://account.bellmedia.ca/api/profile/v1.1'
            response = self._make_request_bearer(url=url, method='GET')
            response_parsed = json.loads(response.text)
            self.account_infos.name = response_parsed[0]['nickname']
            self.account_infos.picture = response_parsed[0]['avatarUrl']
            return self.account_infos
        except:
            self.account_infos = None
            return None

    # ===================================================================
    #   REQUESTS
    # ===================================================================

    def _make_request_license(self, url: str, token: str, challenge):
        headers = copy(BASE_HEADERS)
        headers['Authorization'] = 'Bearer ' + token
        return self._make_request(url, headers=headers, data=challenge, method='POST-DATA').content

    def _make_request_bearer(self, url: str, data: Dict[str, Any] = {}, method: str = 'POST'):
        if not self.login_handler.ensure_login():
            return None
        headers = copy(BASE_HEADERS)
        headers['Authorization'] = 'Bearer ' + self.login_handler.access_token
        return self._make_request(url, headers=headers, data=data, method=method)

