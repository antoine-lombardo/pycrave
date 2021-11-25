from abc import ABC
from typing import Dict, List, Any

class Media(ABC):
  def __init__(self):
    self.type: str = 'media'

    self.title: str = ''
    self.description: str = ''
    self.summary: str = ''
    self.image: str = ''
    self.has_access: bool = True

    self.duration: int = 0
    self.playback_languages: List[str] = []

    self.play_id: Dict[str, str] = {}
    self.additionnal_infos: Dict[str, Any] = {}

class MediaMovie(Media):
  def __init__(self):
    super().__init__()


class MediaEpisode(Media):
  def __init__(self):
    super().__init__()
    self.season: str = None
    self.episode: str = None
    self.episode_tag: str = None