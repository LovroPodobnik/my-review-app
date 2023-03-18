from app_store_scraper import AppStore
from pprint import pprint

minecraft = AppStore(country="us", app_name="minecraft", app_id=479516143)
minecraft.review(how_many=100)

pprint(minecraft.reviews)
pprint(minecraft.reviews_count)