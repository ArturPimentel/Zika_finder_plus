"""
Created by Diandra Kubo and Artur Pimentel
CSE 40437/60437 - Social Sensing and Cyber-Physical Systems 
Spring 2016
University of Notre Dame
Project
Main Class
"""
# -*- coding: utf-8 -*-
import numpy as np
import json
import sys
from datetime import datetime


class Process():	
	def __init__(self, input_file,  dire):
		self.input_file = input_file
		self.dire = dire
		self.readsTweets()
		self.process()
		
	def deformata(self, s):
		return s.decode('utf-8')
	
	def formata(self, s):
		return s.encode('utf-8')

	def readsTweets(self):
		f = open(self.dire+self.input_file, "r")
		tweets = f.readlines()
		self.tweets=[]
		for i in xrange(len(tweets)): 
			if tweets[i]!='\n' and len(tweets[i])>3:
				try:
					t = json.loads(unicode(tweets[i]).encode('utf-8'))
				except:
					sys.stdout.write("'"+tweets[i]+"'")
					print len(tweets[i])
					sys.exit()
				self.tweets.append(t)		
		return
		
	def process(self):
		self.lon=[]
		self.lat=[]
		self.ids=[]
		self.tipos=[]
		self.datas=[]
		self.texts=[]
		cont=0;cont1=0;cont2=0;cont3=0
		tam = len(self.tweets)
		loc=[]	
		existentes=[]	
		lat_ex=[];lon_ex=[]
		data=[]
		
		#-------------This part should be commented if running for the first time-----------------------
		f = open(self.dire+'addresses_newkeywords.txt', 'r')
		data = f.readlines()[1:] 
		for i in xrange(len(data)):
			line = data[i].split('"')
			lat_ex.append(line[0].split(",")[0])
			lon_ex.append(line[0].split(",")[1])
			existentes.append(self.deformata(line[1]))
		f.close()
		#------------------------------------------------------------------------------------------------
		
		existentes = np.array(existentes)
		self.locs=[]
		tamanho = len(self.tweets)
		for i in xrange(tamanho):
			if (i%500)==0:
				f = open(self.dire+"infos.txt", "a")
				f.write(str(i)+"/"+str(tamanho)+"\n")
				f.close()
			t = self.tweets[i]			
			if t['place']!=None:
				lat_center = (float(t['place']['bounding_box']['coordinates'][0][0][1]) + float(t['place']['bounding_box']['coordinates'][0][2][1]))/2 
				lon_center = (float(t['place']['bounding_box']['coordinates'][0][0][0]) + float(t['place']['bounding_box']['coordinates'][0][2][0]))/2
				self.lon.append(lon_center)
				self.lat.append(lat_center)
				self.ids.append(t['id'])
				self.tipos.append(1)
				self.texts.append(unicode(t['text']).encode('utf-8'))
				self.datas.append(t['created_at'])
				cont1+=1
				cont+=1
			elif t['user']['location']!=None:
				x = self.formata(t['user']['location'])				
				if (x in tuple(existentes))==False:
					#self.locs.append(x) #--------------This line should be uncommented if running for the first time
					cont3+=1
					cont+=1
				else:
					ind = np.where(existentes==x)
					self.lon.append(lon_ex[ind[0][0]])
					self.lat.append(lat_ex[ind[0][0]])
					self.ids.append(t['id'])
					self.tipos.append(2)
					self.texts.append(unicode(t['text']).encode('utf-8'))
					self.datas.append(t['created_at'])
					cont2+=1
					cont+=1
				
		f = open(self.dire+"infos.txt", "a")
		f.write(str(cont3)+ " localizacoes de user nao processadas\n")
		f.write(str(cont2)+ " tem localizacao no user mas ja foi processada\n")
		f.write(str(cont1)+ " tem localizacao no tweet\n")
		f.write(str(cont)+" de "+str(len(self.tweets))+ " tinham localizacao. "+str( float(cont)/float(len(self.tweets))*100)+"%\n")
		f.close()
		
		#--------------This part should be uncommented if running for the first time------------
		#f = open("locations_newkeywords.txt", 'w')
		#for i in self.locs:
		#	f.write(i+"\n") 
		#f.close()
		#---------------------------------------------------------------------------------------

		
		#--------------This part should be commented if running for the first time------------
		sys.stdout.write("id, latitude, longitude, locationtype, timestamp, text\n")
		for i in xrange(len(self.lat)):
			print self.ids[i], ",", self.lat[i],  ",", self.lon[i],  ",", self.tipos[i],  ",", self.datas[i],  ", \"", self.texts[i].replace("\n"," ").replace("\"", "'"), "\""
		#---------------------------------------------------------------------------------------	
		return
			
		

if __name__ == "__main__":
	Process(sys.argv[1], 'C:\\Users\\Diandra\\Documents\\Social Sensing and Cyber Physical Systems\\project\\FINAL\\')	
	
	
