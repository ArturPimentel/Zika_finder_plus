"""
Created by Diandra Kubo and Artur Pimentel
CSE 40437/60437 - Social Sensing and Cyber-Physical Systems 
Spring 2016
University of Notre Dame
Project
Plotting the Maps
"""
# -*- coding: utf-8 -*-
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import sys
from datetime import datetime
from mpl_toolkits.basemap import Basemap, addcyclic

"""
#You should choose your combination of keywords from here!
if ('zika' in texto) : #-1
if (('fever' in texto) or ('febre' in texto) or ('fiebre' in texto)) : #-2
if (('joint pain' in texto) or ('dor nas juntas' in texto)) : #-3 
if (('microcephaly' in texto) or ('microcefalia' in texto)) : #-4
if (('mosquito' in texto) or ('mosquitoes' in texto)) : #-5
if ('aedes aegypti' in texto) : #-6
if ('dengue' in texto) : #-7
if ('rash' in texto) : #-8
if (('muscle pain' in texto) or ('dor no corpo' in texto) or ('dolor en el cuerpo' in texto)) : #-9
if (('red eyes' in texto) or ('olho vermelho' in texto)) : #-10
if (('fever' in texto) or ('febre' in texto) or ('fiebre' in texto)) and (('red eyes' in texto) or ('olho vermelho' in texto)) and (('muscle pain' in texto) or ('dor no corpo' in texto) or ('dolor en el cuerpo' in texto)) and (('joint pain' in texto) or ('dor nas juntas' in texto)):
if (('fever' in texto) or ('febre' in texto) or ('fiebre' in texto)) and (('joint pain' in texto) or ('dor nas juntas' in texto)) : 
if (('fever' in texto) or ('febre' in texto) or ('fiebre' in texto)) and (('muscle pain' in texto) or ('dor no corpo' in texto) or ('dolor en el cuerpo' in texto)):
if (('fever' in texto) or ('febre' in texto) or ('fiebre' in texto)) and (('red eyes' in texto) or ('olho vermelho' in texto)):
if (('fever' in texto) or ('febre' in texto) or ('fiebre' in texto)) and ('rash' in texto):
if ('rash' in texto) and (('muscle pain' in texto) or ('dor no corpo' in texto) or ('dolor en el cuerpo' in texto)):
if (('mosquito' in texto) or ('mosquitoes' in texto)) and (('bitten' in texto) or ('bite'  in texto) or ('mordid' in texto) or ('picad' in texto) or ('bit' in texto)):
if ('brazil' not in texto) and ('brazilian' not in texto) and ('brasil' not in texto):
if (('got fever' in texto) or ('have fever' in texto) or ('com febre' in texto) or ('tenho febre' in texto) or ('con fiebre' in texto) or ('tengo fiebre' in texto)) : #-2
if (('got bit' in texto) or ('mordid' in texto) or ('picad' in texto) or ('picadura' in texto)) and ('mosquito' in texto):
if (('muscle pain' in texto)  or ('muscle ache' in texto)  or ('body pain' in texto) or ('dor no corpo' in texto) or ('corpo dolorido' in texto) or ('dolor en el cuerpo' in texto) or ('cuerpo dolorido' in texto)) :
"""

class Plota():
	
	def __init__(self, input_file, dire):
		self.input_file = input_file
		self.dire = dire
		self.mapping()

	def mapping(self):				
		plt.figure(figsize=(12, 10)) 
		f = open(self.input_file, 'r')
		data = f.readlines()[1:]
		f.close()
		lats1=[];lons1=[];lats2=[];lons2=[];tips=[]
		
		"""
		#Change you title and filename according to your search
		plt.title("Locations of tweets containing keyword 'Dengue'"); name="dengue"
		plt.title("Locations of tweets containing keyword 'Aedes Egypti'"); name="aedes"
		plt.title("Locations of tweets containing keywords 'Mosquito'/'Mosquitoes'"); name="mosquito"
		plt.title("Locations of tweets containing keywords 'fever'+'joint pain'"); name="fever_jointpain"
		plt.title("Locations of tweets containing keyword 'microcephaly'"); name="mocrocefalia"
		plt.title("Locations of tweets containing keywords 'fever'+'pain'"); name="fever_pain"
		plt.title("Locations of tweets containing keywords 'fever'+'red eye'"); name="fever_redeye"
		plt.title("Locations of tweets containing keywords 'fever'+'rash'"); name="fever_rash"
		plt.title("Locations of tweets containing keywords 'pain'+'rash'"); name="pain_rash"		
		plt.title("Locations of tweets containing keywords 'brazil', 'brasil', 'brazilian'"); name="brazil"
		plt.title("Locations of tweets containing keywords related to aedes aegypti"); name="aedes"
		"""
		plt.title("Locations of tweets containing keywords related to aedes aegypti"); name="aedes"
		cont=0
		cont2=0
		for i in xrange(len(data)):
			line = data[i].split('"');texto = line[1].lower();line = line[0].split(',')	
			if ('aedes aegypti' in texto):						
					if line[3]==' 1 ': #tweets with location on it
						cont+=1
						lats1.append(line[1])
						lons1.append(line[2])
					else: # tweets where location was from the user location
						lats2.append(line[1])
						lons2.append(line[2])
					cont2+=1				
		
		lat = lats1 + lats2
		lon = lons1 + lons2
		lons1 = np.array(lons1).astype('f')
		lats1 = np.array(lats1).astype('f')
		lons2 = np.array(lons2).astype('f')
		lats2 = np.array(lats2).astype('f')
		lat = np.array(lat).astype('f')
		lon = np.array(lon).astype('f')

		c = Basemap(projection='mill')
		c.drawcoastlines()
		c.drawstates()
		c.drawcountries()

		x, y = c(lons2, lats2)		
		c.scatter(x, y, marker='o',color='g', label="User")
		x, y = c(lons1, lats1)		
		c.scatter(x, y, marker='o',color='r', label="Tweet")
		plt.legend(loc='best')		
		os.system("mkdir plots")
		plt.savefig("plots\\%s.png" % name)		

		return

if __name__ == "__main__":
	Plota(sys.argv[1], "C:\\Users\\Diandra\\Documents\\Social Sensing and Cyber Physical Systems\\project\\FINAL\\")
