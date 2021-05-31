from posix import EX_CANTCREAT
import requests
import time
from lxml import html
from requests.api import post
from bs4 import BeautifulSoup
from telebot import TeleBot
import threading
import datetime
from secrets import TELEGRAM_TOKEN
import os
import datetime
import shutil
import json
from fake_useragent import UserAgent
import re


ua = UserAgent()
s = requests.Session()
app = TeleBot(TELEGRAM_TOKEN)
URLS = {
    'copart': {
        'url': 'https://www.copart.com/public/lots/search',
        'data': [
            {
                "filter[YEAR]": 'lot_year:"2014",lot_year:"2015",lot_year:"2016",lot_year:"2017",lot_year:"2018",lot_year:"2019"',
                "filter[MAKE]": 'lot_make_desc:"VOLKSWAGEN"'
            },
            {
                "filter[YEAR]": 'lot_year:"2019",lot_year:"2018",lot_year:"2017",lot_year:"2016",lot_year:"2015",lot_year:"2014"',
                "filter[MAKE]": 'lot_make_desc:"FORD"',
                "filter[BODY]": 'body_style:"4DR SPOR",body_style:"CONVERTI",body_style:"COUPE",body_style:"HATCHBAC",body_style:"SEDAN 4D"'
            },
            {
                "filter[YEAR]": 'lot_year:"2019",lot_year:"2018",lot_year:"2017",lot_year:"2016",lot_year:"2015",lot_year:"2014"',
                "filter[MAKE]": 'lot_make_desc:"NISSAN"',
                "filter[BODY]": 'body_style:"4DR SPOR",body_style:"COUPE",body_style:"CONVERTI",body_style:"HATCHBAC",body_style:"SEDAN 4D"'
            },
            {
                "filter[YEAR]": 'lot_year:"2022",lot_year:"2021",lot_year:"2020",lot_year:"2019",lot_year:"2018",lot_year:"2017",lot_year:"2016",lot_year:"2015"',
                "filter[FUEL]": 'fuel_type_desc:"DIESEL"',
                "filter[BODY]": 'body_style:"4DR SPOR",body_style:"HATCHBAC",body_style:"SEDAN 4D"'
            },
            {
                "filter[YEAR]": 'lot_year:"2016",lot_year:"2017",lot_year:"2018",lot_year:"2019",lot_year:"2020",lot_year:"2021"',
                "filter[FUEL]": 'fuel_type_desc:"ELECTRIC"',
            }
        ],
        'keys': {
            'keys': ['ld', 'ad', 'yn', 'hb', 'ln', 'fv', 'syn', 'orr', 'lcd', 'scn', 'dd', 'sdd', 'la', 'bstl', 'vehTypDesc', 'clr', 'rc', 'egn', 'cy', 'trf', 'drv', 'ft', 'hk', 'vehTypDesc', 'scl'],
            'values': ['', 'Дата продажи', 'Место продажи', 'Текущая ставка', '№ лота', 'Номер VIN', 'Тип документа', 'Одометр', 'Основные моменты', 'Продавец', 'Основное повреждение', 'Вторичное повреждение', 'Оценочная розничная стоимость', 'Оценка ремонта', 'Тип кузова', 'Цилиндры', 'Передача', 'Привод', 'Топливо', 'Ключи', 'Классификация ТС', 'Примечания']
        }
    },
    'aiia': [
        'https://www.iaai.com/search?url=ZAxKBe2Dn%2f94uvs6933wng66g7MYLRd0HSImvkO9Lo0%3d',
        'https://www.iaai.com/search?url=oXyVh%2bj3Putf7PgNJXnZQiuD8XByquNIu4jS0esuLII%3d',
        'https://www.iaai.com/search?url=giVS22%2fpaKOQuOjNMPoCyl4Go5FT4uc78x1rM859PDI%3d',
        'https://www.iaai.com/search?url=768l%2fsx06Ck4clqVAaCt0VXkoKjQj%2fNhqbiXY1X9qXM%3d',
        'https://www.iaai.com/search?url=VZIXldQudR8cmBtGj0vlR6eLI2evDFY3ntnhYTci2tA%3d'
    ] 
}
headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "ru-UA,ru;q=0.9,uk-UA;q=0.8,uk;q=0.7,ru-RU;q=0.6,en-US;q=0.5,en;q=0.4",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
    "x-xsrf-token": "065a6c42-97be-4521-bf90-99d55b97760d",
    'cookie': ''
}
data_cars = {
    '1': '',
    '2': '',
    '3': '',
    '4': '',
    '5': ''
}
data_aiia = {
    '1': '',
    '2': '',
    '3': '',
    '4': '',
    '5': ''
}

@app.message_handler(commands=['start'])
def example_command(message):
	geted_id = message.chat.id
	with open('telegram.txt', 'r', encoding='utf-8') as f:
		ids_list = f.read().split(',')
		ids = ids_list
	if str(geted_id) not in ids:
		ids.append(str(geted_id))
		# print(message)
		with open('telegram.txt', 'a') as f:
			f.write(f'{str(geted_id)},')
	msg = '''
	Здравствуйте!\nТеперь вам будут присылаться новые объявления из сайтов: \n\ncopart.com\n\n
	Чтоб отказатья от подписки, введите /stop
	'''
	app.send_message(geted_id, msg)

@app.message_handler(commands=['stop'])
def example_command(message):
	geted_id = message.chat.id
	with open('telegram.txt', 'r', encoding='utf-8') as f:
		ids_list = f.read().split(',')
	msg = '''
		ID пользователя не найдено, кажется что Вы ещё не подписаны на рассылку.Подписаться - /start
	'''
	if str(geted_id) in ids_list:
		ids_list.remove(str(geted_id))
		updated_ids_list = ','.join(str(x) for x in ids_list)
		with open('telegram.txt', 'w') as f:
			f.write(updated_ids_list)
		msg = '''
			Вам больше не будут рприходить сообщения от меня.\nЧто бы получать уведомления снова, введите команду /start
		'''
	app.send_message(geted_id, msg)

def send_zip(zip_name):
	with open('telegram.txt', 'r') as f:
		ids_list = f.read().split(',')
		for chat_id in ids_list:
			try:
				app.send_document(chat_id, open(zip_name+'.zip','rb'))
			except:
				pass    

def bot_thread():
	print('### START TELEGRAM ###')
	app.polling()

def download_image(car_id, i, image_id):
    time.sleep(2)
    image = requests.get(i['url']).content
    with open(f'./{car_id}/'+str(car_id)+' --- '+str(image_id)+'.jpg', 'wb') as f:
        f.write(image)
        
def coport_parser(copart_next_post):
    ua.update()
    ua['google chrome']
    headers['User-Agent'] = ua['google chrome']
    s.headers.update(headers)
    text = f'https://www.copart.com/lot/{str(copart_next_post["ln"])}/\n\n'
    for key in range(len(URLS['copart']['keys']['keys'])):
        try:  
            value = str(copart_next_post[URLS['copart']['keys']['keys'][key]]) 
            if URLS['copart']['keys']['keys'][key] == 'ad':
                datetime.datetime.fromtimestamp(copart_next_post[URLS['copart']['keys']['keys'][key]])
            text += URLS['copart']['keys']['values'][key] + ': ' + value + '\n'
        except:
            pass
    try:
        text += f"Статус продажи: {copart_next_post['dynamicLotDetails']['saleStatus']}\n"
    except:
        pass
    car_id = f"copart - {copart_next_post['ld']}"
    try:
        os.mkdir(car_id)
    except:
        shutil.rmtree(f'{car_id}/')
        os.mkdir(car_id)
    with open(f'./{car_id}/'+car_id+'.txt', 'w') as f:
        f.write(text)

    exception_flag = True
    time.sleep(5)
    try:
        images_list = json.loads(s.get('https://www.copart.com/public/data/lotdetails/solr/lotImages/'+str(copart_next_post['ln'])+'').text)['data']['imagesList']['FULL_IMAGE']
    except Exception as e:
        exception_flag = False
        print(e)
        print('Exception in copart images_list request')
    if exception_flag:
        image_id = 0
        for i in images_list:
            image_id += 1
            download_image(car_id, i, image_id)
    shutil.make_archive(car_id, 'zip', car_id)
    shutil.rmtree(f'{car_id}/')
    send_zip(car_id)
    os.remove(car_id+'.zip')

def check_aiia_arr(arr):
    if type(arr) == type([]) and len(arr) > 0:
        return " ".join(str(arr[0]).split())
    else:
        return arr


def parse_aiia(post_url):
    exception_flag = True
    try:
        post_response = requests.get('https://iaai.com'+post_url)
    except Exception as e:
        exception_flag = False
        print(e)
        print('Exception in aiia post request')
    if exception_flag:
        tree = html.fromstring(post_response.content)
        text = f'''
{'https://iaai.com'+post_url}\n\n
{check_aiia_arr(tree.xpath('/html/body/section/main/section[2]/div/div/h1/text()'))}\n
Current Bid: {check_aiia_arr(tree.xpath('/html/body/section/main/section[3]/div/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/ul/li/span[2]/text()'))}\n
Stock #: {check_aiia_arr(tree.xpath('/html/body/section/main/section[3]/div/div[2]/div/div[1]/div[1]/div[2]/ul/li[1]/span[2]/strong/text()'))}\n
Selling Branch: {check_aiia_arr(tree.xpath('/html/body/section/main/section[3]/div/div[2]/div/div[1]/div[1]/div[2]/ul/li[2]/span[2]/text()'))}\n
VIN (Status): {check_aiia_arr(tree.xpath('//*[@id="VIN_VehInfo"]/text()'))}\n
Loss: {check_aiia_arr(tree.xpath('/html/body/section/main/section[3]/div/div[2]/div/div[1]/div[1]/div[2]/ul/li[4]/span[2]/text()'))}\n
Primary Damage: {check_aiia_arr(tree.xpath('//*[@id="walkThruspan"]/text()'))}\n
Secondary Damage: {check_aiia_arr(tree.xpath('/html/body/section/main/section[3]/div/div[2]/div/div[1]/div[1]/div[2]/ul/li[6]/span[2]/text()'))}\n
Title/Sale Doc: {check_aiia_arr(tree.xpath('/html/body/section/main/section[3]/div/div[2]/div/div[1]/div[1]/div[2]/ul/li[7]/span[2]/text()'))}\n
Start Code: {check_aiia_arr(tree.xpath('//*[@id="startcodeengine_image"]/text()'))}\n
Odometer: {check_aiia_arr(tree.xpath('/html/body/section/main/section[3]/div/div[2]/div/div[1]/div[1]/div[2]/ul/li[10]/span[2]/text()'))}\n
Airbags: {check_aiia_arr(tree.xpath('/html/body/section/main/section[3]/div/div[2]/div/div[1]/div[1]/div[2]/ul/li[11]/span[2]/text()'))}\n
Vehicle: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[2]/span[2]/text()'))}\n
Body Style: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[3]/span[2]/text()'))}\n
Engine: {check_aiia_arr(tree.xpath('//*[@id="ingine_image"]/text()'))}\n
Transmission: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[5]/span[2]/text()'))}\n
Drive Line Type: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[6]/span[2]/text()'))}\n
Fuel Type: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[7]/span[2]/text()'))}\n
Cylinders: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[8]/span[2]/text()'))}\n
Restraint System: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[9]/span[2]/text()'))}\n
Exterior/Interior: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[10]/span[2]/text()'))}\n
Options: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[11]/span[2]/text()'))}\n
Manufactured In: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[12]/span[2]/text()'))}\n
Vehicle Class: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[13]/span[2]/text()'))}\n
Model: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[14]/span[2]/text()'))}\n
Series: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[15]/span[2]/text()'))}\n
        '''
        car_id = f"aiia - {tree.xpath('/html/body/section/main/section[2]/div/div/h1/text()')[0]}"
        try:
            os.mkdir(car_id)
        except:
            shutil.rmtree(f'{car_id}/')
            os.mkdir(car_id)
        with open(f'./{car_id}/'+car_id+'.txt', 'w') as f:
            f.write(text)

        images_cid = re.findall(r'var thumbnailKey = "(.+?)";', post_response.text)[0]
        images_json = json.loads(requests.get('https://anvis.iaai.com/dimensions?imageKeys='+images_cid).text)
        i = 0
        for image in images_json['keys']:
            image_url = 'https://anvis.iaai.com/resizer?imageKeys='+str(image['K'])+'&width=845&height=633'
            i += 1
            download_image(car_id, {'url': image_url}, i)
        shutil.make_archive(car_id, 'zip', car_id)
        shutil.rmtree(f'{car_id}/')
        send_zip(car_id)
        os.remove(car_id+'.zip')
        
def parser_thread():
    print('### START PARSER ###')
    while True:
        # copart
        # try:
        #     ua.update()
        #     ua['google chrome']
        #     headers['User-Agent'] = ua['google chrome']
        #     s.headers.update(headers)
        #     request_cookie_update = s.get('https://www.copart.com/ru/lotSearchResults/?free=true&query=&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22FUEL%22:%5B%22fuel_type_desc:%5C%22ELECTRIC%5C%22%22%5D,%22YEAR%22:%5B%22lot_year:%5C%222016%5C%22%22,%22lot_year:%5C%222017%5C%22%22,%22lot_year:%5C%222018%5C%22%22,%22lot_year:%5C%222019%5C%22%22,%22lot_year:%5C%222020%5C%22%22,%22lot_year:%5C%222021%5C%22%22%5D%7D,%22sort%22:%5B%22auction_date_type%20desc%22,%22auction_date_utc%20asc%22%5D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D')
        #     headers['cookie'] = request_cookie_update.request.headers['Cookie']
        # except Exception as e:
        #     print(e)
        #     print('Exception in cookie request')
        #     continue
        # copart_data = URLS['copart']['data']
        # for cars_filter in range(len(copart_data)):
        #     try:
        #         response_copart = json.loads(s.post(URLS['copart']['url'], data=copart_data[cars_filter]).text)['data']['results']['content']
        #     except Exception as e:
        #         print(e)
        #         print(f'Exception in copart global requests, iteration {cars_filter+1}')
        #         continue
        #     copart_next_post = response_copart[0]
        #     if data_cars[str(cars_filter+1)] != copart_next_post['ln']:
        #         coport_parser(copart_next_post)
        #         data_cars[str(cars_filter+1)] = copart_next_post['ln']
        #     time.sleep(30)
        # print('checkout ------- copart ------- ' + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
        # aiia
        cars_counter = 0
        for url in range(len(URLS['aiia'])):
            cars_counter += 1
            try:
                response_aiia = requests.get(URLS['aiia'][url]).text
            except Exception as e:
                print(e)
                print(f'Exception in copart global requests, iteration {cars_counter}')
                continue
            soup_aiia = BeautifulSoup(response_aiia, 'html')
            post_url = soup_aiia.find_all('h4', {'class': 'heading-7 rtl-disabled'})[0].find('a').attrs['href']
            if data_aiia[str(url+1)] != post_url:
                parse_aiia(post_url)
                data_aiia[str(url+1)] = post_url
        print('checkout ------- aiia ------- ' + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
        time.sleep(250)

if __name__ == '__main__':
	thr_bot = threading.Thread(target=bot_thread)
	thr_bot.start()
	thr_parser = threading.Thread(target=parser_thread)
	thr_parser.start()