import requests, xmltodict, os, json, subprocess, binascii, base64

PSSH_URN = 'urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed'
WV_SYSTEM_ID = '[ed ef 8b a9 79 d6 4a ce a3 c8 27 dc d5 1d 21 ed]'
MP4DUMP_EXE = 'binaries/mp4dump.exe'

class PlayInfos():
  def __init__(self, manifest_url, subtitles_url: str, manifest_response, license_token = None, license_url = None, pssh = None, headers = None):
    print('-> Initializing play infos...')
    self.manifest_url: str = manifest_url
    self.subtitles_url: str = subtitles_url
    self.license_url: str = license_url
    self.license_token: str = license_token
    self.manifest_response: requests.Response = manifest_response
    self.pssh: str = pssh
    self.headers = headers

    if self.license_url is None:
      print('---> No license url provided, trying to find it...')
      self._extract_license_url()

    if self.pssh is None:
      print('---> No pssh provided, trying to find it...')
      self._extract_pssh()

  def _extract_license_url(self) -> str:
    pass

  def get_base_url(self) -> str:
    print('-> Extracting base url...')
    try:
      print('---> Searching in manifest...')
      manifest = xmltodict.parse(self.manifest_response.text)
      base_url = manifest['MPD']['BaseURL']
      if base_url is not None:
        print('-----> Found: {}'.format(base_url))
        return base_url
      print('-----> Not found.')
    except:
      print('-----> Not found.')
    print('---> Unable to find base url.')
    return None


  def _extract_pssh(self) -> str:
    # From manifest method
    try:
      print('-----> Searching in manifest...')
      manifest = xmltodict.parse(self.manifest_response.text)
      wv_data = [x for x in manifest['MPD']['Period']['AdaptationSet'][0]['ContentProtection'] if
                                x['@schemeIdUri'] == PSSH_URN]
      if wv_data is None:
        return None
      self.pssh = wv_data[0]['cenc:pssh']
      print('-------> Found: {}'.format(self.pssh))
      return self.pssh
    except:
      print('-------> Not found.')
    # From init file method
    try:
      print('-----> Searching in init segment...')
      manifest = xmltodict.parse(self.manifest_response.text)
      base_url = manifest['MPD']['BaseURL']
      init_path = manifest['MPD']['Period']['AdaptationSet'][0]['SegmentTemplate']['@initialization']
      representation_id = manifest['MPD']['Period']['AdaptationSet'][0]['Representation'][0]['@id']
      init_url = base_url + init_path
      init_url = init_url.replace('$RepresentationID$', representation_id)
      if self.headers is None:
        response = requests.get(init_url)
      else:
        response = requests.get(init_url, headers=self.headers)
      if response.status_code != 200:
        raise
      tmp_path = os.path.abspath('tmp')
      if not os.path.isdir(tmp_path):
        os.makedirs(tmp_path)
      file_path = os.path.join(tmp_path, 'init.mp4')
      if os.path.isfile(file_path):
        os.remove(file_path)
      with open(file_path, "wb") as file:
        file.write(response.content)
      try:
        self.pssh = self._extract_pssh_file(file_path)
        os.remove(file_path)
        if self.pssh is not None:
          print('-------> Found: {}'.format(self.pssh))
          return self.pssh
      except:
        if os.path.isfile(file_path):
          os.remove(file_path)
    except:
      print('-------> Not found.')
    print('-----> Unable to find pssh.')

  @staticmethod
  def _extract_pssh_file(file_path: str) -> str:
    file_path = os.path.abspath(file_path)
    mp4dump_path = os.path.abspath(MP4DUMP_EXE)
    pssh = None
    data = subprocess.check_output([mp4dump_path, '--format', 'json', '--verbosity', '1', file_path])
    data = json.loads(data)
    for atom in data:
        if atom['name'] == 'moov':
            for child in atom['children']:
                if child['name'] == 'pssh' and child['system_id'] == WV_SYSTEM_ID:
                    pssh = child['data'][1:-1].replace(' ', '')
                    pssh = binascii.unhexlify(pssh)
                    # if pssh.startswith('\x08\x01'):
                    #   pssh = pssh[0:]
                    pssh = pssh[0:]
                    pssh = base64.b64encode(pssh).decode('utf-8')
                    return pssh
