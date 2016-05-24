"""
Zikafinder 1.1
Created by Diandra Kubo
Modified by Artur Pimentel
Summer 2016 - University of Notre Dame
Fixing the locations
"""
import geopy
import requests
import sys
import os
import json
import numpy as np
import matplotlib.pyplot as plt

from geopy.geocoders import Nominatim
from datetime import datetime
from mpl_toolkits.basemap import Basemap, addcyclic

# -*- coding: utf-8 -*-
def utf8_deformat(s):
	return s.decode('utf-8')
	
def utf8_format(s):
	return s.encode('utf-8')
	
chaves = ['AIzaSyBGgkR72eR10uEvzkWd0NaVIbArwOkDXG4','AIzaSyAcs3lDxT7RTmPqWKxg3UOHrIN_6qtqznY','AIzaSyBNVMyZGopjQwLOzsYv1KQg5e-b4miUpbk','AIzaSyBbpVo-oMF_wW--OtEFrKmHMF9_2SpAOTY','AIzaSyD815WcRTNyYDjjAuyR2M-A8V5Y6luhbYY','AIzaSyD8L4UpLHf-NMhA2Jo_n3NkhC21yL3kyWo', 'AIzaSyDWuo5kSMRzbNyHq1QTlhYEJzpbTE2iP1w', 'AIzaSyDvVbcGu29IshR-Vka7nahs8A2oad8otcQ', 'AIzaSyD-H1LT7L1EL_v3O5t7kfDqKvACx5qqEzM']
chaves2 = ["AIzaSyCTQb2_S1MQY6yFb1m2dtAuKsZtuIXR4Ow", 'AIzaSyB0DgFNp-YV5gnGEUTzfH90D8AovObccpw', 'AIzaSyBHXc3oGv-cE0SMZgikc8cmi-GmutqyuDo', 'AIzaSyAEankRatzlFjpkOkeW5B8k8EhE2EpTsTk', 'AIzaSyDYQQmA1J3Z1sDMtjg4kMfMC_eh0E-KmaU', 'AIzaSyCtHdEMDTG0W9wX2IUjcuKwaH8QH8dnlmY']										 # chaves artur
chaves3 = ['AIzaSyA4Ml_XAihxv_7QzZlq6Vp69jOH0r-awV4', 'AIzaSyBZolYWTCHK9jP4taiBpIJ_YOFHOVSqZbo', 'AIzaSyBFXZDthlnlEPOHah4GCL_tyFfBGypZFG8', 'AIzaSyBXwDt3sxrU3z6O7bZJ_7YZjK5O_L6VvLc', 'AIzaSyC0RsnZ-P_lC_2sQS2NQBbIWPqshT-L-a4', 'AIzaSyDRb7TgxElQPF4lQsw-4hV2FGQDkxnHL6s', 'AIzaSyCx050b-9Ugb5KQKMn14iB0AnVTyHrTijQ']
chaves4 = [ 'AIzaSyC5bgRWej3l-3oDe9FfN3sOR0JWUMSSW1k','AIzaSyA5aE3iYUxi-rG9Beo1PfMCqMVRuVphnzk','AIzaSyAgyyDgIvwHRqBvZMQggeYw45_gem86WwQ','AIzaSyAtJlS4MTT2z4AfIGX3-7uknkh3TQdo-MQ','AIzaSyDxGlVGSe3JfQgdCdaop_o8xFnlgBO404Q','AIzaSyAjrS04JPEquPkuRH2RypMhmZpRWID_iUQ','AIzaSyDy-iAy32NNkxITioEqVmkens3hmvcJPhY','AIzaSyBeSecqw6_ioFd6nU-Hfw6whTZsOcrj-Z0','AIzaSyAyE6EYD97yqadYcE84TV2oQQh4286IKd0','AIzaSyCpbeg3bWmPmXll9Xfw51UuWZM-Ib9vTAk','AIzaSyCECMp52o3m_J5xLxpG1l1L0Fd_-yMZa5c','AIzaSyAZdLLa_mUCBft8z03ULJMikENwxpCTSz4','AIzaSyCvrLUaX-4pvu8CdZjpVhvgPJM9RqzpQm0','AIzaSyCeFaXpcEzLpK_km2uEt06sa1draAFXIiQ','AIzaSyBQa2baw4H_TZ0I2Uzr1OnO_R06BrcpUxI','AIzaSyDfhRNND59IvLZehbPQ8fhnF_3cDPggcy0','AIzaSyDGEY15Ruxrxbc51gE6O-B1enY314q1eRU','AIzaSyAb_4DqNgAJYq5L7B5GFdOpNp4eKmajgLU','AIzaSyCpbbIYM5y6Ug_OW_qL9gcNwGXH7vjCjtc','AIzaSyDeZ2xqs17Co8V88GNRVvp4OW4hB9BetH0', 'AIzaSyB_9GZouiLUULaVPjwxA-p2wrwrbOFEJ8E','AIzaSyAZJ5pb8p_CIpt6NqLk5iIHvXbfzj9HbXk','AIzaSyC-aoBMaPxNLbLJU9uRGD94tw9mUytbfwc','AIzaSyA25AaFKLzcKjS1ZKHDiRgw0RHoN8cYqdc','AIzaSyC5xeiQleZa05LXUVZUJh4jeGH1DRq_Jg4','AIzaSyDT0j9BX6j5XqDu_smTq9b2TFeRrC4ZcN8','AIzaSyDFXd4YUNTVYNTh5b4IY2GJMzAnWh1mNUw','AIzaSyCIlmRZRaWfIeW5VidMOQTrQ20GLBgeC38','AIzaSyC4R9ZeRP3GTz9n3VsGVGhsX1agJTt04Wg','AIzaSyAVg6C9D_GwsEpMQuE58vOPC8P4OcEc_fo','AIzaSyAr8DLcEpBgKQLhXZtOVrPudfW-pKKAMQ4','AIzaSyAFrHfrtRNjrWmFAVKptYBhf70gKjTkgos','AIzaSyCmrykaRI70Veft_jIv7jRPEfzQfsGlAwQ','AIzaSyBD8F3HfJeVu5bKsryBikB4snk6NS18JA0','AIzaSyA3FjP2r8xvACJLsFFe7uM2wrG9kNNxfiw','AIzaSyCrcJiNs7SCuTPrPrN9-wfqur0McNhvI5s','AIzaSyDlM6aODMJGGAs5OmQlV1WHLrh1eqISrgY','AIzaSyCndwIGj8tmXEdXGyvMhXvWWhh0iTiqius','AIzaSyBusLRnr_Bs_D2rX-vbdTaCA6TLh3WsjWk','AIzaSyB0ytCt3LgpTiwCDef5IVqLJ_bj-4BQnRI','AIzaSyAVndwjAvmadsgEqGcH-eljYMaheA4Mo44','AIzaSyBKpfaNWLkJheBYDEPxjXozhgW-CO78lZY','AIzaSyAAvK866b5PMwphUyClEQEKTW2uF6C5MFU','AIzaSyAq0lYHG88em9Td1x2ttYEWRzS4O5cl9t4','AIzaSyBcG3mRDvXgOfD-iHxH1reCXF5Isl3tPfU','AIzaSyCNheS7cGpAHCbOnVC8R9ZuF0l5qkdgWRM','AIzaSyA6w-FQh2GZtz9lTbwrvaepBZ3DeSP8tCk','AIzaSyAVsuSqic0UOWePXuzPGuGV88AySNSbgrQ','AIzaSyDpG36jce6AhdMINfkPA7T9G6BGSn4le0g','AIzaSyBLt1n186ACDI27tMeGCPoQz87jg4GEabw']
chaves5 = ['AIzaSyC5bgRWej3l-3oDe9FfN3sOR0JWUMSSW1k','AIzaSyBUU2cnAhQ0vNPqxNpNK_PNwKRW5kxwwbk','AIzaSyCTvyO5mhrq2D5HusdklD6V5hN8h7rMLlY','AIzaSyBdYkmkKUy69tTaNisJSKnzJomW88UbzQg','AIzaSyCbCGtQteybjOMkofe34aJcB82hX41blJw']
chaves6 = ['AIzaSyDvVbcGu29IshR-Vka7nahs8A2oad8otcQ','AIzaSyDFswxkgdoI79Wzn3Y9z5cdUruTUlNlkWM','AIzaSyBUU2cnAhQ0vNPqxNpNK_PNwKRW5kxwwbk','AIzaSyCTvyO5mhrq2D5HusdklD6V5hN8h7rMLlY','AIzaSyBdYkmkKUy69tTaNisJSKnzJomW88UbzQg','AIzaSyCbCGtQteybjOMkofe34aJcB82hX41blJw','AIzaSyBIWzPVxxFMc2NY_nuKbIjZOeQgNyTHx0E','AIzaSyC6OOoLGBS54llIHeaKcQgbOnwRfciAlCw','AIzaSyCIpflhVktxXzqjWnkIuLHRfWXTkZxUUWw','AIzaSyAkFWycnoF9iUcFtmY1nZ7Pjzc_aft1Y9g','AIzaSyD27vrGmBa9dOP03RwN0dBaAgf9G_jO4js','AIzaSyDyHrDIti5eZ9Elg3j11IGzGae2m6dEdmw','AIzaSyAdUMBs5iVddRnbDpGs8q0PyguW8EVVInw','AIzaSyD8z9RlOgmZCL-cmBxvnPtoBM0x3ErVlIU','AIzaSyBvThYRSoYOePJ_u3zc5ewWZeAQA9xaewY','AIzaSyAz3j1z7atvwiKo5TawNPTwfIszqsBRmCo','AIzaSyAOkIwVF1SWmt3oN3IKkakOFJgQ043Arck','AIzaSyChEHdQaB1TH7aOeng8Xj-O-aYhJpRyJMs','AIzaSyAcQS4dcelH0OiyMvc_MBrDwrU_c_M24qE','AIzaSyA56MU-IwXcSaxncvQlzCFxxaxj9Tyqk5g','AIzaSyA_0JYzDj4DWX-MTbVq_AL4gIJjmFLYzpo','AIzaSyAj2gtssE1AJSsxwuQUHNvxCRUt4wXPpW4','AIzaSyCAgOsBdlukg9AbvpJMAfh6W80xl5mV7-I']
chaves = list(set(chaves+chaves2+chaves3+chaves4+chaves5+chaves6))

chave_id=0
f = open('locations_newkeywords.txt','r')
locs = f.readlines()
f.close()
lats=[];lons=[];adds=[]
cont=0;cont2=0;ind=0
adds_existem=[]
data=[]

#f = open("cont.txt", 'r')
#ind = int(f.readline())
#f.close()

for j in xrange(ind, len(locs)):
	location = locs[j][:-1]
	sys.stdout.write("\n%d " % j)
	if (utf8_deformat(location) in tuple(adds_existem))==False:
		try:
			# Get raw information about a city
			response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?key=%s&address=%s' % (chaves[chave_id], location.replace(' ', '+'))) 
			resp_json_payload = response.json()
			# Append lat and long info in different arrays  
			lats.append(resp_json_payload['results'][0]['geometry']['location']['lat'])
			lons.append(resp_json_payload['results'][0]['geometry']['location']['lng'])
			adds.append(location)
			cont2+=1
		except Exception as e:
			print location, e.args[0]
			if resp_json_payload['status']==u'OVER_QUERY_LIMIT' or resp_json_payload['status']==u'REQUEST_DENIED':
				chave_id+=1
				j-=1
				print 'Changing key------------------------------------', chave_id
				if chave_id>(len(chaves)-1):
					print 'Acabaram as chaves'
					os.system("echo %d > cont.txt" % j)
					print "cont-----------", j
					f = open('addresses_newkeywords.txt', 'a')
					for i in xrange(len(lats)):
						f.write("%s,%s,\"%s\"\n" % (lats[i], lons[i], adds[i]))
					f.close()
					sys.exit(2)
				
			elif e.args[0]!='list index out of range' or resp_json_payload['status']!=u'ZERO_RESULTS':
				print resp_json_payload
				os.system("echo %d > cont.txt" % j)
				print "CONTADOR-----------", j
				f = open('addresses_newkeywords.txt', 'a')
				for i in xrange(len(lats)):
					f.write("%s,%s,\"%s\"\n" % (lats[i], lons[i], adds[i]))
				f.close()
				lats=[];lons=[];adds=[]
f = open('addresses_newkeywords.txt', 'a')
for i in xrange(len(lats)):
	f.write("%s,%s,\"%s\"\n" % (lats[i], lons[i], adds[i]))
f.close()


