from config import *
from pycrave import Crave

crave = Crave(cache_dir, username, password)
search_result = crave.search("justice league")
movie_infos = crave.get_result_infos(search_result[0])
account = crave.get_account_infos()
print("ss")