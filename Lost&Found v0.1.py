# -*- coding:utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import os
import time
import requests
import selenium


def formatpath(fstr):
    flist = "\\/:*?\"<>|."
    for i in range(len(flist)):
        while fstr.find(flist[i]) != -1:
            fstr = fstr[0:fstr.find(flist[i])] + " " + fstr[fstr.find(flist[i]) + 1:len(fstr)]
    return fstr.rstrip()


def remove_dir(fdir):
    fdir = fdir.replace('\\', '/')
    if os.path.isdir(fdir):
        for p in os.listdir(fdir):
            remove_dir(os.path.join(fdir, p))
        if os.path.exists(fdir):
            os.rmdir(fdir)
    else:
        if os.path.exists(fdir):
            os.remove(fdir)


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


def eprint(fstr="", end="\n"):
    try:
        print(fstr, end=end)
    except Exception as e:
        print(e, end=end)


def matchsimple(keyword, content):
    keyword = keyword.lower()
    content = content.lower()
    for i in range(len(keyword)):
        if content.find(keyword[i]) == -1:
            if content.find(keyword=[i + 1]) == -1:
                return 0
            else:
                if i != 0 and content.find(keyword[i + 1]) - content.find(keyword[i - 1]) > 4:
                    return 0
        else:
            if i != 0 and content.find(keyword[i]) - content.find(keyword[i - 1]) > 3:
                return 0
    return 1


def parse(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    res = response.content.decode()
    return res


def getvar(varname, content, punc=':', end=' '):
    if content.find(varname)==-1:
        return ''
    startbit = content.find(varname + punc) + len(varname + punc)
    endbit = content.find(end, startbit + 1)
    if endbit == -1:
        endbit = len(content)
    varcontent = content[startbit:endbit]
    return varcontent



class Bilibili:
    def __init__(self):
        # correctdir()
        # input()
        self.mode = 1
        self.path = ["d:/data/danmuku/Lost&Found", "", ""]
        self.avlist = []
        self.titlelist = []
        chromedriver = r"C:\\Users\Dell\AppData\Local\Google\Chrome\Application\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)

    def main(self):

        driver = self.driver
        path = self.path
        lkeyword = []
        lduration = []
        lmode = []
        ltype=[]
        luid=[]
        with open(path[0] + "/keyword.txt", "r")as f:
            lline = f.readlines()
        for line in lline:
            lkeyword.append(getvar('keyword', line))
            lduration.append(getvar('duration(min)', line))
            lmode.append(getvar('mode', line))
            ltype.append(getvar('type', line))
            luid.append(getvar('uid', line))

        for ikeyword in range(len(lkeyword)):
            keyword = lkeyword[ikeyword]

            lblsection = ['&tids_1=1&tids_2=27', '&tids_1=13&tids_2=32', '&tids_1=13&tids_2=33', '&tids_1=13&tids_2=152', '&tids_1=23&tids_2=145', '&tids_1=23&tids_2=146', '&tids_1=23&tids_2=83', '&tids_1=11&tids_2=187']
            lbpsection = ['综合', "完结动画", "连载动画", '官方延伸', '欧美电影', '日本电影', '其他国家', '连载剧集']
            if lmode[ikeyword] == '':
                lsblsection = lblsection
                lsbpsection = lbpsection
            if lmode[ikeyword] == 'anime':
                lsblsection = ['&tids_1=13&tids_2=32', '&tids_1=13&tids_2=33']
                lsbpsection = ["完结动画", "连载动画"]
            if lmode[ikeyword] == 'cartoon':
                lsblsection = ['&tids_1=13&tids_2=32', '&tids_1=13&tids_2=33', '&tids_1=23&tids_2=83', '&tids_1=11&tids_2=187']
                lsbpsection = ["完结动画", "连载动画",'其他国家', '连载剧集']
            #if lmode
            for isection in range(len(lsblsection)):
                reservedav = []
                reservedtitle = []
                blavlist = []
                bltitlelist = []
                bpavlist = []
                bptitlelist = []
                numpage = 1
                i1 = 0
                fbanned = 0
                while i1 < numpage:

                    driver.get("https://search.bilibili.com/all?keyword={skeyword}&from_source=banner_search&order=click&duration=0{ssection}&page={spage}".format(skeyword=keyword, spage=i1 + 1, ssection=lsblsection[isection]))
                    time.sleep(1)
                    if i1 == 0:
                        if len(driver.find_elements_by_xpath("//button[@class='pagination-btn']")) != 0:
                            numpage = int(driver.find_element_by_xpath("//button[@class='pagination-btn']").text)

                    i1 = i1 + 1

                    page = driver.page_source
                    soup: BeautifulSoup = BeautifulSoup(page, 'html.parser')
                    items = soup.find_all('li', class_="video matrix")
                    if len(items) == 0:
                        try:
                            driver.find_element_by_xpath('//*[@id="server-search-app"]/div[2]/div[2]/div/div[1]/div/div[1]/i').click()
                        except selenium.common.exceptions.NoSuchElementException:
                            fbanned = 1
                            break
                        time.sleep(1)
                        page = driver.page_source
                        soup: BeautifulSoup = BeautifulSoup(page, 'html.parser')
                        items = soup.find_all('li', class_="video matrix")
                    for i in range(len(items)):
                        item = items[i].find('a', class_='img-anchor')
                        av = int(re.findall(r"video/av([\d]*)", item['href'])[0])
                        reservedav.append(av)
                        reservedtitle.append(item['title'])
                        if self.mode:
                            ndanmu = items[i].find('span', class_='so-icon hide').text
                            ndanmu = ndanmu.strip().rstrip()
                            if ndanmu.find("万") != -1 or int(ndanmu) > 200:

                                bltitlelist.append(item['title'])
                                blavlist.append(av)
                                duration = items[i].find('span', class_='so-imgTag_rb').text.strip().rstrip().split(':')

                                if len(duration)==3 or (len(duration)==2 and int(duration[0]) > int(lduration[ikeyword])):

                                    eprint(item['title'])
                                    flagf = 1
                                    try:
                                        ensureDir(path[0] + "//" + keyword + "//bilibili//av" + str(av) + " " + formatpath(item['title']))
                                    except:
                                        ensureDir(path[0] + "//" + keyword + "//bilibili//av" + str(av))
                                        flagf = 0
                                    if flagf == 1:
                                        with open(path[0] + "//" + keyword + "//bilibili//av" + str(av) + " " + formatpath(item['title']) + "//info.txt", "w", encoding="utf-8") as f:
                                            f.write(parse('https://www.bilibili.com/video/av' + str(av)))
                                    else:
                                        with open(path[0] + "//" + keyword + "//bilibili//av" + str(av) + "//info.txt", "w", encoding="utf-8") as f:
                                            f.write(parse('https://www.bilibili.com/video/av' + str(av)))
                if self.mode:
                    if not fbanned:
                        with open(path[0] + "//" + keyword + "//bilibili//{} list.txt".format(lsbpsection[isection]), "w", encoding="utf-8") as f:
                            for i in range(len(blavlist)):
                                f.write("av:" + str(blavlist[i]) + " title:" + bltitlelist[i] + "\n")
                        with open(path[0] + "//" + keyword + "//bilibili//{} reservelist.txt".format(lsbpsection[isection]), "w", encoding="utf-8") as f:
                            for i in range(len(reservedav)):
                                f.write("av:" + str(reservedav[i]) + " title:" + reservedtitle[i] + "\n")


                f502 = 1
                while f502:
                    f502 = 0
                    driver.get("https://www.biliplus.com/api/do.php?source=biliplus&act=search&o=default&n=20&p=1&word={skeyword}%20%40{ssection}".format(skeyword=keyword, ssection=lsbpsection[isection]))
                    while len(driver.find_elements_by_xpath('//div[@class="pointer"]')) == 0 and driver.find_element_by_xpath('//div [@id="footer"]').text != '没有更多啦~':
                        time.sleep(0.1)
                    while len(driver.find_elements_by_xpath('//div[@style="display:inline-block;border-radius:5px;border:1px solid #AAA;background:#DDD;padding:8px 20px;cursor:pointer"]')) != 0:

                        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath('//div[@style="display:inline-block;border-radius:5px;border:1px solid #AAA;background:#DDD;padding:8px 20px;cursor:pointer"]'))
                        time.sleep(1)
                        if (len(driver.find_elements_by_xpath('//div[@style="display:inline-block;border-radius:5px;border:1px solid #AAA;background:#DDD;padding:8px 20px;cursor:pointer"]')) != 0):
                            driver.find_element_by_xpath('//div[@style="display:inline-block;border-radius:5px;border:1px solid #AAA;background:#DDD;padding:8px 20px;cursor:pointer"]').click()
                        time.sleep(1)
                        if len(driver.find_elements_by_xpath('//div[@class="pointer"]')) == 0:
                            driver.get("https://www.biliplus.com/api/do.php?source=biliplus&act=search&o=default&n=20&p=1&word={skeyword}%20%40{ssection}".format(skeyword=keyword, ssection=lbpsection[isection]))

                            time.sleep(3)
                    videomatrixs = driver.find_elements_by_xpath('//div[@class="pointer"]')
                    tele = driver.find_elements_by_xpath('//div[@style="text-align:center;font-weight:bold"]')
                    if len(videomatrixs) == 0 and len(tele) and tele[0].text.find('502') != -1:
                        f502 = 1

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

                    # eprint(parse('https://www.bilibili.com/video/av' + str(av))[0:130])
                    flags = 1
                    fexsit=0
                    while flags:
                        try:
                            print('check av'+str(av))
                            if parse('https://www.bilibili.com/video/av' + str(av))[0:130] != '<!DOCTYPE html><html><head itemprop="video" itemscope itemtype="http://schema.org/VideoObject"><title data-vue-meta="true">视频去哪了呢？':
                                fexsit = 1
                                break
                            flags = 0
                        except selenium.common.exceptions.WebDriverException:
                            flags = 1
                    if fexsit:
                        continue

                    flags = 0

                    fpage = ''

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
                    # ensureDir(path[0] + "//temp")
                    # with open(path[0] + "//temp//temp.txt", "w", encoding="utf-8") as f:
                    #    f.write(fpage)
                    # fkeyword = re.search('name="keywords" content="(.*?)" />').string
                    # if not matchsimple(keyword, fkeyword):
                    #    continue
                    title = re.findall('"lastupdatets":.*?,"title":"(.*?)"', fpage)
                    if len(title) == 0:
                        title = re.findall('"lastupdate":.*?,"title":"(.*?)"', fpage)

                    title = title[0]
                    eprint(title)
                    bptitlelist.append(title)
                    bpavlist.append(av)
                    flagf = 1
                    try:
                        ensureDir(path[0] + "//" + keyword + "//biliplus//av" + str(av) + " " + formatpath(title))
                    except:
                        ensureDir(path[0] + "//" + keyword + "//biliplus//av" + str(av))
                        flagf = 0
                    if flagf == 1:
                        with open(path[0] + "//" + keyword + "//biliplus//av" + str(av) + " " + formatpath(title) + "//info.txt", "w", encoding="utf-8") as f:
                            f.write(fpage)
                    else:
                        with open(path[0] + "//" + keyword + "//biliplus//av" + str(av) + "//info.txt", "w", encoding="utf-8") as f:
                            f.write(fpage)



        driver.quit()


if __name__ == '__main__':
    bilibili = Bilibili()
    bilibili.main()
