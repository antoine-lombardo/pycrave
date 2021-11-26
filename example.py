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

categories = crave.get_root_categories()
serie_category = crave.get_elements(categories[0])
drames_category = crave.get_elements(serie_category[0])
collection_category = crave.get_elements(categories[4])

search_result = crave.search("your honor")
serie_infos = crave.get_result_infos(search_result[0])

search_result = crave.search("justice league")
movie_infos = crave.get_result_infos(search_result[0])
account = crave.get_account_infos()

play_infos_serie = crave.get_play_infos(serie_infos['fr'], season = 1, episode = 1)
logger.info('Manifest: {}'.format(play_infos_serie.manifest_url))
logger.info('License URL: {}'.format(play_infos_serie.license_url))
play_infos_serie = crave.get_play_infos(serie_infos['en'], season = 1, episode = 1)
logger.info('Manifest: {}'.format(play_infos_serie.manifest_url))
logger.info('License URL: {}'.format(play_infos_serie.license_url))

play_infos_movie = crave.get_play_infos(movie_infos['fr'])
logger.info('Manifest: {}'.format(play_infos_movie.manifest_url))
logger.info('License URL: {}'.format(play_infos_movie.license_url))