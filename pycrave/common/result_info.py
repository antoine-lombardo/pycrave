from abc import ABC, abstractmethod
from typing import Dict, List, Any

class ResultInfo(ABC):
  def __init__(self):
    self.version: str = ''
    self.type: str = ''
    self.image: str = ''
    self.title: str = ''
    self.description: str = ''
    self.summary: str = ''
    self.play_id: Dict[str, str] = {}
    self.playback_languages: List[str] = []
    self.additionnal_infos: Dict[str, Any] = {}