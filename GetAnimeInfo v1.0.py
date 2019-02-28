# -*- coding:utf-8 -*-
from typing import List, Any, Union

from selenium import webdriver
from bs4 import BeautifulSoup, ResultSet
import re
import os
import time
import requests


def switch_tab(browser, origintab):
    time.sleep(1)
    browser.close()
    newhandles = browser.window_handles
    for i2 in range(len(newhandles)):

        if newhandles[i2] != origintab:
            browser.switch_to_window(newhandles[i2])
            break


def parse(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    res = response.content.decode()
    return res


def ensureDir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def formatpath(str):
    list = "\/:*?\"<>|"

    for i in range(len(list)):
        #print(list[i])
        str.replace(list[i],  ' ', 20)
        #print(str)
    #while(str.find('/'))!=0:
    #    str=str[0,]
    return str


def formathtml(str):
    lastpos = -1
    while str.find("&", lastpos + 1) != -1:
        lastpos = str.find("&")
        str = str[0:str.find("&") + 1] + "amp;" + str[str.find("&") + 1:len(str)]
    return str


class Bilibili:
    def __init__(self):
        self.path = ["", "", ""]

        self.path[0] = (r"D:\data\danmuku\Anime")
        chromedriver = r"C:\\Users\Dell\AppData\Local\Google\Chrome\Application\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.browser = webdriver.Chrome(chromedriver)

    def main(self):
        path = self.path
        browser = self.browser
        origintab = browser.window_handles[0]
        self.browser.get("http://space.bilibili.com/7300570/bangumi")

        time.sleep(1)
        animes = self.browser.find_elements_by_xpath("//a[contains(@class,'cover')]")
        unnamed = 0
        while len(animes) == 0:
            time.sleep(0.1)
            print("w1")
            animes = self.browser.find_elements_by_xpath("//a[contains(@class,'cover')]")

        time.sleep(3)
        next_page = browser.find_elements_by_xpath('//li[@class="be-pager-next"]')
        numpage = browser.find_elements_by_xpath('//span[@class="be-pager-total"]')[0].text
        numpage = int(numpage[2:len(numpage) - 2])

        syncanimes = os.listdir(path[0])

        for i1 in range(numpage):

            animes = self.browser.find_elements_by_xpath("//a[@target='_blank' and @class='title']")

            for anime in animes:

                animename = anime.get_attribute("title")
                try:
                    print(animename)
                except UnicodeEncodeError:
                    None
                fsync = 0
                for syncanime in syncanimes:

                    if animename == syncanime:
                        fsync = 1
                if fsync == 1:
                    continue
                anime.click()

                browser.switch_to.window(browser.window_handles[1])
                i = 0
                while len(browser.find_elements_by_class_name('misl-ep-item')) == 0:
                    i = i + 1
                    print("w3 "+str(i))
                    if i == 20:
                        browser.refresh()
                        i = 0
                    time.sleep(0.1)
                browser.find_element_by_class_name('misl-ep-item').click()
                time.sleep(0.5)
                switch_tab(browser, origintab)
                # page = str(browser.page_source).encode("utf-8")

                time.sleep(1)
                page: str = parse(browser.current_url)
                with open(path[0] + "\\info.txt", 'w', encoding="utf-8") as f:
                    f.write(page)

                animename = page[page.find('"series_title":"'):page.find('"', page.find('"series_title":"') + 16)].rstrip()

                if animename == "":
                    animename = page[page.find('"series":"') + 10:page.find('"', page.find('"series":"') + 10)]
                if animename == "":
                    animename = page[page.find('"title":"') + 9:page.find('"', page.find('"title":"') + 9)]
                if animename == "":
                    animename = "unnamed " + str(unnamed)
                    unnamed = unnamed + 1
                if animename.find('u002')!=-1 or animename.find('/')!=-1:
                    animename = "unnamed " + str(unnamed)
                    unnamed = unnamed + 1

                animename = formatpath(animename)
                fsync = 0

                for syncanime in syncanimes:

                    if animename == syncanime:
                        browser.close()
                        browser.switch_to.window(browser.window_handles[0])
                        fsync = 1
                if fsync == 1:
                    continue
                syncanimes.append(animename)
                print(animename)
                path[1] = path[0] + '\\' + animename

                ensureDir(path[1])
                flag1 = 1
                seasonflag = 1
                syncseaseasons = []

                while flag1:

                    if len(browser.find_elements_by_xpath('//div[@class = "entry-old"]')) != 0:
                        browser.find_element_by_xpath('//div[@class = "btn-old"]').click()
                        time.sleep(3)
                    page = parse(browser.current_url)
                    seasontitles = []
                    seasons = browser.find_elements_by_xpath('//li[contains(@report-id,"click_season")]')

                    for i in range(len(seasons)):
                        seasontitles.append(seasons[i].text)
                    # input(seasontitles)

                    if len(seasontitles) == 1:
                        seasonflag = 0
                        path[2] = path[1] + "\\" + seasontitles[0]

                    if len(seasontitles) == 0:
                        seasonflag = 0
                        path[2] = path[1] + "\\TV"

                    else:

                        current_season = browser.find_element_by_xpath('//li[@class="season-item on"]').text


                        current_season = formatpath(current_season)
                        path[2] = path[1] + '\\' + current_season
                        syncseaseasons.append(current_season)
                        print(current_season)

                    cids = re.findall('"aid":[\d]*,"cid":([\d]*),', page)
                    index_titles = re.findall('"index":".*?","index_title":"(.*?)"', page)

                    if len(index_titles) == 0:
                        titleFormat = re.findall('"title":".*?","titleFormat":"(.*?)","vid":".*?",', page)

                        longTitle = re.findall('"title":".*?","titleFormat":".*?","vid":".*?","longTitle":"(.*?)"', page)
                        for i in range(len(titleFormat) - 1):
                            index_titles.append(formatpath(titleFormat[i] + " " + longTitle[i]))

                    ensureDir(path[2])
                    with open(path[2] + "\\info.txt", 'w', encoding="utf-8") as f:
                        f.write(page)
                    with open(path[2] + "\\partinfo.txt", 'w', encoding="utf-8") as f:
                        for i in range(len(cids) - 1):
                            f.write("p" + str(i + 1) + " cid:" + cids[i] + " title:" + index_titles[i] + "\n")
                            try:
                                index_titles[i]=formatpath(index_titles[i])
                                ensureDir(path[2] + '\\p' + str(i + 1) + ' ' + index_titles[i])
                            except FileNotFoundError:
                                ensureDir(path[2] + '\\p' + str(i + 1) + ' ' +"unnamed " + str(unnamed))
                                unnamed = unnamed + 1
                            except OSError:
                                ensureDir(path[2] + '\\p' + str(i + 1) + ' ' + "unnamed " + str(unnamed))
                                unnamed = unnamed + 1
                    if seasonflag == 1:
                        flag2 = 1
                        seasons = browser.find_elements_by_xpath('//li[@class="season-item"]')

                        for season in seasons:
                            flag2 = 1

                            for syncseaseason in syncseaseasons:
                                if season.text == syncseaseason:
                                    flag2 = 0
                                    break
                            if flag2 == 1:
                                season.click()
                                time.sleep(0.5)
                                while len(browser.find_elements_by_xpath('//li[contains(@class,"episode-item")]')) == 0:
                                    time.sleep(0.1)
                                    print('//li[@class="episode-item"]')
                                browser.find_element_by_xpath('//li[@report-id="click_ep"]').click()
                                time.sleep(2)
                                break
                        if flag2 == 0:
                            flag1 = 0
                    else:
                        flag1 = 0

                browser.close()
                browser.switch_to.window(browser.window_handles[0])
            if i1 == numpage - 1:
                continue
            next_page[0].click()
            time.sleep(1)
            next_page = browser.find_elements_by_xpath('//li[@class="be-paper-next"]')
            while len(next_page) == 0:
                time.sleep(0.1)

                print(next_page)
                next_page = browser.find_elements_by_xpath('//li[@class="be-pager-next"]')


if __name__ == '__main__':
    bilibili = Bilibili()
    bilibili.main()
