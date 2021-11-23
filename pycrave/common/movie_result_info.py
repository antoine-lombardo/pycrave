from .result_info import ResultInfo


from .result_info import ResultInfo


class MovieResultInfo(ResultInfo):
  def __init__(self):
    super().__init__()
    self.type = 'movie'
    self.year: int = 0
    self.duration: int = 0