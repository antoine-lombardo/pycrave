from abc import ABC
from typing import Dict, List, Any

from .media import Media

class ResultInfo(ABC):
  def __init__(self):
    self.type: str = ''

    self.title: str = ''
    self.description: str = ''
    self.summary: str = ''
    self.image: str = ''

    self.medias: Dict[str, Media] = {}