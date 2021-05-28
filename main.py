from posix import EX_CANTCREAT
import requests
import time
from bs4 import BeautifulSoup
from telebot import TeleBot
import threading
import datetime
from secrets import TELEGRAM_TOKEN
import os
import datetime
import shutil
import json


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
    # "x-xsrf-token": "b3da8034-eff4-4a59-ae77-8d652ce33bce",
    "cookie": "visid_incap_242093=6wyLApMZT6+UO0s5f4c1DT1OrmAAAAAAQUIPAAAAAACsDgSB3YI4M3nRD48AOp1c; s_fid=139DB19ECBB69742-193E7AEAD73FE34C; g2usersessionid=c5b2569f1ff735589559c3b0f42c764e; G2JSESSIONID=5BDEF1C85A74184206BCBEE4BABFB1D0-n1; userLang=ru; incap_ses_686_242093=l5rkOmJBRSDaCXsBxCmFCX8NsWAAAAAARc7yToUTYM8yK1nWxbUFqw==; copartTimezonePref=%7B%22displayStr%22%3A%22EEST%22%2C%22offset%22%3A3%2C%22dst%22%3Atrue%2C%22windowsTz%22%3A%22Europe%2FHelsinki%22%7D; timezone=Europe%2FHelsinki; s_cc=true; s_sq=%5B%5BB%5D%5D; s_pv=public%3AsearchResults; s_vnum=1624628032261%26vn%3D3; s_invisit=true; s_lv_s=Less%20than%201%20day; s_depth=3; s_ppvl=public%253AsearchResults%2C34%2C31%2C1037%2C1043%2C937%2C1920%2C1080%2C1%2CP; s_nr=1622219559741-Repeat; s_lv=1622219559743; s_ppv=public%253AsearchResults%2C100%2C25%2C3696%2C1043%2C937%2C1920%2C1080%2C1%2CP"
}
s = requests.Session()
s.headers.update(headers)
app = TeleBot(TELEGRAM_TOKEN)
URLS = {
    'copart': {
        'url': 'https://www.copart.com/public/lots/search',
        'data': [
            {
                "referrer": "https://www.copart.com/ru/lotSearchResults/?free=true&query=&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22VOLKSWAGEN%5C%22%22%5D,%22YEAR%22:%5B%22lot_year:%5C%222014%5C%22%22,%22lot_year:%5C%222015%5C%22%22,%22lot_year:%5C%222016%5C%22%22,%22lot_year:%5C%222017%5C%22%22,%22lot_year:%5C%222018%5C%22%22,%22lot_year:%5C%222019%5C%22%22%5D%7D,%22sort%22:%5B%22auction_date_type%20desc%22,%22auction_date_utc%20asc%22%5D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D",
                "referrerPolicy": "strict-origin-when-cross-origin",
                "body": "draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=8&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=9&columns%5B9%5D%5Bname%5D=&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=10&columns%5B10%5D%5Bname%5D=&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=true&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=11&columns%5B11%5D%5Bname%5D=&columns%5B11%5D%5Bsearchable%5D=true&columns%5B11%5D%5Borderable%5D=true&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B12%5D%5Bdata%5D=12&columns%5B12%5D%5Bname%5D=&columns%5B12%5D%5Bsearchable%5D=true&columns%5B12%5D%5Borderable%5D=true&columns%5B12%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B12%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B13%5D%5Bdata%5D=13&columns%5B13%5D%5Bname%5D=&columns%5B13%5D%5Bsearchable%5D=true&columns%5B13%5D%5Borderable%5D=true&columns%5B13%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B13%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B14%5D%5Bdata%5D=14&columns%5B14%5D%5Bname%5D=&columns%5B14%5D%5Bsearchable%5D=true&columns%5B14%5D%5Borderable%5D=false&columns%5B14%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B14%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B15%5D%5Bdata%5D=15&columns%5B15%5D%5Bname%5D=&columns%5B15%5D%5Bsearchable%5D=true&columns%5B15%5D%5Borderable%5D=false&columns%5B15%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B15%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=asc&start=0&length=20&search%5Bvalue%5D=&search%5Bregex%5D=false&sort=auction_date_type+desc%2Cauction_date_utc+asc&defaultSort=true&filter%5BMAKE%5D=lot_make_desc%3A%22VOLKSWAGEN%22&filter%5BYEAR%5D=lot_year%3A%222014%22%2Clot_year%3A%222015%22%2Clot_year%3A%222016%22%2Clot_year%3A%222017%22%2Clot_year%3A%222018%22%2Clot_year%3A%222019%22&query=*&watchListOnly=false&freeFormSearch=false&page=0&size=20",
                "method": "POST",
                "mode": "cors"
            },
            {
                "referrer": "https://www.copart.com/ru/lotSearchResults/?free=true&query=&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22BODY%22:%5B%22body_style:%5C%224DR%20SPOR%5C%22%22,%22body_style:%5C%22CONVERTI%5C%22%22,%22body_style:%5C%22COUPE%5C%22%22,%22body_style:%5C%22HATCHBAC%5C%22%22,%22body_style:%5C%22SEDAN%204D%5C%22%22%5D,%22MAKE%22:%5B%22lot_make_desc:%5C%22FORD%5C%22%22%5D,%22YEAR%22:%5B%22lot_year:%5C%222019%5C%22%22,%22lot_year:%5C%222018%5C%22%22,%22lot_year:%5C%222017%5C%22%22,%22lot_year:%5C%222016%5C%22%22,%22lot_year:%5C%222015%5C%22%22,%22lot_year:%5C%222014%5C%22%22%5D%7D,%22sort%22:%5B%22auction_date_type%20desc%22,%22auction_date_utc%20asc%22%5D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D",
                "referrerPolicy": "strict-origin-when-cross-origin",
                "body": "draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=8&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=9&columns%5B9%5D%5Bname%5D=&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=10&columns%5B10%5D%5Bname%5D=&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=true&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=11&columns%5B11%5D%5Bname%5D=&columns%5B11%5D%5Bsearchable%5D=true&columns%5B11%5D%5Borderable%5D=true&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B12%5D%5Bdata%5D=12&columns%5B12%5D%5Bname%5D=&columns%5B12%5D%5Bsearchable%5D=true&columns%5B12%5D%5Borderable%5D=true&columns%5B12%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B12%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B13%5D%5Bdata%5D=13&columns%5B13%5D%5Bname%5D=&columns%5B13%5D%5Bsearchable%5D=true&columns%5B13%5D%5Borderable%5D=true&columns%5B13%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B13%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B14%5D%5Bdata%5D=14&columns%5B14%5D%5Bname%5D=&columns%5B14%5D%5Bsearchable%5D=true&columns%5B14%5D%5Borderable%5D=false&columns%5B14%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B14%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B15%5D%5Bdata%5D=15&columns%5B15%5D%5Bname%5D=&columns%5B15%5D%5Bsearchable%5D=true&columns%5B15%5D%5Borderable%5D=false&columns%5B15%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B15%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=asc&start=0&length=20&search%5Bvalue%5D=&search%5Bregex%5D=false&sort=auction_date_type+desc%2Cauction_date_utc+asc&defaultSort=true&filter%5BBODY%5D=body_style%3A%224DR+SPOR%22%2Cbody_style%3A%22CONVERTI%22%2Cbody_style%3A%22COUPE%22%2Cbody_style%3A%22HATCHBAC%22%2Cbody_style%3A%22SEDAN+4D%22&filter%5BMAKE%5D=lot_make_desc%3A%22FORD%22&filter%5BYEAR%5D=lot_year%3A%222019%22%2Clot_year%3A%222018%22%2Clot_year%3A%222017%22%2Clot_year%3A%222016%22%2Clot_year%3A%222015%22%2Clot_year%3A%222014%22&query=*&watchListOnly=false&freeFormSearch=false&page=0&size=20",
                "method": "POST",
                "mode": "cors"
            },
            {
                "referrer": "https://www.copart.com/ru/lotSearchResults/?free=true&query=&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22BODY%22:%5B%22body_style:%5C%224DR%20SPOR%5C%22%22,%22body_style:%5C%22CONVERTI%5C%22%22,%22body_style:%5C%22COUPE%5C%22%22,%22body_style:%5C%22HATCHBAC%5C%22%22,%22body_style:%5C%22SEDAN%204D%5C%22%22%5D,%22MAKE%22:%5B%22lot_make_desc:%5C%22FORD%5C%22%22%5D,%22YEAR%22:%5B%22lot_year:%5C%222019%5C%22%22,%22lot_year:%5C%222018%5C%22%22,%22lot_year:%5C%222017%5C%22%22,%22lot_year:%5C%222016%5C%22%22,%22lot_year:%5C%222015%5C%22%22,%22lot_year:%5C%222014%5C%22%22%5D%7D,%22sort%22:%5B%22auction_date_type%20desc%22,%22auction_date_utc%20asc%22%5D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D",
                "referrerPolicy": "strict-origin-when-cross-origin",
                "body": "draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=8&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=9&columns%5B9%5D%5Bname%5D=&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=10&columns%5B10%5D%5Bname%5D=&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=true&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=11&columns%5B11%5D%5Bname%5D=&columns%5B11%5D%5Bsearchable%5D=true&columns%5B11%5D%5Borderable%5D=true&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B12%5D%5Bdata%5D=12&columns%5B12%5D%5Bname%5D=&columns%5B12%5D%5Bsearchable%5D=true&columns%5B12%5D%5Borderable%5D=true&columns%5B12%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B12%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B13%5D%5Bdata%5D=13&columns%5B13%5D%5Bname%5D=&columns%5B13%5D%5Bsearchable%5D=true&columns%5B13%5D%5Borderable%5D=true&columns%5B13%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B13%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B14%5D%5Bdata%5D=14&columns%5B14%5D%5Bname%5D=&columns%5B14%5D%5Bsearchable%5D=true&columns%5B14%5D%5Borderable%5D=false&columns%5B14%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B14%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B15%5D%5Bdata%5D=15&columns%5B15%5D%5Bname%5D=&columns%5B15%5D%5Bsearchable%5D=true&columns%5B15%5D%5Borderable%5D=false&columns%5B15%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B15%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=asc&start=0&length=20&search%5Bvalue%5D=&search%5Bregex%5D=false&sort=auction_date_type+desc%2Cauction_date_utc+asc&defaultSort=true&filter%5BBODY%5D=body_style%3A%224DR+SPOR%22%2Cbody_style%3A%22CONVERTI%22%2Cbody_style%3A%22COUPE%22%2Cbody_style%3A%22HATCHBAC%22%2Cbody_style%3A%22SEDAN+4D%22&filter%5BMAKE%5D=lot_make_desc%3A%22FORD%22&filter%5BYEAR%5D=lot_year%3A%222019%22%2Clot_year%3A%222018%22%2Clot_year%3A%222017%22%2Clot_year%3A%222016%22%2Clot_year%3A%222015%22%2Clot_year%3A%222014%22&query=*&watchListOnly=false&freeFormSearch=false&page=0&size=20",
                "method": "POST",
                "mode": "cors"
            },
            {
                "referrer": "https://www.copart.com/ru/lotSearchResults/?free=true&query=&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22BODY%22:%5B%22body_style:%5C%224DR%20SPOR%5C%22%22,%22body_style:%5C%22HATCHBAC%5C%22%22,%22body_style:%5C%22SEDAN%204D%5C%22%22%5D,%22FUEL%22:%5B%22fuel_type_desc:%5C%22DIESEL%5C%22%22%5D,%22YEAR%22:%5B%22lot_year:%5C%222022%5C%22%22,%22lot_year:%5C%222021%5C%22%22,%22lot_year:%5C%222020%5C%22%22,%22lot_year:%5C%222019%5C%22%22,%22lot_year:%5C%222018%5C%22%22,%22lot_year:%5C%222017%5C%22%22,%22lot_year:%5C%222016%5C%22%22,%22lot_year:%5C%222015%5C%22%22%5D%7D,%22sort%22:%5B%22auction_date_type%20desc%22,%22auction_date_utc%20asc%22%5D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D",
                "referrerPolicy": "strict-origin-when-cross-origin",
                "body": "draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=8&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=9&columns%5B9%5D%5Bname%5D=&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=10&columns%5B10%5D%5Bname%5D=&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=true&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=11&columns%5B11%5D%5Bname%5D=&columns%5B11%5D%5Bsearchable%5D=true&columns%5B11%5D%5Borderable%5D=true&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B12%5D%5Bdata%5D=12&columns%5B12%5D%5Bname%5D=&columns%5B12%5D%5Bsearchable%5D=true&columns%5B12%5D%5Borderable%5D=true&columns%5B12%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B12%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B13%5D%5Bdata%5D=13&columns%5B13%5D%5Bname%5D=&columns%5B13%5D%5Bsearchable%5D=true&columns%5B13%5D%5Borderable%5D=true&columns%5B13%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B13%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B14%5D%5Bdata%5D=14&columns%5B14%5D%5Bname%5D=&columns%5B14%5D%5Bsearchable%5D=true&columns%5B14%5D%5Borderable%5D=false&columns%5B14%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B14%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B15%5D%5Bdata%5D=15&columns%5B15%5D%5Bname%5D=&columns%5B15%5D%5Bsearchable%5D=true&columns%5B15%5D%5Borderable%5D=false&columns%5B15%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B15%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=asc&start=0&length=20&search%5Bvalue%5D=&search%5Bregex%5D=false&sort=auction_date_type+desc%2Cauction_date_utc+asc&defaultSort=true&filter%5BBODY%5D=body_style%3A%224DR+SPOR%22%2Cbody_style%3A%22HATCHBAC%22%2Cbody_style%3A%22SEDAN+4D%22&filter%5BFUEL%5D=fuel_type_desc%3A%22DIESEL%22&filter%5BYEAR%5D=lot_year%3A%222022%22%2Clot_year%3A%222021%22%2Clot_year%3A%222020%22%2Clot_year%3A%222019%22%2Clot_year%3A%222018%22%2Clot_year%3A%222017%22%2Clot_year%3A%222016%22%2Clot_year%3A%222015%22&query=*&watchListOnly=false&freeFormSearch=false&page=0&size=20",
                "method": "POST",
                "mode": "cors"
            },
            {
                "referrer": "https://www.copart.com/ru/lotSearchResults/?free=true&query=&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22FUEL%22:%5B%22fuel_type_desc:%5C%22ELECTRIC%5C%22%22%5D,%22YEAR%22:%5B%22lot_year:%5C%222016%5C%22%22,%22lot_year:%5C%222017%5C%22%22,%22lot_year:%5C%222018%5C%22%22,%22lot_year:%5C%222019%5C%22%22,%22lot_year:%5C%222020%5C%22%22,%22lot_year:%5C%222021%5C%22%22%5D%7D,%22sort%22:%5B%22auction_date_type%20desc%22,%22auction_date_utc%20asc%22%5D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D",
                "referrerPolicy": "strict-origin-when-cross-origin",
                "body": "draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=8&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=9&columns%5B9%5D%5Bname%5D=&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=10&columns%5B10%5D%5Bname%5D=&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=true&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=11&columns%5B11%5D%5Bname%5D=&columns%5B11%5D%5Bsearchable%5D=true&columns%5B11%5D%5Borderable%5D=true&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B12%5D%5Bdata%5D=12&columns%5B12%5D%5Bname%5D=&columns%5B12%5D%5Bsearchable%5D=true&columns%5B12%5D%5Borderable%5D=true&columns%5B12%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B12%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B13%5D%5Bdata%5D=13&columns%5B13%5D%5Bname%5D=&columns%5B13%5D%5Bsearchable%5D=true&columns%5B13%5D%5Borderable%5D=true&columns%5B13%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B13%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B14%5D%5Bdata%5D=14&columns%5B14%5D%5Bname%5D=&columns%5B14%5D%5Bsearchable%5D=true&columns%5B14%5D%5Borderable%5D=false&columns%5B14%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B14%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B15%5D%5Bdata%5D=15&columns%5B15%5D%5Bname%5D=&columns%5B15%5D%5Bsearchable%5D=true&columns%5B15%5D%5Borderable%5D=false&columns%5B15%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B15%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=asc&start=0&length=20&search%5Bvalue%5D=&search%5Bregex%5D=false&sort=auction_date_type+desc%2Cauction_date_utc+asc&defaultSort=true&filter%5BFUEL%5D=fuel_type_desc%3A%22ELECTRIC%22&filter%5BYEAR%5D=lot_year%3A%222016%22%2Clot_year%3A%222017%22%2Clot_year%3A%222018%22%2Clot_year%3A%222019%22%2Clot_year%3A%222020%22%2Clot_year%3A%222021%22&query=*&watchListOnly=false&freeFormSearch=false&page=0&size=20",
                "method": "POST",
                "mode": "cors"
            }
        ],
        'keys': {
            'keys': ['ld', 'hb', 'ln', 'fv', 'syn', 'orr', 'lcd', 'scn', 'dd', 'sdd', 'la', 'bstl', 'vehTypDesc', 'clr', 'egn', 'cy', 'trf', 'drv', 'ft', 'hk', 'scl'],
            'values': ['', 'Текущая ставка', '№ лота', 'Номер VIN', 'Тип документа', 'Одометр', 'Основные моменты', 'Продавец', 'Основное повреждение', 'Вторичное повреждение', 'Оценочная розничная стоимость', 'Тип кузова', 'Цилиндры', 'Передача', 'Привод', 'Топливо', 'Ключи', 'Примечания']
        }
    }
}
data_cars = {
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
    image = requests.get(i['url']).content
    with open(f'./{car_id}/'+str(car_id)+' --- '+str(image_id)+'.jpg', 'wb') as f:
        f.write(image)

def coport_parser(copart_next_post):
    text = ''
    for key in range(len(URLS['copart']['keys']['keys'])):
        try:
            print(copart_next_post['ln'])
            text += URLS['copart']['keys']['values'][key] + ': ' + str(copart_next_post[URLS['copart']['keys']['keys'][key]]) + '\n'
        except Exception as e:
            print(e)
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
    try:
        images_list = json.loads(s.get('https://www.copart.com/public/data/lotdetails/solr/lotImages/31839991/USA').text)['data']['imagesList']['FULL_IMAGE']
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

def parser_thread():
    print('### START PARSER ###')
    copart_prev_post = ''
    while True:
        copart_data = URLS['copart']['data']
        for cars_filter in range(len(copart_data)):
            print(cars_filter)
            try:
                response_copart = json.loads(s.post(URLS['copart']['url'], data=copart_data[cars_filter]).text)['data']['results']['content']
            except Exception as e:
                print(e)
                print(f'Exception in copart global requests, iteration {cars_filter+1}')
                continue
            copart_next_post = response_copart[0]
            # if copart_prev_post != copart_next_post['ln']:
            coport_parser(copart_next_post)
            # copart_prev_post = copart_next_post['ln']
        print('checkout ------- copart ------- ' + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
        # time.sleep(300)

if __name__ == '__main__':
	thr_bot = threading.Thread(target=bot_thread)
	thr_bot.start()
	thr_parser = threading.Thread(target=parser_thread)
	thr_parser.start()