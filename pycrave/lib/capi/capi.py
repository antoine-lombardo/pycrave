import json
from ...common.play_infos import PlayInfos
import requests


PLATFORM = 'android'
HOST = 'capi.9c9media.com'
LICENSE_URL = 'https://license.9c9media.ca/widevine'
HEADERS = {
  'accept-encoding': 'identity',
  'connection': 'Keep-Alive',
  'user-agent': 'okhttp/4.9.0',
}

class CAPI():
  @staticmethod
  def get_play_infos(destination: str, content_id: str, language: str, token: str = None, filter: str = None) -> PlayInfos:
    # get package id
    print('-> Making CAPI request...')
    url = CAPI.get_content_url(destination, content_id)
    url += '?$lang={}&$include=[Images,Authentication,AdTarget,Season,ContentPackages,Media,Owner,Omniture,Tags,ChannelAffiliate]'.format(language)
    response = requests.get(url=url, headers=HEADERS)
    if response.status_code != 200:
        print('---> Bad response ().'.format(str(response.status_code)))
        return None
    package_id = str(json.loads(response.text)['ContentPackages'][0]['Id'])
    print('---> Found package ID: {}'.format(package_id))
    # suffixes
    manifest_url_suffix = []
    license_url_suffix = []
    if token is not None:
      manifest_url_suffix.append('jwt={}'.format(token))
      license_url_suffix.append('jwt={}'.format(token))
    if filter is not None:
      manifest_url_suffix.append('filter={}'.format(filter))
    # format urls
    package_url = CAPI.get_package_bond_url(destination, content_id, package_id)
    subtitles_url = package_url + '/manifest.vtt'
    manifest_url = package_url + '/manifest.mpd'
    license_url = 'https://license.9c9media.ca/widevine'
    # add suffixes
    if len(manifest_url_suffix) > 0:
      subtitles_url += '?{}'.format('&'.join(manifest_url_suffix))
      manifest_url += '?{}'.format('&'.join(manifest_url_suffix))
    if len(license_url_suffix) > 0:
      license_url += '?{}'.format('&'.join(license_url_suffix))
    # making manifest request
    print('-> Making manifest request...')
    manifest_response = requests.get(url=manifest_url, headers=HEADERS)
    if manifest_response.status_code != 200:
      if manifest_response.status_code == 403:
        print('---> Cannot load manifest, too many concurrent connections.')
      else:
        print('---> Cannot load manifest.')
      return None
    return PlayInfos(
        manifest_url=manifest_url,
        manifest_response=manifest_response,
        subtitles_url=subtitles_url,
        license_token=token,
        license_url=license_url,
        headers=HEADERS
    )

  @staticmethod
  def get_base_url(destination: str) -> str:
    return 'https://{}/destinations/{}/platforms/{}'.format(HOST, destination, PLATFORM)

  @staticmethod
  def get_content_url(destination: str, content_id: str) -> str:
    return CAPI.get_base_url(destination) + '/contents/{}'.format(content_id)

  @staticmethod
  def get_content_bond_url(destination: str, content_id: str) -> str:
    return CAPI.get_base_url(destination) + '/bond/contents/{}'.format(content_id)

  @staticmethod
  def get_package_url(destination: str, content_id: str, package_id: str) -> str:
    return CAPI.get_content_url(destination, content_id) + '/contentPackages/{}'.format(package_id)

  @staticmethod
  def get_package_bond_url(destination: str, content_id: str, package_id: str) -> str:
    return CAPI.get_content_bond_url(destination, content_id) + '/contentPackages/{}'.format(package_id)