from abc import ABC, abstractmethod
from .result_info import ResultInfo
from .serie_result_info import SerieResultInfo
from .movie_result_info import MovieResultInfo
from .account import Account
from .search_result import SearchResult
from .play_infos import PlayInfos
from typing import Any, Dict, List, Tuple, Union
import requests
import os
import pickle

class Platform(ABC):
  name: str
  tag: str
  session: requests.Session

  def __init__(self, cache_dir: str) -> None:
    self.cache_dir = os.path.join(cache_dir, self.tag)
    if not os.path.isdir(self.cache_dir):
      os.makedirs(self.cache_dir)
    self._load_session()

  # ===================================================================
  #   ACCOUNT
  # ===================================================================

  @abstractmethod
  def login(username: str, password: str) -> bool:
    pass

  @abstractmethod
  def logout() -> None:
    pass

  @abstractmethod
  def ensure_login() -> None:
    pass

  @abstractmethod
  def get_account_infos() -> Account:
    pass

  # ===================================================================
  #   SEARCH
  # ===================================================================

  @abstractmethod
  def search(self, input: str) -> List[Tuple[int, SearchResult]]:
    pass

  # ===================================================================
  #   RESULT INFOS
  # ===================================================================

  @abstractmethod
  def get_result_infos(self, result: SearchResult) -> List[Union[MovieResultInfo, SerieResultInfo]]:
    pass

  # ===================================================================
  #   PLAY_INFOS
  # ===================================================================

  @abstractmethod
  def get_play_infos(self, result_infos: ResultInfo, season: int = None, episode: int = None, language: str = 'fr') -> PlayInfos:
    pass


  # ===================================================================
  #   SESSION
  # ===================================================================

  def _load_session(self) -> None:
    self.session = requests.Session()
    session_file = os.path.join(self.cache_dir, 'session.pck')
    if os.path.isfile(session_file):
      try:
        with open(session_file, 'rb') as file:
          self.session.cookies.update(pickle.load(file))
      except:
        os.remove(session_file)
        self.session.cookies.clear()
    self._save_session()

  def _save_session(self) -> None:
    session_file = os.path.join(self.cache_dir, 'session.pck')
    if os.path.isfile(session_file):
      os.remove(session_file)
    with open(session_file, 'wb') as file:
      pickle.dump(self.session.cookies, file)


  # ===================================================================
  #   REQUESTS
  # ===================================================================

  def _make_request(self, url: str, data: Dict[str, Any] = {}, headers: Dict[str, str] = {}, method: str = 'POST'):
    if method == 'POST':
      response = self.session.post(url=url, json=data, headers=headers)
    elif method == 'POST-DATA':
      response = self.session.post(url=url, data=data, headers=headers)
    else:
      response = self.session.get(url=url, headers=headers)
    self._save_session()
    return response