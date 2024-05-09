import os
import random
from utils import File, Log
from gig import Ent

log = Log('ReadMe')


class ReadMe:
    @property
    def image_info_list(self):
        image_info_list = []
        for file_name in os.listdir(os.path.join('data', 'images')):
            gnd_id, qlatlng, ext = file_name.split('.')
            if ext != 'png':
                continue
            file_path = os.path.join('data', 'images', file_name)
            file_path_unix = file_path.replace('\\', '/')
            gnd = Ent.from_id(gnd_id)
            dsd_id = gnd.dsd_id
            dsd = Ent.from_id(dsd_id)
            district_id = dsd.district_id
            district = Ent.from_id(district_id)
            province_id = district.province_id
            province = Ent.from_id(province_id)

            image_info_list.append(
                dict(
                    gnd_id=gnd_id,
                    gnd=gnd,
                    dsd=dsd,
                    district=district,
                    province=province,
                    qlatlng=qlatlng,
                    file_name=file_name,
                    file_path=file_path,
                    file_path_unix=file_path_unix,
                )
            )
        return image_info_list

    @property
    def lines_images(self):
        image_info_list = self.image_info_list
        random.shuffle(image_info_list)
        lines = []
        for image_info in image_info_list:
            gnd = image_info['gnd']
            dsd = image_info['dsd']
            district = image_info['district']
            province = image_info['province']

            gnd_id = image_info['gnd_id']
            file_path_unix = image_info['file_path_unix']
            lines.extend(
                [
                    '<div id="image-info">',
                    '',
                    f'## {gnd.name} GND',
                    '',
                    f'{dsd.name} DSD, {district.name} District, {province.name} Province',
                    '',
                    f'![{gnd_id}]({file_path_unix})',
                    '',
                    '</div>',
                    '',
                ]
            )
        return lines

    @property
    def lines(self):
        return [
            '# Random Sri Lanka',
            '',
            '*A collection of random Google Street Views.*',
            '',
        ] + self.lines_images

    def build(self):
        readme_path = 'README.md'
        File(readme_path).write_lines(self.lines)
        log.info(f'Wrote {readme_path}')
