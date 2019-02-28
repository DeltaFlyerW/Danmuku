# -*- coding: utf-8 -*-
# coding=utf-8

from pprint import pprint

import re
import os
from selenium import webdriver
import win32con
import win32api
import time
import datetime
import pyperclip
import shutil
import selenium


def psleep(second):
    if second < 10:
        eprint("wait for " + str(second // 10), end=" ")
    while second > 0:
        if second % 10 == 0:
            eprint("wait for " + str(second // 10), end=" ")
        eprint(second % 10, end=" ")
        if second % 10 == 1:
            eprint()

        second = second - 1
        time.sleep(1)


def eprint(str="", end="\n"):
    try:
        print(str, end=end)
    except Exception as e:
        print(e, end=end)


def formatpath(str):
    if str.find("\\u002") != -1:
        str = str[0:str.find("\\u002")] + " " + str[str.find("\\u002") + 5:len(str)]

    list = "\\/:*?\"<>|"
    for i in range(len(list)):
        while str.find(list[i]) != -1:
            str = str[0:str.find(list[i])] + " " + str[str.find(list[i]) + 1:len(str)]

    return str.rstrip(".").rstrip()


def remove_dir(dir):
    dir = dir.replace('\\', '/')
    if os.path.isdir(dir):
        for p in os.listdir(dir):
            remove_dir(os.path.join(dir, p))
        if os.path.exists(dir):
            os.rmdir(dir)
    else:
        if os.path.exists(dir):
            os.remove(dir)


def ensureDir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def getvar(varname, content, punc=':', end=' '):
    if content.find(varname) == -1:
        return ''
    startbit = content.find(varname + punc) + len(varname + punc)
    endbit = content.find(end, startbit + 1)
    if endbit == -1:
        endbit = len(content)
    varcontent = content[startbit:endbit]
    return varcontent


def dstrip(str):
    t = str.find("\\")
    while t != -1:
        str = str[0:t] + "-" + str[t + 1:len(str)]
        t = str.find("\\")
    t = str.find("/")
    while t != -1:
        eprint(t)
        str = str[0:t] + "-" + str[t + 1:len(str)]
        t = str.find("/")
    while str[len(str) - 1] == " ":
        str = str[0:len(str) - 1]
    return str



def moveall(opath, npath):
    if not os.path.isdir(opath):
        return
    path = ""
    lpath = ""
    while os.path.isdir(opath + "/" + path):
        lpath = path
        lfile = os.listdir(opath + '/' + path)
        if len(lfile) == 0:
            if not os.path.exists(npath + '/' + path):
                os.makedirs(npath + '/' + path)
            os.remove(opath + '/' + path)
            moveall(opath, npath)
            return
        path = path + "/" + lfile[0]
    if not os.path.exists(npath + '/' + lpath):
        os.makedirs(npath + '/' + lpath)
    with open(opath + '/' + path, "r", encoding="utf-8") as f0:
        with open(opath + '/' + path, "w", encoding="utf-8", ) as f1:
            f1.write(f0.read())
    os.remove(opath + '/' + path)
    moveall(opath, npath)
    return


class Bili(object):
    def __init__(self):

        self.path = [r"D:\data\danmuku\Anime", "", "", "", ""]
        self.temp = r"D:\DF's Files\Temp"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"

        }
        self.cdownload = 0
        self.mode = 0
        self.handle = None

    def initfirefox(self):

        chromedriver = r"C:\Users\Dell\AppData\Local\Google\Chrome\Application\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        browser = webdriver.Chrome(chromedriver)
        browser.get("https://passport.bilibili.com/login")

        while browser.current_url != "https://www.bilibili.com/":
            time.sleep(1)
        return browser

    def downloaddanmuku(self, cid, date, pos, browser, count=-1):
        self.cdownload = self.cdownload + 1
        ensureDir(pos)

        lfile = os.listdir(pos)
        flags = 0
        ffile = 0
        for file in lfile:
            if os.path.isfile(pos + '/' + file):
                ffile = 1
                filename = file
                break
            else:
                remove_dir(pos + '/' + file)
        if count == -1:
            eprint("\t\t\t\t", end=" ")
        if count != -1 or ffile == 0:

            browser.get("https://api.bilibili.com/x/v2/dm/history?type=1&date={sdate}&oid={scid}".format(sdate=date, scid=cid))

            if count == 0:
                eprint("\n\t\t\t\t", end=" ")

            eprint(date, end=" ")
            count = count + 1
            if count == 3:
                count = 0

            if self.mode == 1:
                time.sleep(2)
            pyperclip.copy("{}.xml".format(date + "_" + cid))
            win32api.keybd_event(17, 0, 0, 0)
            win32api.keybd_event(83, 0, 0, 0)
            time.sleep(0.1)

            win32api.keybd_event(83, 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(1)

            if os.path.isfile(str(self.temp + "\\{}.xml".format(date + "_" + cid))):
                os.remove(str(self.temp + "\\{}.xml".format(date + "_" + cid)))

            win32api.keybd_event(17, 0, 0, 0)
            win32api.keybd_event(86, 0, 0, 0)
            time.sleep(0.1)

            win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.1)

            win32api.keybd_event(13, 0, 0, 0)
            time.sleep(0.1)
            win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
            while os.path.exists(str(self.temp + "\\{}.xml".format(date + "_" + cid))) != 1:
                time.sleep(0.1)

            if self.mode == 1:
                time.sleep(2)
            ffile = 0
            while ffile == 0:
                try:
                    with open(self.temp + "\\{}.xml".format(date + "_" + cid), "r", encoding="utf-8") as f0:
                        with open(pos + "\\" + "{}.xml".format(date + "_" + cid), "w", encoding="utf-8") as f1:
                            f1.write(f0.read())
                    ffile = 1
                except Exception as e:
                    time.sleep(0.1)
            time.sleep(0.1)
            while os.path.isfile(self.temp + "\\{}.xml".format(date + "_" + cid)):
                try:
                    os.remove(self.temp + "\\{}.xml".format(date + "_" + cid))

                except Exception as e:
                    time.sleep(0.1)

        else:
            date = filename[0:filename.find("_")]
            count = 0
            flags = 1

            eprint(date, end=" ")

        try:
            with open(pos + "\\{}.xml".format(date + "_" + cid), "r", encoding='UTF-8') as lastf:
                lines = lastf.read()
        except IOError:
            eprint("IOError R")
            time.sleep(10)
            with open(pos + "\\{}.xml".format(date + "_" + cid), "r", encoding='UTF-8') as lastf:
                lines = lastf.read()
        if len(lines) < 100:
            if flags == 0:
                os.remove(pos + "\\{}.xml".format(date + "_" + cid))

                psleep(300)
                browser.get('https://www.bilibili.com/')
                self.downloaddanmuku(cid, date, pos, browser, count - 1)
            else:
                os.remove(pos + "\\{}.xml".format(date + "_" + cid))

                self.downloaddanmuku(cid, date, pos, browser, 0)
            return
        else:
            results = re.findall("<d p=\"[\d.]*?,[\d.]*?,[\d.]*?,[\d.]*?,([\d]*?),", lines)

            if len(results) < int(lines[lines.find('<maxlimit>') + 10:lines.find('<', lines.find('<maxlimit>') + 10)]) * 0.9:
                if len(results) == 0:
                    os.remove(pos + "\\{}.xml".format(date + "_" + cid))

                eprint()
                return
            firsttime = int(results[0])
            for result in results:
                if int(result) < firsttime:
                    firsttime = int(result)

            if firsttime != 0:
                timestamp = firsttime
                timearray = time.localtime(timestamp)

                if date == time.strftime('%Y-%m-%d', timearray):
                    timestamp = firsttime - 86400
                    timearray = time.localtime(timestamp)
                    date = time.strftime('%Y-%m-%d', timearray)
                else:
                    date = time.strftime('%Y-%m-%d', timearray)
                try:
                    if self.mode == 1:
                        time.sleep(2)
                    self.downloaddanmuku(cid, date, pos, browser, count)
                except selenium.common.exceptions.TimeoutException:
                    time.sleep(2)
                    self.downloaddanmuku(cid, date, pos, browser, count)

            else:
                eprint()
                return

    def run(self):
        path = self.path

        browser = self.initfirefox()
        lanime = os.listdir(path[0])

        for anime in lanime:

            path[1] = path[0] + "/" + anime
            if os.path.isfile(path[1]):
                continue
            # if os.path.isdir(path[1] + "\\synced") or os.path.isdir(path[1] + "\\extra") == 0:
            #    continue

            eprint(anime)
            for season in os.listdir(path[1]):
                if season == "synced" and season != 'extra':
                    continue
                path[2] = path[1] + "/" + season

                if (os.path.isdir(path[2] + "\\synced") and season != "extra") or season == "synced":
                    continue
                eprint("\t" + season)
                if season != "extra":

                    with open(path[2] + '/partinfo.txt', "r", encoding="utf-8") as f:
                        lpartinfo = f.readlines()
                    lpart = os.listdir(path[2])
                    for i in range(len(lpart)):
                        if lpart[i] != "info.txt" and lpart[i] != "partinfo.txt":
                            path[3] = path[2] + "\\" + lpart[i]
                            if os.path.isdir(path[3] + "\\synced"):
                                continue
                            eprint("\t\t" + lpart[i])
                            date0 = datetime.datetime.now().strftime('%Y-%m-%d')
                            spartinfo = ""
                            for partinfo in lpartinfo:
                                # eprint(partinfo.encode("utf-8"))
                                # if  partinfo.encode("utf-8").find(b'\xef\xbb\xbf')!=-1:
                                #    partinfo = partinfo.encode("utf-8").replace(b'\xef\xbb\xbf', '').decode("utf-8")

                                if partinfo[0:partinfo.find(" ")] == lpart[i][0:lpart[i].find(" ")]:
                                    spartinfo = partinfo
                                    break
                            cid = spartinfo[spartinfo.find(" ") + 5:spartinfo.find(" title:")]
                            # eprint(cid)
                            self.downloaddanmuku(cid, date0, path[3], browser)
                            ensureDir(path[3] + "\\synced")
                    if len(lduration) != 0:
                        with open(path[3] + "/partinfo.txt", "w", encoding="utf-8") as f:
                            for i in range(len(lcid)):
                                f.write("p" + lpage[i] + " cid:" + lcid[i] + " title:" + lpname[i] + " duration:" + lduration[i] + "\n")
                    else:
                        with open(path[3] + "/partinfo.txt", "w", encoding="utf-8") as f:
                            for i in range(len(lcid)):
                                f.write("p" + lpage[i] + " cid:" + lcid[i] + " title:" + lpname[i] + "\n")
                else:
                    lextra = os.listdir(path[2])
                    for exvideo in lextra:
                        path[3] = path[2] + '/' + exvideo
                        if not (os.path.isfile(path[3] + "/info.txt") or os.path.isfile(path[3] + "/partinfo.txt")):
                            continue
                        if exvideo == "synced":
                            continue

                        if os.path.isdir(path[3] + "\\synced"):
                            lobject = os.listdir(path[3])
                            fsync = 0
                            for object in lobject:

                                if object != 'info.txt' and object != 'synced' and object != 'partinfo.txt':
                                    fsync = 1
                                    break
                            if fsync == 1:
                                continue

                        if os.path.isfile(path[3] + "/info.txt"):
                            with open(path[3] + "/info.txt", "r", encoding="utf-8") as f:
                                info = f.read()

                            info = info[0:info.find('"related":')]

                            if anime != '精灵宝可梦' and anime!='鲁路修' and anime!='碧阳学生会议事录':
                                isofficial = re.findall('"owner":{"mid":[\d]*,"name":"哔哩哔哩番剧","face":"', info)
                                if len(isofficial) != 0 and (anime != '月刊少女野崎君' or anime != '悠悠式'):
                                    ensureDir(path[2] + '/cache/TV/' + exvideo)
                                    try:
                                        shutil.copy(path[3] + "/info.txt", path[2] + '/cache/TV/' + exvideo + "/info.txt")
                                        remove_dir(path[3])
                                    except FileNotFoundError:
                                        psleep(5)
                                        shutil.copy(path[3] + "/info.txt", path[2] + '/cache/TV/' + exvideo + "/info.txt")
                                        remove_dir(path[3])
                                    continue
                                wordlist = {"配", "粤", "英语", "法语", "德语", "TVB", "国语"}
                                fbanword = 0
                                for w in wordlist:

                                    if exvideo.find(w) != -1:
                                        ensureDir(path[2] + '/cache/TV/' + exvideo)
                                        try:

                                            shutil.copy(path[3] + "/info.txt", path[2] + '/cache/TV/' + exvideo + "/info.txt")
                                            remove_dir(path[3])
                                        except FileNotFoundError:
                                            psleep(5)
                                            shutil.copy(path[3] + "/info.txt", path[2] + '/cache/TV/' + exvideo + "/info.txt")
                                            remove_dir(path[3])
                                        fbanword = 1
                                        break
                                if fbanword == 1:
                                    continue

                                if exvideo.find(anime) == -1:
                                    keyword = re.findall('name="keywords" content="(.*?)"/>', info)
                                    if len(keyword) == 0:
                                        keyword = re.findall('name="keywords" content="(.*?)" />', info)
                                        if len(keyword) == 0:
                                            keyword = re.findall('name="keywords" content="(.*?)">', info)
                                    keyword = keyword[0].lower()
                                    if keyword.find(anime.lower()) == -1:
                                        fexist = 0
                                        lastpos = 0
                                        temp = anime.lower()

                                        for i in range(len(temp) - 1):

                                            if (keyword.find(temp[i]) == -1 and keyword.find(temp[i + 1]) == -1) or (keyword.find(temp[i], lastpos) - lastpos > 2 and keyword.find(temp[i + 1], lastpos) - lastpos > 3):
                                                if lastpos != 0:
                                                    fexist = 1
                                                    break
                                            lastpos = keyword.find(temp[i])
                                        if fexist:
                                            ensureDir(path[2] + '/cache/other/' + exvideo)
                                            try:
                                                shutil.copy(path[3] + "/info.txt", path[2] + '/cache/other/' + exvideo + "/info.txt")
                                                remove_dir(path[3])
                                            except FileNotFoundError:
                                                psleep(5)
                                                shutil.copy(path[3] + "/info.txt", path[2] + '/cache/other/' + exvideo + "/info.txt")
                                                remove_dir(path[3])
                                            continue

                            eprint("\t\t" + exvideo)

                            posbegin = info.find('window.addEventListener')
                            if posbegin == -1:
                                posbegin = info.find('"videoData"')
                            posend = info.find('"subtitle":')
                            info = info[posbegin:posend]

                            lcid = re.findall(r'"cid":([\d]*),"page":', info)

                            lpage = re.findall("\"cid\":[\d]*,\"page\":([\d]*),\"from\":\".*?\",\"part\":\".*?\"", info)
                            lpname = re.findall("\"cid\":[\d]*,\"page\":[\d]*,\"from\":\".*?\",\"part\":\"(.*?)\"", info)
                            lduration = re.findall("\"cid\":[\d]*,\"page\":[\d]*,\"from\":\".*?\",\"part\":\".*?\",\"duration\":([\d]*)", info)
                            if len(lcid) == 0:
                                lcid = re.findall('"page":[\d]*,"type":.*?,"part":".*?","cid":([\d]*),', info)
                                lpage = re.findall('"page":([\d]*),"type":.*?,"part":".*?","cid":[\d]*,', info)
                                lpname = re.findall('"page":[\d]*,"type":.*?,"part":"(.*?)","cid":[\d]*,', info)
                            if len(lduration) != 0:
                                with open(path[3] + "/partinfo.txt", "w", encoding="utf-8") as f:
                                    for i in range(len(lcid)):
                                        f.write("p" + lpage[i] + " cid:" + lcid[i] + " title:" + lpname[i] + " duration:" + lduration[i] + "\n")
                            else:
                                with open(path[3] + "/partinfo.txt", "w", encoding="utf-8") as f:
                                    for i in range(len(lcid)):
                                        f.write("p" + lpage[i] + " cid:" + lcid[i] + " title:" + lpname[i] + "\n")
                        else:
                            eprint("\t\t" + exvideo)
                            with open(path[3] + "/partinfo.txt", "r", encoding="utf-8") as f:
                                info = f.read()


                            lcid = re.findall(r'cid:([\d]*) ', info)
                            lduration = []
                            lpage=[]
                            lpname = re.findall("filename:(.*?)\n", info)
                            for i in range(len(lcid)):
                                lpage.append(str(i+1))

                        for i in range(len(lcid)):

                            eprint("\t\t\t" + lpname[i])
                            '''if os.path.isdir(path[3] + "/p" + lpage[i]) and lpname[i] !="":

                                eprint("\t\t\trename")
                                path[4] = path[3] + "/p" + lpage[i] + " " + formatpath(lpname[i])

                                ensureDir(path[4])
                                for file in os.listdir(path[3] + "/p" + lpage[i]):
                                    if os.path.isfile(path[3] + "/p" + lpage[i]+"/"+file):
                                        shutil.copy(path[3] + "/p" + lpage[i]+"/"+file,path[4]+"/"+file)
                                    else:
                                        ensureDir(path[4] + "/" +file)
                                remove_dir(path[3] + "/p" + lpage[i])
                                continue'''

                            if (lpname[i] != ""):
                                try:
                                    path[4] = path[3] + "/p" + lpage[i] + " " + formatpath(lpname[i])
                                    ensureDir(path[4])

                                except Exception as e:
                                    eprint(e)
                                    path[4] = path[3] + "/p" + lpage[i]
                                    ensureDir(path[4])
                            else:
                                path[4] = path[3] + "/p" + lpage[i]
                                ensureDir(path[4])

                            if os.path.isdir(path[4] + "\\synced"):
                                continue

                            date0 = datetime.datetime.now().strftime('%Y-%m-%d')
                            self.downloaddanmuku(lcid[i], date0, path[4], browser)
                            print('\t\t\t\t' + str(self.cdownload))
                            ensureDir(path[4] + "\\synced")
                        ensureDir(path[3] + "\\synced")
                ensureDir(path[2] + "\\synced")
            ensureDir(path[1] + "\\synced")
        input("end")


if __name__ == '__main__':
    b = Bili()
    b.run()
