from abc import ABC
from typing import Dict, List, Any

class Category(ABC):
  def __init__(self, type = '', title = '', image = '', id = ''):
    self.obj_type = 'category'
    self.type: str = type
    self.title: str = title
    self.image: str = image
    self.id: str = id