# -*- coding: utf-8 -*-
"""
@author: Birol Emekli
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException
from time import sleep
import sys
import re


istenenKisi = 1


class Control:
    def __init__(self, driver, time):
        self.driver = driver
        self.zaman = time

    def sayfaKontrol(self):

        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "mainTabView:gidisSeferTablosu_data")))
            if element != "":
                # Flags
                bulundu = False
                bulunanlar = []

                # Kac tane sefer var
                seferlerElementleri = self.driver.find_elements(By.XPATH,
                                                                "/html/body/div[3]/div[2]/div/div/div/div/form/div[1]/div/div[1]/div/div/div/div[1]/div/div/div/table/tbody/tr")
                seferSayisi = len(seferlerElementleri)

                # for row in range(1, seferSayisi):
                for row, seferElement in enumerate(seferlerElementleri):
                    try:
                        # TODO: seferlerElementleri ni kullan bastan bulmak yerine
                        #aranan = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div/div/div/form/div[1]/div/div[1]/div/div/div/div[1]/div/div/div/table/tbody/tr[{0}]/td[1]/span'.format(row)).text
                        aranan = seferElement.find_element(
                            By.XPATH, 'td[1]/span').text
                        print("bulunan saat : " + aranan +
                              " | aranan  saat : " + self.zaman)
                        sleep(0.5)
                        # if self.zaman == aranan:
                        # Zaman buyuktur olarak bak
                        arananSayi = aranan.replace(':', '')
                        arananSayi = int(arananSayi)
                        myZaman = int(self.zaman.replace(':', ''))

                        if arananSayi >= myZaman:
                            print(aranan + " kontrol et")
                            sleep(0.5)
                            # mainTabView:gidisSeferTablosu:0:j_idt109:0:somVagonTipiGidis1
                            # mainTabView:gidisSeferTablosu:1:j_idt109:0:somVagonTipiGidis1_input
                            # mainTabView:gidisSeferTablosu:2:j_idt109:0:somVagonTipiGidis1_input

                            # select = self.driver.find_element(By.XPATH, '//*[@id="mainTabView:gidisSeferTablosu:{0}:j_idt109:0:somVagonTipiGidis1_input"]'.format(0))
                            # select.find_elements(By.XPATH, './option')[0].get_attribute("textContent")

                            # sec = self.driver.find_element(By.XPATH, '//*[@id="mainTabView:gidisSeferTablosu:{0}:j_idt109:0:somVagonTipiGidis1_panel"]')

                            # sec.find_elements(By.XPATH, './div/ul/li')[0].get_attribute("textContent") ekonomi
                            # sec.find_elements(By.XPATH, './div/ul/li')[1].get_attribute("textContent") bussiness

                            # message = self.driver.find_element(
                            #     By.XPATH, '//*[@id="mainTabView:gidisSeferTablosu:{0}:j_idt109:0:somVagonTipiGidis1_label"]'.format(row - 1)).text
                            # if message[22] != '0':

                            secenekler = self.driver.find_elements(
                                By.XPATH, '//*[@id="mainTabView:gidisSeferTablosu:{0}:j_idt109:0:somVagonTipiGidis1_input"]/option'.format(row))
                            for secenek in secenekler:
                                secenekText = secenek.get_attribute(
                                    "textContent")
                                print(secenekText)
                                # parantez icinde sayi bul
                                bosKoltuk = int(
                                    re.search("\((\d+)\)", secenekText).groups()[0])

                                if ("Ekonomi" in secenekText and bosKoltuk >= istenenKisi+2) or ("Business" in secenekText and bosKoltuk >= istenenKisi):
                                    #print("Boş koltuk sayısı: ", bosKoltuk)
                                    bulunanText = "{} treninde {} bos koltuk var ".format(
                                        aranan, bosKoltuk)
                                    print('*'*20)
                                    print(bulunanText)
                                    print('*'*20)

                                    # return "successful"
                                    bulundu = True
                                    bulunanlar.append(bulunanText)
                                else:
                                    print("bos yer yok: ", bosKoltuk)
                                    message = ""
                                    # self.driver.quit()
                                    # return

                    except Exception as e:
                        print(e)
                        print("Saatinizde hata var...")
                        return
                        # self.driver.quit()
                        # sys.exit()
                else:
                    print('-'*30)

                if len(bulunanlar) > 0:
                    return bulunanlar
                else:
                    self.driver.quit()
                    return
            else:
                print("Aradığınız seferde boş yer yoktur...")

        except (TimeoutException, NoSuchElementException) as ex:
            print("TCDD sitesi yüklemede bir hata meydana geldi... Tekrar deneniyor...")
            self.driver.close()
            return
        except UnexpectedAlertPresentException as ex1:
            print("Güzergah bilgilerinde hata meydana geldi. Kontrol ederek tekrar deneyiniz. İstasyonları doğru girdiğinizden emin olunuz")
            self.driver.quit()
            exit()
