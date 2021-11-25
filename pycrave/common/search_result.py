from typing import List


class SearchResult():

  def __init__(self, dict = None):
    self.requirements: List[str] = []
    self.title: str = ''
    self.search_title: str = ''
    self.type: str = ''
    self.description: str = ''
    self.id: str = ''
    self.image: str = ''
    self.platform_tag: str = ''
    self.version: str = None
    if dict is not None:
      self.__dict__.update(dict)

  def to_dict(self):
    return {
      "requirements": self.requirements,
      "title": self.title,
      "search_title": self.search_title,
      "type": self.type,
      "description": self.description,
      "id": self.id,
      "image": self.image,
      "platform_tag": self.platform_tag
    }

  def __lt__(self, other):
    if self.search_title != '':
      if(self.search_title<other.search_title):
        return True
      else:
        return False
    else:
      if(self.title<other.title):
        return True
      else:
        return False
