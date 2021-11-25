from typing import Any, Dict

from pycrave.common.serie_result_info_episode import SerieResultInfoEpisode
from .result_info import ResultInfo


class SerieResultInfo(ResultInfo):
  def __init__(self):
    super().__init__()
    self.type = 'serie'