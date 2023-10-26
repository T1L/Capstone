import urllib.request
import re
from lxml import etree
from public_py import save_csv
from public_py import fullyIntegrated
from data_process import all_data_process
from data_augmentation import data_Augmentation
import numpy as np
from joblib import load
class entrance:
    def __init__(self):
        self.all_url_list = [
            {
                "self": True,
                "url": 'https://www.cleanenergyregulator.gov.au/NGER/National%20greenhouse%20and%20energy%20reporting'
                       '%20data/electricity-sector-emissions-and-generation-data/electricity-sector-emissions-and'
                       '-generation-data-2021%E2%80%9322 '
            },
            {
                "self": False,
                "url": 'https://www.cleanenergyregulator.gov.au/NGER/National%20greenhouse%20and%20energy%20reporting'
                       '%20data/electricity-sector-emissions-and-generation-data/electricity-sector-emissions-and'
                       '-generation-data-2020-21 '
            },
            {
                "self": False,
                "url": 'https://www.cleanenergyregulator.gov.au/NGER/National%20greenhouse%20and%20energy%20reporting'
                       '%20data/electricity-sector-emissions-and-generation-data/electricity-sector-emissions-and'
                       '-generation-data-2019-20 '
            },
            {
                "self": False,
                "url": 'https://www.cleanenergyregulator.gov.au/NGER/National%20greenhouse%20and%20energy%20reporting'
                       '%20data/electricity-sector-emissions-and-generation-data/electricity-sector-emissions-and'
                       '-generation-data-2018-19 '
            },
            {
                "self": False,
                "url": 'https://www.cleanenergyregulator.gov.au/NGER/Pages/Published%20information/Electricity'
                       '%20sector%20emissions%20and%20generation%20data/Electricity-sector-emissions-and-generation'
                       '-data-2017%E2%80%9318-.aspx '
            },
            {
                "self": False,
                "url": 'https://www.cleanenergyregulator.gov.au/NGER/National%20greenhouse%20and%20energy%20reporting'
                       '%20data/electricity-sector-emissions-and-generation-data/electricity-sector-emissions-and'
                       '-generation-data-2016-17 '
            },
            {
                "self": False,
                "url": 'https://www.cleanenergyregulator.gov.au/NGER/National%20greenhouse%20and%20energy%20reporting'
                       '%20data/electricity-sector-emissions-and-generation-data/electricity-sector-emissions-and'
                       '-generation-data-2015-16 '
            },
            {
                "self": False,
                "url": 'https://www.cleanenergyregulator.gov.au/NGER/National%20greenhouse%20and%20energy%20reporting'
                       '%20data/electricity-sector-emissions-and-generation-data/electricity-sector-emissions-and'
                       '-generation-data-2014-15 '
            },
            {
                "self": False,
                "url": 'https://www.cleanenergyregulator.gov.au/NGER/National%20greenhouse%20and%20energy%20reporting'
                       '%20data/electricity-sector-emissions-and-generation-data/electricity-sector-emissions-and'
                       '-generation-data-2013-14 '
            },
            {
                "self": False,
                "url": 'https://www.cleanenergyregulator.gov.au/NGER/National%20greenhouse%20and%20energy%20reporting'
                       '%20data/electricity-sector-emissions-and-generation-data/electricity-sector-emissions-and'
                       '-generation-data-2012-13 '
            }
        ]
        self.char = 'wind farm'
        self.download_url = 'https://www.cleanenergyregulator.gov.au/DocumentAssets/Pages/Greenhouse-and-energy' \
                            '-information-by-designated-generation-facility-%s.aspx '
        self.public_download = [
            {
                "link": 'https://www.cleanenergyregulator.gov.au/DocumentAssets/Pages/Greenhouse-and-energy-information-by-designated-generation-facility-%s.aspx',
                "re": r'/DocumentAssets/Pages/Greenhouse-and-energy-information-by-designated-generation-facility-(.*?).aspx'
            },
            {
                "link": 'https://www.cleanenergyregulator.gov.au/DocumentAssets/Pages/Greenhouse-and-energy-information-for-designated-generation-facilities-%s.aspx',
                "re": r'/DocumentAssets/Pages/Greenhouse-and-energy-information-for-designated-generation-facilities-(.*?).aspx'
            },
            {
                "link": 'https://www.cleanenergyregulator.gov.au/DocumentAssets/Pages/%s-Greenhouse-and-energy-information-for-designated-generation-facilities.aspx',
                "re": r'/DocumentAssets/Pages/(.*?)-Greenhouse-and-energy-information-for-designated-generation-facilities.aspx'
            }
        ]

    def get_download_url(self, saveName=None, prefix=None):
        if saveName:
            new_url = prefix % saveName[0]
            download_res = urllib.request.urlopen(new_url)
            download_content = download_res.read().decode('utf-8')
            html = etree.HTML(download_content)
            #
            download_url = html.xpath('//a[@class="docAssetItem"]')
            for download_item in download_url:
                types = download_item.xpath('./span[@class="type"]/text()')
                csv_url = download_item.xpath('./@href')
                if len(types) and types[0].lower() == 'csv':
                    save_csv(csv_file=saveName[0], url=csv_url[0])
                    break

    def run(self):
        for item in self.all_url_list:
            response = urllib.request.urlopen(item['url'])
            content = response.read().decode('utf-8')
            switch_off = True
            for down in self.public_download:
                saveName = re.findall(down['re'], content, re.S)
                if len(saveName):
                    self.get_download_url(saveName=saveName, prefix=down['link'])
                    switch_off = False
                    break
            if switch_off:
                print('获取文件地址失败！')

        pass


loaded_model = load('trained_model.joblib')


if __name__ == '__main__':
    #
    string = input('Enter 1 to update the data,2 Integrate data,3 to process data,4 to train the model,5 to estimate：')
    if string == '1':
        entrance().run()
    if string == '2':
        fullyIntegrated()
    if string == '3':
        all_data_process()
        data_Augmentation()
    if string == '4':
        with open("model.py", "r") as f:
            code = f.read()
            exec(code)
    if string == '5':
        with open("Tools.py", "r") as f:
            code = f.read()
            exec(code)

