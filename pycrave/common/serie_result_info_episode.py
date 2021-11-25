from typing import Any, Dict
from .result_info import ResultInfo


class SerieResultInfoEpisode(ResultInfo):
  def __init__(self):
    super().__init__()
    self.type = 'episode'
    self.seasons: Dict[int, Dict[int, Any]] = {}