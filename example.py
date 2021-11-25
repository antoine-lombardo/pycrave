import logging
from config import *
from pycrave import Crave

logging.basicConfig(
  format='%(asctime)s [%(levelname)s] [%(module)s] %(message)s',
  datefmt='%Y-%m-%d,%H:%M:%S')
logging.getLogger().setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)


crave = Crave(
  cache_dir = cache_dir,
  username  = username,
  password  = password,
  metadata_lang = 'en'
  )



search_result = crave.search("madame lebrun")
serie_infos = crave.get_result_infos(search_result[0])

search_result = crave.search("justice league")
movie_infos = crave.get_result_infos(search_result[0])
account = crave.get_account_infos()
print("ss")