import os
import random
import tempfile
import time

from gig import Ent, EntType
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import Log

log = Log('RandomLKMap')

TEST_MODE = os.name == 'nt'


class RandomLKMap:
    T_CAPTURE_SLEEP = 5
    MIN_FILE_SIZE = 100 * 1024

    @staticmethod
    def get_random_gnd():
        gnds = Ent.list_from_type(EntType.GND)
        return random.choice(gnds)

    @staticmethod
    def get_random_offset():
        Q = 0.001
        return [random.random() * Q, random.random() * Q]

    def __init__(self):
        self.gnd = RandomLKMap.get_random_gnd()
        self.dlatlng = RandomLKMap.get_random_offset()

    @property
    def latlng(self):
        lat0, lng0 = self.gnd.centroid
        dlat, dlng = self.dlatlng
        lat, lng = lat0 + dlat, lng0 + dlng
        return lat, lng

    @property
    def url(self):
        lat, lng = self.latlng
        return (
            'https://www.google.com/maps'
            + '/@?api=1'
            + '&map_action=pano'
            + f'&viewpoint={lat:.6f},{lng:.6f}'
        )

    @property
    def image_path(self):
        gnd_id = self.gnd.id
        lat, lng = self.latlng
        qlat, qlng = [int(x * 1000000) for x in [lat, lng]]
        return os.path.join('data', 'images', f'{gnd_id}.{qlat}-{qlng}.png')

    @staticmethod
    def capture_screenshot(url):
        log.debug(f'Opening {url}...')
        image_path = tempfile.mktemp(suffix='.png')
        options = Options()
        options.add_argument('--headless')
        options.window_size = (1920, 1080)

        driver = webdriver.Firefox(options=options)

        driver.get(url)
        time.sleep(RandomLKMap.T_CAPTURE_SLEEP)
        driver.save_screenshot(image_path)

        driver.quit()

        log.info(f'Wrote {image_path}')
        return image_path

    def capture_image(self):
        if os.path.exists(self.image_path):
            return self.image_path

        temp_image_path = RandomLKMap.capture_screenshot(
            self.url,
        )
        file_size = os.path.getsize(temp_image_path)
        log.debug(f'File size: {file_size:,}')
        if file_size < RandomLKMap.MIN_FILE_SIZE:
            log.warn('File size too small.')
            return None

        os.rename(temp_image_path, self.image_path)
        log.info(f'Copied image to {self.image_path}')
        if TEST_MODE:
            os.startfile(self.image_path)
        return self.image_path

    @staticmethod
    def gen():
        while True:
            map = RandomLKMap()
            if map.capture_image():
                return map
