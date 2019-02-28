#pylint:disable=W0613
#pylint:disable=W0312

#pylint:disable=W0612
import os
import re

def getvar(varname,content,punc=':'):
	varcontent=content[content.find(content+':')+len(content)+1:content.find(' ',content.find(content+':')+len(content)+1)]
	return varcontent

def matchsimple(keyword,content):
	keyword=keyword.lower()
	content=content.lower()
	for i in range(len(keyword)):
		if content.find(keyword[i])==-1:
			if content.find(keyword=[i+1])==-1:
				return 0
	
	return 1
				

def ensureDir(path):
    if not os.path.exists(path):
        os.makedirs(path)



class danmukum:
		def __init__(self,dirpath):
			self.dirpath=dirpath
			self.path=['/storage/emulated/0/data/danmuku','','']

		def apexfilter(self,ldanmu):
			with open(os.getcwd()+'/data/apexfilter.txt','w',encoding='utf-8' ) as f:
				for idanmu in range(len(ldanmu)):
				
					None
			return ldanmu
				
				
		def run(self):
			self.savedata(self.mergefromdir(self.dirpath))

			
			
		def getdanmufromfile(self,path):
				fstr=""
				
				with open(path,'r',encoding='utf-8') as f:
						fstr=f.read()
						
				p1=r'(<d p=".*?</d>)'
				lsdanmu=re.findall(p1,fstr)
				
				ldanmu=[]
				ddanmu=['0 pos','1 type','2 fontsize','3 color','4 timestamp','5 pooltype','6 userid','7 danmuid','8 comtent','9 prot']
				
				
				
				
				
				for sdanmu in lsdanmu:
					usedinfo=sdanmu[sdanmu.find('p="')+3:sdanmu.find('">')]
					ddanmu=usedinfo.split(',')
					ddanmu.append(sdanmu[sdanmu.find('">')+2:sdanmu.find('</d>')])
					ddanmu.append(sdanmu)
					
					
					ldanmu.append(ddanmu)
				return ldanmu
			
		def savedata(self,ldanmu,dirpath=os.getcwd()+'/data',filename="danmu"):
			ensureDir(dirpath)
			with open(dirpath+"/"+filename+".txt",'w',encoding='utf-8') as f:
				f.write('<?xml version="1.0" encoding="UTF-8"?><i><chatserver>chat.bilibili.com</chatserver><chatid>0</chatid><mission>0</mission><maxlimit>{}</maxlimit><state>0</state><real_name>0</real_name>'.format(str(len(ldanmu))))
				for danmu in ldanmu:
					f.write(danmu[9])
				f.write('</i>')
						
		def danmufilter(self,ldanmu,lrule):
			lpattern=[]
			for rule in lrule:
				lpattern.append(re.compile(rule))
			f=open('./data/filter.txt','w',encoding='utf-8')
			for idanmu in range(len(ldanmu)):
				for ipattern in range(len(lpattern)):
					if lpattern[ipattern].search(ldanmu[idanmu][9]) is not None:
						f.write(ldanmu[idanmu][9]+' '+lrule[ipattern]+'\n')
						del ldanmu[idanmu]
			f.close()
			ldanmu=self.apexfilter(ldanmu)
			return ldanmu
			

		def mergefromdir(self,dirpath):
				ldanmu=[]
				lfile=os.listdir(dirpath)
				for file in lfile:
						if file=='synced':
								continue
				
						tldanmu=self.getdanmufromfile(dirpath+'/'+file)
						tldanmu.reverse()
						itime=0
						print(len(tldanmu))
						if len(ldanmu)!=0 and len(tldanmu)!=0:
							
							while tldanmu[itime][4]<=ldanmu[len(ldanmu)-1][4]:
							
								
								itime=itime+1
							ldanmu.extend(tldanmu[itime:])
						else:
							ldanmu.extend(tldanmu)
								 
		                      
								
				print(len(ldanmu))
				return  ldanmu		
		def mergefromdirs(self,ldirpath):
			ldanmu=[]
			for dirpath in ldirpath:
				ldanmu.extend(self.mergefromdir(dirpath))
			return ldanmu

		'''
		def getanimename(self):
			path=self.path
			sanime=input("anime:")
			lanime=os.listdir(self.path[0])
			fexist=0
			for anime in lanime:
				if anime==sanime:
					fexist=1
					break
			if fexist==0:
				print("no such anime")
				self.getanimename()
			path[1]=path[0]+'/'+sanime
			lseason=os.listdir(path[1])
			for iseason in range(len(lseason)):
				if lseason[iseason]=='extra':
					continue
				print('[{}] '.format(str(iseason))+ lseason(iseason))
			nseason=input('input the number:')
			while nseason>0 and nseason<len(lseason-1):
				nseason=input('input the number:')
			path[2]=path[1]+'/'+lseason[nseason]
			leposide=os.listdir(path[2])
			for ieposide in range(len(leposide)):
				if leposide[ieposide]=='extra':
					continue
				print('[{}] '.format(str(ieposide))+ leposide(ieposide))
			neposide=input('input the number:')
			while neposide>0 and neposide<len(leposide-1):
				neposide=input('input the number:')
				'''
	
		def mergeaccordingname(self,anime,season,eposide):
			path=self.path
			path[1]=path[0]+'/'+anime
			partinfo=open(path[1]+'/'+season+'/partinfo').readlines[int(eposide[1:eposide.find(' ')])]
			cid = getvar('cid',partinfo)
			info=open(path[1]+'/'+season+'/info.txt').read()
			#duration = re.search(
			duration=1449
			


if __name__ == '__main__':
    sdirpath=input("dirpath:")
    danmumerger = danmukum(sdirpath)
    danmumerger.run()