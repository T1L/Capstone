import os, requests, re
from lxml import etree
import csv
import spacy

nlp = spacy.load("en_core_web_sm")


def extract_entities(text):
    doc = nlp(text)
    entities = []
    for entity in doc.ents:
        if entity.label_ == 'QUANTITY' or entity.label_ == 'CARDINAL':  # 选择QUANTITY和CARDINAL标签的实体
            entities.append(entity.text)
    return entities


def makedir(path):
    # 不存在创建文件夹
    if not os.path.exists(path):
        # 创建文件夹
        os.makedirs(path)


prefix = './csv'
makedir(path=prefix)
makedir(path='./new_csv')


def save_csv(csv_file=None, url=None):
    if csv_file and url:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        flieName = prefix + '/' + csv_file + '.csv'
        with open(flieName, "wb") as file:
            file.write(response.content)


def analysis(flieName=None):
    if flieName:
        # 读取 CSV 文件
        data = csv_to_dict(flieName)
        # 将数据保存为列表
        new_filename = flieName.split('/')[-1]

        for item in data:
            if item['Facility Name'].lower().find('wind farm') > -1:
                Facility_Name = item['Facility Name']
                date = new_filename.split('.')[0]
                year = date.split('-')[0]
                print(Facility_Name)
                walls = summary_Details(query=Facility_Name)
                numbers = walls['numbers']
                divideBy_self = False
                if walls['PowerPerunit'].lower().find('kw') != -1:
                    divideBy_self = True
                PowerPerunit = extract_entities(walls['PowerPerunit'])
                if len(PowerPerunit):
                    if divideBy_self:
                        PowerPerunit = get_counts(entities=PowerPerunit[0], bool=True) / 1000
                    else:
                        PowerPerunit = get_counts(entities=PowerPerunit[0], bool=False)
                else:
                    PowerPerunit = ''
                Capacity = extract_entities(walls['Capacity'])
                if len(Capacity):
                    Capacity = get_counts(entities=Capacity[0], bool=False)
                else:
                    Capacity = ''
                item['year'] = year
                item['numbers'] = numbers
                item['Power Per unit'] = PowerPerunit
                item['Capacity'] = Capacity
                dict_to_csv([item], './new_csv/output.csv')
                # writer.writerow(new_row)


def summary_Details(query=None):
    # 设置header信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': 'WMF-Last-Access=29-Jun-2023; WMF-Last-Access-Global=29-Jun-2023; GeoIP=JP:13:Tokyo:35.69:139.69:v4; enwikimwuser-sessionId=1a04d68d7e632b337f55; enwikiBlockID=9050896%219f9c06fa5cb602d5ddeba6832a9133235da1e9880e656aa493a61a56d674ac929bd89c858b7372a1f44a295a07fb9f05b2fb92c0eb91cad046cdc4c18d31e909; WMF-DP=761; NetworkProbeLimit=0.001; enwikiwmE-sessionTickLastTickTime=1688044888207; enwikiwmE-sessionTickTickCount=12'
    }
    url = 'https://en.wikipedia.org/wiki/' + query.replace(' ', '_')
    obj = {'text': '', 'PowerPerunit': '', 'Capacity': '', 'numbers': ''}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html = etree.HTML(response.text)
        quantities = html.xpath('//*[@id="mw-content-text"]//text()')
        if len(quantities):
            obj['text'] = ''.join(quantities)
            table_tr = html.xpath('//*[@id="mw-content-text"]//table[@class="infobox vcard"]//tr')
            for tr in table_tr:
                string = tr.xpath('./th//text()')
                if len(string):
                    if ''.join(string).lower().find('capacity') != -1 and ''.join(string).lower().find('eplate') != -1:
                        text = tr.xpath('./td//text()')
                        obj['Capacity'] = ''.join(text)
                    if ''.join(string).lower().find('units') != -1 and ''.join(string).lower().find('operation') != -1:
                        text = tr.xpath('./td//text()')
                        if len(text):
                            new_text = ''.join(text).replace(' ', '')
                            # X x x
                            if new_text.find('x') != -1:
                                s = new_text.split('x')
                            elif new_text.find('X') != -1:
                                s = new_text.split('X')
                            else:
                                s = new_text.split('×')
                            try:
                                obj['PowerPerunit'] = s[-1]
                                obj['numbers'] = s[0]
                            except IndexError:
                                obj['PowerPerunit'] = text
                                obj['numbers'] = text

    return obj


def get_counts(entities='entities', bool=True):
    counts = 0
    pattern = r'\d+\.?\d*|\.\d+'  # 匹配带小数的数字部分
    result = re.findall(pattern, entities)
    if len(result) > 0:
        if bool:
            counts = float(result[0])
        else:
            counts = result[0]

    return counts


def csv_to_dict(file_path):
    data_dict = []
    column_names = [
        'year',
        'Reporting Entity',
        'Facility Name',
        'State',
        'Electricity production (GJ)',
        'Electricity Production (Mwh)',
        'scope 1',
        'scope 2',
        'Total emissions (t CO2-e)',
        'numbers',
        'Power Per unit',
        'Capacity'
    ]
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # 处理表头，去除空格并设置为大写字母
                header_dict = {}
                for item in column_names:
                    values = ''
                    for key, value in row.items():
                        if key.replace(" ", "").replace("\n", "").replace("\r", "").upper().find(item.replace(" ", "").upper()) != -1:
                            header_dict[item] = value
                            break
                    else:
                        header_dict[item] = values
                data_dict.append(header_dict)
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # 处理表头，去除空格并设置为大写字母
                header_dict = {}
                for item in column_names:
                    values = ''
                    for key, value in row.items():
                        if key.replace(" ", "").replace("\n", "").replace("\r", "").upper().find(item.replace(" ", "").upper()) != -1:
                            header_dict[item] = value
                            break
                    else:
                        header_dict[item] = values
                data_dict.append(header_dict)

    return data_dict


def dict_to_csv(data_dict, file_path='./new_csv/output.csv'):
    fieldnames = data_dict[0].keys()
    if os.path.exists(file_path):
        try:
            with open('./new_csv/output.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames)
                writer.writerows(data_dict)
        except UnicodeDecodeError:
            with open('./new_csv/output.csv', 'a', newline='', encoding='latin-1') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames)
                writer.writerows(data_dict)
    else:
        with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames)
            writer.writeheader()
            writer.writerows(data_dict)


import glob


def fullyIntegrated():
    folder_path = './csv'
    csv_files = glob.glob(f'{folder_path}/*.csv')
    # 打印所有CSV文件路径
    for file in csv_files:
        analysis(file.replace('\\', '/'))


# if __name__ == '__main__':
#     fullyIntegrated()
