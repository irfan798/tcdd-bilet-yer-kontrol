# -*- coding: utf-8 -*-
"""
@author: Birol Emekli
"""
from selenium import webdriver
from time import sleep
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import PySimpleGUI as sg
from threading import Thread

import Control
import Rota
import DriverSetting
import DriverGet

from datetime import datetime


class PushSafer():
    def sendNotification(self, baslik, mesaj):
        url = 'https://www.pushsafer.com/api'
        post_fields = {
            "t": baslik,
            "m": mesaj,
            "s": 20,
            "pr": 2,
            "v": 3,
            "i": 9,
            "d": 'a',
            "k": "6augZeHQP55WWR37JhgS"
        }
        request = Request(url, urlencode(post_fields).encode())
        json = urlopen(request).read().decode()
        print(json)


pushSafer = PushSafer()
#pushSafer.sendNotification('Naber Sait', "Sait love sencer")


def driverSetting():
    return DriverSetting.DriverSetting().driverUP()


def driverGet(drivers):
    DriverGet.DriverGet(drivers).driverGet()


def rota(driver, first_location, last_location, date):
    Rota.Rota(driver, first_location, last_location, date).dataInput()


def control(driver, timee):
    response = Control.Control(driver, timee).sayfaKontrol()

    if response:
        notif = " - ".join(response)
        pushSafer.sendNotification(
            'TCDD Bilet Kontrol', notif)
        driver.quit()
        sys.exit()


font = ('Arial', 10)
sg.theme('DarkBlue')

layout = [
    [[sg.Column([[sg.Text('TCDD')]], justification='center')]],
    [sg.Text('Nereden :', size=(7, 1)), sg.Combo(['Gebze', 'Bilecik YHT', 'Eskişehir',
                                                  'İstanbul(Söğütlü Ç.)', 'İstanbul(Pendik)'], default_value='Eskişehir', key='nereden')],
    [sg.Text('Nereye :', size=(7, 1)), sg.Combo(['Gebze', 'Bilecik YHT', 'Eskişehir',
                                                 'İstanbul(Söğütlü Ç.)', 'İstanbul(Pendik)'], default_value='İstanbul(Pendik)', key='nereye')],
    [sg.Text('Tarih :', size=(7, 1)), sg.InputText(
        ['04.09.2022'], size=(14, 5), key='tarih')],
    [sg.Text('Saat  :', size=(7, 1)), sg.InputText(
        '14:20',      size=(14, 5), key='saat')],
    [sg.Button('Ara'), sg.Button('Durdur'), sg.Button('Kapat')]
]


window = sg.Window('Python App', layout, size=(
    250, 250), resizable=False, font=font)


def mainLoop():

    while True:
        print(datetime.now())
        driver = driverSetting()
        driverGet(driver)
        rota(driver, nereden, nereye, tarih)
        control(driver, saat)

        print("waiting")
        sleep(60*2)


while True:

    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Kapat':

        window.close()
        sys.exit()

    if event == 'Ara':

        nereden = values['nereden']
        nereye = values['nereye']
        tarih = values['tarih']
        saat = values['saat']

        th = Thread(target=mainLoop).start()
