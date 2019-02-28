# -*- coding:utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup, ResultSet
import re
import os
import time
import shutil
import requests
import selenium


def formatpath(str):
    list = "\/:*?\"<>|"
    for i in range(len(list)):
        while str.find(list[i]) != -1:
            str = str[0:str.find(list[i])] + " " + str[str.find(list[i]) + 1:len(str)]
    return str


def remove_dir(dir):
    dir = dir.replace('\\', '/')
    if (os.path.isdir(dir)):
        for p in os.listdir(dir):
            remove_dir(os.path.join(dir, p))
        if (os.path.exists(dir)):
            os.rmdir(dir)
    else:
        if (os.path.exists(dir)):
            os.remove(dir)


def ensureDir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def psleep(second):
    while second > 0:
        if second % 10 == 0:
            print("\nwait for " + str(second // 10), end=" ")
        print(second % 10, end=" ")
        second = second - 1
        time.sleep(1)
    print("\n")


def parse(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    res = response.content.decode()
    return res


class Bilibili:
    def __init__(self):
        # correctdir()
        # input()
        self.mode = 1
        self.path = ["d:/data/danmuku/Anime", "", ""]
        self.avlist = []
        self.titlelist = []
        chromedriver = r"C:\\Users\Dell\AppData\Local\Google\Chrome\Application\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)

    def main(self):

        driver = self.driver
        path = self.path
        keywords = []

        if self.mode:
            dirs = os.listdir(path[0])
            for i1 in range(len(dirs)):
                if i1 == 0:
                    continue

                if os.path.isfile(path[0] + "\\" + dirs[i1] + "\\extra\\extralist.txt") == 0:
                    keywords.append(dirs[i1])

            ekeywords = os.listdir(path[0])

            with open("keyword.txt", "r")as f:
                temp = f.readlines()
            i = 0
            while i < len(temp):
                fexist = 0
                for okeyword in ekeywords:
                    if temp[i].strip().rstrip() == okeyword:
                        fexist = 1
                        break

                if fexist != 1:
                    keywords.append(temp[i].strip().rstrip())
                i = i + 1
        else:
            lkeyword = os.listdir('extrakeyword')
            for keyword in lkeyword:
                if not os.path.isdir('extrakeyword/' + keyword + '/synced'):
                    keywords.append(keyword)

        for keyword in keywords:
            print(keyword)
            if os.path.isdir(path[0] + "\\" + keyword + '\\' + 'synced'):
                continue
            reservedav = []
            avlist = []
            titlelist = []
            if self.mode:
                blsection = ["32", "33"]
                for s in blsection:
                    numpage = 1
                    i1 = 0
                    while i1 < numpage:
                        driver.get("https://search.bilibili.com/all?keyword={skeyword}&from_source=banner_search&order=click&duration=0&tids_1=13&tids_2={ssection}&page={spage}".format(skeyword=keyword, spage=i1 + 1, ssection=s))
                        time.sleep(1)
                        if i1 == 0:
                            if (len(driver.find_elements_by_xpath("//button[@class='pagination-btn']")) != 0):
                                numpage = int(driver.find_element_by_xpath("//button[@class='pagination-btn']").text)

                        i1 = i1 + 1

                        page = driver.page_source
                        soup: BeautifulSoup = BeautifulSoup(page, 'html.parser')
                        items: ResultSet = soup.find_all('li', class_="video matrix")
                        if len(items) == 0:
                            button=driver.find_elements_by_xpath('//*[@id="server-search-app"]/div[2]/div[2]/div/div[1]/div/div[1]/i')
                            if len(button)!=0:
                                button[0].click()
                                time.sleep(1)
                                page = driver.page_source
                                soup: BeautifulSoup = BeautifulSoup(page, 'html.parser')
                                items: ResultSet = soup.find_all('li', class_="video matrix")
                            else:
                                break

                        for i in range(len(items)):
                            item = items[i].find('a', class_='img-anchor')
                            av = int(re.findall("video/av([\d]*)", item['href'])[0])

                            reservedav.append(av)
                            temp = items[i].find('span', class_='so-icon hide').text
                            temp = temp.strip().rstrip()
                            if temp.find("万") != -1 or int(temp) > 200:
                                flag = 1
                                try:
                                    print(item['title'])
                                except:
                                    print("error")
                                titlelist.append(item['title'])

                                avlist.append(av)
                                flagf = 1
                                try:
                                    ensureDir(path[0] + "//" + keyword + "//extra//av" + str(av) + " " + formatpath(item['title']))
                                except:
                                    ensureDir(path[0] + "//" + keyword + "//extra//av" + str(av))
                                    flagf = 0
                                if flagf == 1:
                                    with open(path[0] + "//" + keyword + "//extra//av" + str(av) + " " + formatpath(item['title']) + "//info.txt", "w", encoding="utf-8") as f:
                                        f.write(parse('https://www.bilibili.com/video/av' + str(av)))
                                else:
                                    with open(path[0] + "//" + keyword + "//extra//av" + str(av) + "//info.txt", "w", encoding="utf-8") as f:
                                        f.write(parse('https://www.bilibili.com/video/av' + str(av)))

            bpsection = ["完结动画", "连载动画"]
            for s in bpsection:
                driver.get("https://www.biliplus.com/api/do.php?source=biliplus&act=search&o=default&n=20&p=1&word={skeyword}%20%40{ssection}".format(skeyword=keyword, ssection=s))
                time.sleep(5)
                while len(driver.find_elements_by_xpath('//div[@style="display:inline-block;border-radius:5px;border:1px solid #AAA;background:#DDD;padding:8px 20px;cursor:pointer"]')) != 0:

                    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath('//div[@style="display:inline-block;border-radius:5px;border:1px solid #AAA;background:#DDD;padding:8px 20px;cursor:pointer"]'))
                    time.sleep(1)
                    driver.find_element_by_xpath('//div[@style="display:inline-block;border-radius:5px;border:1px solid #AAA;background:#DDD;padding:8px 20px;cursor:pointer"]').click()
                    time.sleep(3)
                    if len(driver.find_elements_by_xpath('//div[@class="pointer"]')) == 0:
                        driver.refresh()
                        time.sleep(3)
                videomatrixs = driver.find_elements_by_xpath('//div[@class="pointer"]')
                for videomatrix in videomatrixs:
                    av = videomatrix.get_attribute('data-link')
                    if av[0:4] == '/ban':
                        continue
                    av = int(av[9:len(av) - 1])
                    flagr = 0
                    for rav in reservedav:
                        if rav == av:
                            flagr = 1
                            break
                    if flagr == 1:
                        continue
                    flags=1
                    fexsit = 0
                    while flags:
                        try:
                            print('check av' + str(av))
                            if parse('https://www.bilibili.com/video/av' + str(av))[0:130] != '<!DOCTYPE html><html><head itemprop="video" itemscope itemtype="http://schema.org/VideoObject"><title data-vue-meta="true">视频去哪了呢？':
                                fexsit = 1
                                break
                            flags = 0
                        except selenium.common.exceptions.WebDriverException:
                            flags = 1
                    if fexsit:
                        continue
                    flags = 0
                    while flags == 0:
                        try:
                            flags = 1
                            fpage = parse('https://www.biliplus.com/video/av{}/'.format(str(av)))
                        except:
                            flags = 0
                            psleep(10)
                    while len(fpage) < 400:
                        psleep(30)
                        fpage = parse('https://www.biliplus.com/video/av{}/'.format(str(av)))
                    ensureDir(path[0] + "//temp")
                    with open(path[0] + "//temp//temp.txt", "w", encoding="utf-8") as f:
                        f.write(fpage)
                    title = re.findall('"lastupdatets":.*?,"title":"(.*?)"', fpage)
                    if len(title) == 0:
                        title = re.findall('"lastupdate":.*?,"title":"(.*?)"', fpage)
                    try:
                        print(title)
                    except:
                        print("error")
                    title = title[0]
                    self.titlelist.append(title)
                    self.avlist.append(av)
                    flagf = 1
                    try:
                        ensureDir(path[0] + "//" + keyword + "//extra//av" + str(av) + " " + formatpath(title))
                    except:
                        ensureDir(path[0] + "//" + keyword + "//extra//av" + str(av))
                        flagf = 0
                    if flagf == 1:
                        with open(path[0] + "//" + keyword + "//extra//av" + str(av) + " " + formatpath(title) + "//info.txt", "w", encoding="utf-8") as f:
                            f.write(fpage)
                    else:
                        with open(path[0] + "//" + keyword + "//extra//av" + str(av) + "//info.txt", "w", encoding="utf-8") as f:
                            f.write(fpage)

            ensureDir(path[0] + "//" + keyword + "//extra")
            with open(path[0] + "//" + keyword + "//extra//extralist.txt", "w", encoding="utf-8") as f:
                for i in range(len(avlist)):
                    f.write("av:" + str(avlist[i]) + " title:" + titlelist[i] + "\n")
            if not self.mode:
                ensureDir('extrakeyword/' + keyword + '/synced')
        driver.quit()


if __name__ == '__main__':
    bilibili = Bilibili()
    bilibili.main()
