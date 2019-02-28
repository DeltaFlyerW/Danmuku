import os


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


def getvar(varname, content, punc=':', end=' '):
    startbit = content.find(varname + punc) + len(varname + punc)
    endbit = content.find(end, startbit + 1)
    if endbit == -1:
        endbit = len(content)
    varcontent = content[startbit:endbit]
    return varcontent


def joinpath(lobject):
    path = ''
    for object in lobject:
        path = path + '/' + object
    return path


def ensureDir(path):
    if not os.path.exists(path):
        os.makedirs(path)


class Bilibili:
    def __init__(self):
        self.path = [r"D:\data\danmuku\Anime", "", "", "", ""]
        self.pathother = r"D:\data\danmuku\Others"
        self.pathrecover = r"D:\data\danmuku\Recover"
        self.lexsitcid = []
        self.lrecovercid = []

    def getallexsitcid(self):
        path = self.path
        lanime = os.listdir(path[0])
        for anime in lanime:

            path[1] = path[0] + "/" + anime
            if os.path.isfile(path[1]):
                continue

            for season in os.listdir(path[1]):
                if season == "synced":
                    continue
                path[2] = path[1] + "/" + season

                if season != "extra":
                    lline = open(path[2] + '/partinfo.txt', encoding='utf-8').readlines()
                    for line in lline:
                        self.lexsitcid.append(getvar('cid', line))
                else:
                    lextra = os.listdir(path[2])
                    for exvideo in lextra:
                        path[3] = path[2] + '/' + exvideo
                        if not os.path.isfile(path[3] + "/info.txt"):
                            continue
                        if not os.path.isfile(path[3] + '/partinfo.txt'):
                            continue
                        lline = open(path[3] + '/partinfo.txt', encoding='utf-8').readlines()
                        for line in lline:
                            self.lexsitcid.append(getvar('cid', line))
        print(len(self.lexsitcid))

    """def getlostcid(self):

        dirtree = [self.pathother, '', '', '', '']
        o1dir = os.listdir(dirtree[0])
        for o1 in o1dir:
            if o1 == 'Cache':
                continue
            dirtree[1] = dirtree[0] + '/' + o1
            o2dir = os.listdir(dirtree[1])

            lcid = []
            lastcid = ''
            for o2 in o2dir:

                dirtree[2] = dirtree[1] + '/' + o2
                if o2[len(o2) - 4, len(o2)] == '.xml':
                    fdirnum = 2
                    content = open(dirtree[2], encoding='utf-8').read()
                    scid = getvar('<chatid', content, '>', '<')
                    fexist = 0
                    try:
                        self.lexsitcid.index(scid)
                        fexist = 1
                    except Exception as e:
                        fexist = 0
                    if fexist == 0:

                        if scid != lastcid:
                            ensureDir(self.pathrecover + '/' + o1 + '/' + o2)

                            lcid.append(scid)
                        else:
                            break

                else:
                    if os.path.isdir(dirtree[2]):
                        dirtree[3] = dirtree[2] + '/' + o2
                        o3dir = os.listdir(dirtree[3])

                        lcid = []
                        lastcid = ''
                        for o3 in o3dir:

                            dirtree[4] = dirtree[3] + '/' + o3
                            if o2[len(o2) - 4, len(o2)] == '.xml':
                                fdirnum = 2
                                content = open(dirtree[2], encoding='utf-8').read()
                                scid = getvar('<chatid', content, '>', '<')
                                fexist = 0
                                try:
                                    self.lexsitcid.index(scid)
                                    fexist = 1
                                except Exception as e:
                                    fexist = 0
                                if fexist == 0:

                                    if scid != lastcid:
                                        ensureDir(self.pathrecover + '/' + o1 + '/' + o2)

                                        lcid.append(scid)
                                    else:
                                        break

                            else:
            if fdirnum == 2:
                ensureDir(self.pathrecover + '/' + o1)
                with open(self.pathrecover + '/' + o1 + '/partinfo.txt') as f:
                    for cid in lcid:
                        f.write('cid:' + cid + '\n')

        lpath = [self.pathother]
        flags = 1
        while flags:
            lobject = os.listdir(joinpath(lpath))
            fnextlevel = 0
            for object in lobject:
                if os.path.isdir(joinpath(lpath) + '/' + object + '/synced'):
                    result = self.getcidfromdir(joinpath(lpath) + '/' + object, self.pathother, self.pathrecover)
                if result == 0:
                    lpath.append(object)
                    fnextlevel = 1
                    break
                if result == 1:
                    continue
            if fnextlevel == 0:
                lpath.pop()"""

    def checkdir(self, path):
        lobject = os.listdir(path)
        for object in lobject:
            result = self.getcidfromdir(path + '/' + object, self.pathother, self.pathrecover)
            if result == 0:
                self.checkdir(path + '/' + object)

    def checkdir(self, path):
        lobject = os.listdir(path)
        for object in lobject:
            result = self.getcidfromdir(path + '/' + object, self.pathother, self.pathrecover)
            if result == 0:
                self.checkdir(path + '/' + object)




    def run(self):
        self.checkdir(self.pathother)

    def getcidfromdir(self, path, opath, npath):
        print('\n' + path)
        lobject = os.listdir(path)
        lcid = []
        lastcid = ''
        lfilename = []
        result = 1
        for object in lobject:
            #print(object)
            if os.path.isdir(path + '/' + object):
                result= 0
                break
            else:
                if object[len(object) - 4:len(object)] != '.xml':
                    result= -1
                    break
                else:
                    danmu = open(path + '/' + object, encoding='utf-8').read()
                    scid = getvar('<chatid', danmu, '>', '<')
                    if scid == lastcid:
                        result=1
                        break
                    else:
                        lastcid = scid
                    try:
                        self.lexsitcid.index(scid)
                        print('existed', end=' ')
                        fexist = 1
                    except Exception as e:
                        fexist = 0

                    if fexist == 0:
                        print(scid, end=' ')
                        lcid.append(scid)
                        lfilename.append(object[:len(object) - 4])
                        ensureDir(npath + path[len(opath):])

        if len(lcid) != 0:

            with open(npath + path[len(opath):] + '/partinfo.txt', 'w', encoding='utf-8') as f:
                for icid in range(len(lcid)):
                    f.write('cid:' + lcid[icid] + ' ' + 'filename:' + lfilename[icid] + '\n')


        return result


if __name__ == '__main__':
    b = Bilibili()
    b.getallexsitcid()
    b.run()
