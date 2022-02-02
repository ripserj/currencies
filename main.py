# -*- coding: utf-8 -*-

import requests
import sqlite3
from bs4 import BeautifulSoup
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

Form, Window = uic.loadUiType("exchange.ui")
app = QApplication(sys.argv)

window = Window()
form = Form()
form.setupUi(window)

def reset_db():
    conn = sqlite3.connect('kurs.db')
    cur = conn.cursor()
    cur.execute("""DROP TABLE IF EXISTS kurs""")
    conn.commit()
    cur.execute("""CREATE TABLE IF NOT EXISTS kurs(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       date TEXT,
       quantity INT,
       kurs REAL);
       """)
    conn.commit()
    conn.close()


def insert_kurs(insert_values):
    conn = sqlite3.connect('kurs.db')
    conn.executemany("insert into kurs(date, quantity, kurs) values (?,?,?)", insert_values)
    conn.commit()


session = requests.Session()
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    'Accept-Encoding': "gzip, deflate, sdch",
}

session.headers = headers
response = session.get("https://cbr.ru/currency_base/dynamics/", headers=headers)

data_min_date = response.text.split('data-min-date="')[1].split('"')[0]
data_max_date = response.text.split('data-max-date="')[1].split('"')[0]

soup = BeautifulSoup(response.text, features="html.parser")
currencies = dict()
for tag in soup.find_all('option'):
    currencies[tag.contents[0].strip()] = tag['value']

def combobox_load():
    form.comboBox.clear()
    for item, value in currencies.items():
        form.comboBox.addItem(item, value)
    form.label_5.setText("Список валют загружен успешно!")

def get_data():
    reset_db()
    val_code = form.comboBox.currentData()
    response = session.get(
        "https://cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=" + val_code + "&UniDbQuery.From=" + data_min_date + "&UniDbQuery.To=" + data_max_date,
        headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    counter = 0
    insert_values = []
    for tag in soup.find_all('tr'):
        if counter > 1:
            actual_date = str(tag.contents[1]).replace('<td>', '').replace('</td>', '').strip()
            quantity = str(tag.contents[3]).replace('<td>', '').replace('</td>', '').strip()
            kurs = str(tag.contents[5]).replace('<td>', '').replace('</td>', '').strip().replace(',', '.').replace(' ','')
            value = (actual_date, quantity, kurs)
            insert_values.append(value)

        counter += 1
    insert_kurs(insert_values)


form.pushButton.clicked.connect(combobox_load)
form.pushButton_2.clicked.connect(get_data)

window.show()
app.exec()
