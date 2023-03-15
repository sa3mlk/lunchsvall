import json
import urllib3
from datetime import date

class MatochmatClient:
    def __init__(self):
        self.base_url = 'https://www.matochmat.se/rest/v2'
        self.http = urllib3.PoolManager()

    def __get_json(self, endpoint, args=None):
        query = f'{self.base_url}/{endpoint}'
        if args:
            query += f"?{'&'.join([f'{k}={v}' for k, v in args.items()])}"
        response = self.http.request('GET', query)
        return json.loads(response.data)['data']

    def get_cities(self):
        return self.__get_json('cities')

    def get_restaurants(self, city_id):
        return self.__get_json('restaurants', {'city': city_id})

    def get_menus(self, city_id):
        return self.__get_json('menus', {'city': city_id})

def get_daily_specials(day=None):
    client = MatochmatClient()
    cities = client.get_cities()

    sundsvall = next(city for city in cities if city['name'] == 'Sundsvall')

    restaurant_by_id = {}
    for r in client.get_restaurants(sundsvall['id']):
        restaurant_by_id[r.get('id')] = r

    day = date.today().weekday() if day is None else day
    day = ['mandag', 'tisdag', 'onsdag', 'torsdag', 'fredag', 'lordag', 'sondag'][day]

    def generate_specials(day: str):
        menus = client.get_menus(sundsvall['id'])
        for menu in menus:
            restaurant = restaurant_by_id.get(menu['restaurantId'])
            specials = []
            for daily in json.loads(menu['content'])[day]:
                specials.append(f"{daily['name']} {daily['description']}")

            if 'Dagens rätt kommer snart ' in specials:
                continue

            geo = restaurant['geodata']
            yield {
                'name': restaurant['name'],
                'streetaddress': restaurant['address'],
                'dataurl': restaurant['website'],
                'specials': specials,
                'mapurl': f"https://www.hitta.se/kartan!~{geo['latitude']},{geo['longitude']},{geo['zoomLevel'] if geo['zoomLevel'] > 0 else 14}z"
            }

    return list(generate_specials(day))

if __name__ == '__main__':
	import test
	test.run(get_daily_specials)
