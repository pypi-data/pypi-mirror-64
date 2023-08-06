from collections import namedtuple
from platform import architecture, sys
from pathlib import Path
import os
import json
import asyncio
from datetime import datetime

from seleniumwire import webdriver

TotalStats = namedtuple('TotalStats', 'confirmed deaths recovered')
Country = namedtuple('Country', 'total_stats id last_updated areas name lat long')
SubArea = namedtuple('SubArea', 'total_stats id last_updated areas name lat long')  # for US States etc

class CoronaTracker:
    ENDPOINT = 'https://bing.com/covid'
    def __init__(self):
        self.executable = self.get_bin()

        options = webdriver.FirefoxOptions()
        options.headless = True

        self.driver = webdriver.Firefox(executable_path=self.executable, options=options)

        self.countries = []
        self.total_stats = None

        self._data = {}

    def get_bin(self):
        _bin = Path(__file__).parent.joinpath('bin')
        if sys.platform.startswith('win32'):
            bit = architecture()[0]
            if bit == '32bit':
                exe = _bin.joinpath('geckodriver_32.exe') # 32-bit v0.26.0
            else:
                exe = _bin.joinpath('geckodriver_64.exe')
        elif sys.platform.startswith('linux'):
            exe = _bin.joinpath('linux.geckodriver') # 32-bit v0.26.0
            os.system(f'chmod +x {_bin}')
        elif sys.platform.startswith('darwin'):
            exe = _bin.joinpath('darwin.geckodriver') # OS X v0.26.0
            os.system(f'chmod +x {_bin}')
        else:
            raise FileNotFoundError('Could not find pre-installed geckodriver for {sys.platform}')

        return exe

    def fetch_results(self):
        self.driver.get('https://bing.com/covid')
        request = self.driver.wait_for_request('/data', timeout=20)

        self._data = self.get_json(request.response.body.decode(encoding='utf-8'))
        self.countries = self.generate_areas(self._data['areas'])
        self.total_stats = self.generate_stats(self._data)

    def __old_fetch_results(self):
        r = requests.get(self.ENDPOINT)

        self._data = self.get_json(r.text)
        self.countries = self.generate_areas(self._data['areas'])
        self.total_stats = self.generate_stats(self._data)

    async def aio_fetch_results(self):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.fetch_results)
        return

    async def __old_aio_fetch_results(self):
        if self.__aio_session is None:
            self.__aio_session = aiohttp.ClientSession()

        r = await self.__aio_session.get(self.ENDPOINT)

        self._data = self.get_json(await r.text())
        self.countries = self.generate_areas(self._data['areas'])
        self.total_stats = self.generate_stats(self._data)

    def get_json(self, text):
        return json.loads(text)

    def __old_get_json(self, text):
        #s = re.search(r'var data={(.+)};', text).group(0)
        #return json.loads(s.replace('var data=', '')[:-1])
        ...

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
