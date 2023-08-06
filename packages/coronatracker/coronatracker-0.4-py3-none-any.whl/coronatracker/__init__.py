from collections import namedtuple
from datetime import datetime
import requests
import aiohttp
import json
import re

TotalStats = namedtuple('TotalStats', 'confirmed deaths recovered')
Country = namedtuple('Country', 'total_stats id last_updated areas name lat long')
SubArea = namedtuple('SubArea', 'total_stats id last_updated areas name lat long')  # for US States etc

class CoronaTracker:
    ENDPOINT = 'https://bing.com/covid'
    def __init__(self):
        self.countries = []
        self.total_stats = None

        self._data = {}
        self.__aio_session = None

    def fetch_results(self):
        r = requests.get(self.ENDPOINT)

        self._data = self.get_json(r.text)
        self.countries = self.generate_areas(self._data['areas'])
        self.total_stats = self.generate_stats(self._data)

    async def aio_fetch_results(self):
        if self.__aio_session is None:
            self.__aio_session = aiohttp.ClientSession()

        r = await self.__aio_session.get(self.ENDPOINT)

        self._data = self.get_json(await r.text())
        self.countries = self.generate_areas(self._data['areas'])
        self.total_stats = self.generate_stats(self._data)

    def get_json(self, text):
        s = re.search(r'var data={(.+)};', text).group(0)
        return json.loads(s.replace('var data=', '')[:-1])

    def generate_areas(self, areas, *, cls=Country):
        ret = []

        for area in areas:
            sub_areas = []

            if len(area['areas']) > 0:
                sub_areas = self.generate_areas(area['areas'], cls=SubArea)

            lu = area.get('lastUpdated')
            if lu:
                last_updated = datetime.fromisoformat(area['lastUpdated'][:-1])
            else:
                last_updated = datetime.utcnow()

            ret.append(cls(self.generate_stats(area), area['id'], 
                       last_updated, sub_areas, area['displayName'], area['lat'], area['long']))

        return ret

    def generate_stats(self, area):
        return TotalStats(area['totalConfirmed'], area['totalDeaths'], area['totalRecovered'])

    def get_country(self, name):
        for c in self.countries:
            if c.name == name:
                return c
