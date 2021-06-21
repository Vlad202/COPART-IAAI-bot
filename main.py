from posix import EX_CANTCREAT
import requests
import time
from lxml import html
from bs4 import BeautifulSoup
from telebot import TeleBot
import threading
from secrets import TELEGRAM_TOKEN
import os
import datetime
import shutil
import json
from fake_useragent import UserAgent
import re


payload = {}
# ua = UserAgent()
app = TeleBot(TELEGRAM_TOKEN)
URLS = {
    'copart': {
        'url': 'https://www.copart.com/public/lots/search',
        'data': [
            {
                "filter[YEAR]": 'lot_year:"2014",lot_year:"2015",lot_year:"2016",lot_year:"2017",lot_year:"2018",lot_year:"2019"',
                "filter[MAKE]": 'lot_make_desc:"VOLKSWAGEN"',
                "filter[NLTS]": 'expected_sale_assigned_ts_utc:[NOW/DAY-7DAY TO NOW/DAY]'
            },
            {
                "filter[YEAR]": 'lot_year:"2019",lot_year:"2018",lot_year:"2017",lot_year:"2016",lot_year:"2015",lot_year:"2014"',
                "filter[MAKE]": 'lot_make_desc:"FORD"',
                "filter[BODY]": 'body_style:"4DR SPOR",body_style:"CONVERTI",body_style:"COUPE",body_style:"HATCHBAC",body_style:"SEDAN 4D"',
                "filter[NLTS]": 'expected_sale_assigned_ts_utc:[NOW/DAY-7DAY TO NOW/DAY]'
            },
            {
                "filter[YEAR]": 'lot_year:"2019",lot_year:"2018",lot_year:"2017",lot_year:"2016",lot_year:"2015",lot_year:"2014"',
                "filter[MAKE]": 'lot_make_desc:"NISSAN"',
                "filter[BODY]": 'body_style:"4DR SPOR",body_style:"COUPE",body_style:"CONVERTI",body_style:"HATCHBAC",body_style:"SEDAN 4D"',
                "filter[NLTS]": 'expected_sale_assigned_ts_utc:[NOW/DAY-7DAY TO NOW/DAY]'
            },
            {
                "filter[YEAR]": 'lot_year:"2022",lot_year:"2021",lot_year:"2020",lot_year:"2019",lot_year:"2018",lot_year:"2017",lot_year:"2016",lot_year:"2015"',
                "filter[FUEL]": 'fuel_type_desc:"DIESEL"',
                "filter[BODY]": 'body_style:"4DR SPOR",body_style:"HATCHBAC",body_style:"SEDAN 4D"',
                "filter[NLTS]": 'expected_sale_assigned_ts_utc:[NOW/DAY-7DAY TO NOW/DAY]'
            },
            {
                "filter[YEAR]": 'lot_year:"2016",lot_year:"2017",lot_year:"2018",lot_year:"2019",lot_year:"2020",lot_year:"2021"',
                "filter[FUEL]": 'fuel_type_desc:"ELECTRIC"',
                "filter[NLTS]": 'expected_sale_assigned_ts_utc:[NOW/DAY-7DAY TO NOW/DAY]'
            }
        ],
        'keys': {
            'keys': ['ld', 'ad', 'yn', 'hb', 'ln', 'fv', 'syn', 'orr', 'lcd', 'scn', 'dd', 'sdd', 'la', 'bstl', 'vehTypDesc', 'clr', 'rc', 'egn', 'cy', 'trf', 'drv', 'ft', 'hk', 'vehTypDesc', 'scl'],
            'values': ['', 'Дата продажи', 'Место продажи', 'Текущая ставка', '№ лота', 'Номер VIN', 'Тип документа', 'Одометр', 'Основные моменты', 'Продавец', 'Основное повреждение', 'Вторичное повреждение', 'Оценочная розничная стоимость', 'Оценка ремонта', 'Тип кузова', 'Цилиндры', 'Передача', 'Привод', 'Топливо', 'Ключи', 'Классификация ТС', 'Примечания']
        }
    },
    'aiia': [
        'https://www.iaai.com/search?url=SILrjGptBGTiqPA8XndoyjlJr0DRZKvqCu%2fkh6A4qCE%3d',
        'https://www.iaai.com/search?url=anAxnyLSnoFBJgK9xBb363EKHRmsn9G1o%2fwxtvDGMFQ%3d',
        'https://www.iaai.com/search?url=rEyIKvCOUAlxQC%2bqCltnBjXIbgJuD4bQ79YsqZN9%2b6w%3d',
        'https://www.iaai.com/search?url=DgV5nMhW%2fe7JSWPv6G8Xs3qFhbs2LgrDSExswj4B568%3d',
        'https://www.iaai.com/search?url=JxarIrGtsOG0v54B6JV7HO%2f5q6JWfIG1j%2f5PAqDHGoQ%3d'
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
    'cookie': '',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}
try:
    ua.update()
    ua['google chrome']
    headers['User-Agent'] = ua['google chrome']
except:
    pass
data_cars = {
    '0': '',
    '1': '',
    '2': '',
    '3': '',
    '4': ''
}
data_aiia = {
    '0': 'Auction Not Assigned',
    '1': 'Auction Not Assigned',
    '2': 'Auction Not Assigned',
    '3': 'Auction Not Assigned',
    '4': 'Auction Not Assigned'
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
    image = requests.get(i['url'], data=payload).content
    with open(f'./{car_id}/'+str(car_id)+' --- '+str(image_id)+'.jpg', 'wb') as f:
        f.write(image)
        
def coport_parser(s, copart_next_post):
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
    car_id = f"copart - {copart_next_post['ld']}".replace('/', ' - ')
    try:
        os.mkdir(car_id)
    except:
        try:
            shutil.rmtree(f'{car_id}/')
            os.mkdir(car_id)
        except:
            pass
    with open(f'./{car_id}/'+car_id+'.txt', 'w') as f:
        f.write(text)

    exception_flag = True
    try:
        url = 'https://www.copart.com/public/data/lotdetails/solr/lotImages/'+str(copart_next_post['ln'])+''
        images_response = s.get(url).content
        images_list = json.loads(images_response)['data']['imagesList']['FULL_IMAGE']
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
    print(post_url)
    exception_flag = True
    try:
        post_response = requests.get('https://iaai.com'+post_url, data=payload)
    except Exception as e:
        exception_flag = False
        print(e)
        print('Exception in aiia post request')
    if exception_flag:
        tree = html.fromstring(post_response.content)
        post_soup = BeautifulSoup(post_response.text, 'html')
        text = 'https://iaai.com'+post_url+'\n' + post_soup.find('h1', {'class': 'heading-2 heading-2-semi mb-0 rtl-disabled'}).text.strip().replace('/', ' ')+ '\n\n'
        post_lists = BeautifulSoup(post_response.text, 'html').find_all('li', {'class': 'data-list__item'})
        text_arr = []
        for li in post_lists:
            line = " ".join(str(li.text.strip()).split())
            if line not in text_arr:
                text += line + '\n'
                text_arr.append(line)
        # text = "\n".join(text.split())
#         text = f'''
# {'https://iaai.com'+post_url}\n\n
# {check_aiia_arr(tree.xpath('/html/body/section/main/section[2]/div/div/h1/text()'))}\n
# Current Bid: {check_aiia_arr(tree.xpath('/html/body/section/main/section[3]/div/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/ul/li/span[2]/text()'))}\n
# Stock #: {check_aiia_arr(tree.xpath('/html/body/section/main/section[3]/div/div[2]/div/div[1]/div[1]/div[2]/ul/li[1]/span[2]/strong/text()'))}\n
# Selling Branch: {check_aiia_arr(tree.xpath('/html/body/section/main/section[3]/div/div[2]/div/div[1]/div[1]/div[2]/ul/li[2]/span[2]/text()'))}\n
# VIN (Status): {check_aiia_arr(tree.xpath('//*[@id="VIN_VehInfo"]/text()'))}\n
# Loss: {check_aiia_arr(tree.xpath('/html/body/section/main/section[3]/div/div[2]/div/div[1]/div[1]/div[2]/ul/li[4]/span[2]/text()'))}\n
# Primary Damage: {check_aiia_arr(tree.xpath('//*[@id="walkThruspan"]/text()'))}\n
# Secondary Damage: {check_aiia_arr(tree.xpath('/html/body/section/main/section[3]/div/div[2]/div/div[1]/div[1]/div[2]/ul/li[6]/span[2]/text()'))}\n
# Title/Sale Doc: {check_aiia_arr(tree.xpath('/html/body/section/main/section[3]/div/div[2]/div/div[1]/div[1]/div[2]/ul/li[7]/span[2]/text()'))}\n
# Start Code: {check_aiia_arr(tree.xpath('//*[@id="startcodeengine_image"]/text()'))}\n
# Odometer: {check_aiia_arr(tree.xpath('/html/body/section/main/section[3]/div/div[2]/div/div[1]/div[1]/div[2]/ul/li[10]/span[2]/text()'))}\n
# Airbags: {check_aiia_arr(tree.xpath('/html/body/section/main/section[3]/div/div[2]/div/div[1]/div[1]/div[2]/ul/li[11]/span[2]/text()'))}\n
# Vehicle: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[2]/span[2]/text()'))}\n
# Body Style: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[3]/span[2]/text()'))}\n
# Engine: {check_aiia_arr(tree.xpath('//*[@id="ingine_image"]/text()'))}\n
# Transmission: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[5]/span[2]/text()'))}\n
# Drive Line Type: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[6]/span[2]/text()'))}\n
# Fuel Type: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[7]/span[2]/text()'))}\n
# Cylinders: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[8]/span[2]/text()'))}\n
# Restraint System: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[9]/span[2]/text()'))}\n
# Exterior/Interior: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[10]/span[2]/text()'))}\n
# Options: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[11]/span[2]/text()'))}\n
# Manufactured In: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[12]/span[2]/text()'))}\n
# Vehicle Class: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[13]/span[2]/text()'))}\n
# Model: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[11]/span[2]/text()'))}\n
# Series: {check_aiia_arr(tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[12]/span[2]/text()'))}\n
#         '''
        car_soup = BeautifulSoup(post_response.text, 'html')
        # print(car_id)
        try:
            car_id = f"aiia - {car_soup.find('h1', {'class': 'heading-2 heading-2-semi mb-0 rtl-disabled'}).text.strip().replace('/', ' ')}"
        except:
            car_id = f'aiia - {datetime.datetime.now().strftime("%m-%d-%Y %H-%M-%S")}'
        try:
            os.mkdir(car_id)
        except:
            shutil.rmtree(f'{car_id}/')
            os.mkdir(car_id)
        with open(f'./{car_id}/'+car_id+'.txt', 'w') as f:
            f.write(text)
        try: 
            images_cid = re.findall(r'var thumbnailKey = "(.+?)";', post_response.text)[0]
        except:
            images_cid = car_soup.find_all('img', {'class': 'img-responsive lazyload'})[0].attrs['data-src']
            images_cid = re.findall(r'imageKeys=(.+?)~', images_cid)[0] + '~SID'
        images_json = json.loads(requests.get('https://anvis.iaai.com/dimensions?imageKeys='+images_cid, data=payload).text)
        i = 0
        for image in images_json['keys']:
            image_url = 'https://anvis.iaai.com/resizer?imageKeys='+str(image['K'])+'&width=845&height=633'
            i += 1
            download_image(car_id, {'url': image_url}, i)
        shutil.make_archive(car_id, 'zip', car_id)
        shutil.rmtree(f'{car_id}/')
        send_zip(car_id)
        os.remove(car_id+'.zip')
        
def copart_thread():
    print('### START COPART ###')
    while True:
        s = requests.Session()
        s.headers.update(headers)
        # copart
        try:
            request_cookie_update = s.get('https://www.copart.com/ru/lotSearchResults/?free=true&query=&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22FUEL%22:%5B%22fuel_type_desc:%5C%22ELECTRIC%5C%22%22%5D,%22YEAR%22:%5B%22lot_year:%5C%222016%5C%22%22,%22lot_year:%5C%222017%5C%22%22,%22lot_year:%5C%222018%5C%22%22,%22lot_year:%5C%222019%5C%22%22,%22lot_year:%5C%222020%5C%22%22,%22lot_year:%5C%222021%5C%22%22%5D%7D,%22sort%22:%5B%22auction_date_type%20desc%22,%22auction_date_utc%20asc%22%5D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D')
            headers['cookie'] = request_cookie_update.request.headers['Cookie']
        except Exception as e:
            print(e)
            print('Exception in cookie request')
            continue
        copart_data = URLS['copart']['data']
        for cars_filter in range(len(copart_data)):
            with open('./copart_flags/copart_flag'+str(cars_filter)+'.txt', 'r') as f:
                checkout_url = f.read()
            try:
                response_copart = json.loads(s.post(URLS['copart']['url'], headers=headers, data=copart_data[cars_filter]).text)['data']['results']['content']
            # print(s.post(URLS['copart']['url'], headers=headers, data=copart_data[cars_filter]).text)
            except Exception as e:
                print(e)
                print(f'Exception in copart global requests, iteration {cars_filter+1}')
                continue
            # time.sleep(30)
            copart_flag = True
            print(response_copart)
            response_copart = list(reversed(response_copart))
            for post in range(len(response_copart)):
                print(response_copart[post]['ln'])
                if str(response_copart[post]['ln']) == str(checkout_url):
                    copart_flag = False
                    try:
                        posts_list = response_copart[post+1:]
                    except:
                        posts_list = []
                    for final_post in posts_list:
                        with open('./copart_flags/copart_flag'+str(cars_filter)+'.txt', 'w') as f:
                            f.write(str(response_copart[post]['ln']))
                        coport_parser(s, final_post)
                        time.sleep(10)
                    break
            if copart_flag:
                response_copart = list(reversed(response_copart))
                with open('./copart_flags/copart_flag'+str(cars_filter)+'.txt', 'w') as f:
                    f.write(str(response_copart[0]['ln']))
                coport_parser(s, response_copart[0])

            # copart_next_post = response_copart[0]
            # if data_cars[str(cars_filter)] != copart_next_post['ln']:
            #     coport_parser(s, copart_next_post)
            #     data_cars[str(cars_filter)] = copart_next_post['ln']
            time.sleep(200)
        print('checkout ------- copart ------- ' + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
        time.sleep(350)

def aiia_thread():
    headers = {
        'Cookie': 'IAAITrackingCookie=62c9879f-0635-49cb-a4d8-9c4a742397ba; ASP.NET_SessionId=y5fn0edtzmj4weh3cbk1g3tt; Locations_Cookie=Locations_Cookie=MapView; ASLBSA=752283e7583a4afe9fc575e5d6e4609eaf721f80b006245f19f03fcbdc3f34a8; ASLBSACORS=752283e7583a4afe9fc575e5d6e4609eaf721f80b006245f19f03fcbdc3f34a8'
    }
    print('### START AIIA ###')
    while True:
        # aiia
        cars_counter = 0
        for url in range(len(URLS['aiia'])):
            cars_counter += 1
            try:
                response_aiia = requests.get(URLS['aiia'][url]).text
            except Exception as e:
                print(e)
                print(f'Exception in aiia global requests, iteration {cars_counter}')
                continue
            soup_aiia = BeautifulSoup(response_aiia, 'html')
            try:
                # post_url = soup_aiia.find_all('h4', {'class': 'heading-7 rtl-disabled'}).find('a').attrs['href']
                post_flags = soup_aiia.find_all('div', {'class': 'table-row table-row-border'})
            except Exception as e:
                print(e)
                print(f'Exception in aiia post_url')
                continue
            with open('./iaai_flags/aiia_flag'+str(url)+'.txt', 'r') as f:
                checkout_url = f.read()
            post_flags = list(reversed(post_flags))
            copart_flag = True
            for j in range(len(post_flags)):
                # post_auction = post_flags[j].find('span', {'class': 'data-list__value data-list__value--action'}).text.strip()
                post_url = post_flags[j].find('h4', {'class': 'heading-7 rtl-disabled'}).find('a').attrs['href']
                if checkout_url == post_url:
                    data_aiia[str(url)] = post_url
                    copart_flag = False
                    try:
                        res_posts_list = post_flags[j+1:]
                    except:
                        res_posts_list = []
                    for res_post in res_posts_list:
                        res_post_url = res_post.find('h4', {'class': 'heading-7 rtl-disabled'}).find('a').attrs['href']
                        post_auction = res_post.find('span', {'class': 'data-list__value data-list__value--action'}).text.strip()
                        if post_auction != 'Auction Not Assigned':
                            with open('./iaai_flags/aiia_flag'+str(url)+'.txt', 'w') as f:
                                f.write(res_post_url)
                            parse_aiia(res_post_url)
                    break
            if copart_flag:
                post_flags = list(reversed(post_flags))
                with open('./iaai_flags/aiia_flag'+str(url)+'.txt', 'w') as f:
                    f.write(post_flags[0].find('h4', {'class': 'heading-7 rtl-disabled'}).find('a').attrs['href'])
                parse_aiia(post_flags[0].find('h4', {'class': 'heading-7 rtl-disabled'}).find('a').attrs['href'])
                        
        print('checkout ------- aiia ------- ' + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
        time.sleep(300)

if __name__ == '__main__':
	thr_bot = threading.Thread(target=bot_thread)
	thr_bot.start()
	thr_copart = threading.Thread(target=copart_thread)
	thr_copart.start()
	thr_aiia = threading.Thread(target=aiia_thread)
	thr_aiia.start()