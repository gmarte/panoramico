import csv
from itertools import islice
import numpy as np
import glob
import time
from datetime import date
import codecs
import pandas as pd

array = list()
checktiendas = ['807','B551']
counter = 0
first = 0
tnd = list()
newDF = pd.DataFrame()

def tiendas():
	with open(r'C:\Users\gmarte\Documents\Ponches\LSTM\tiendas.txt','rb') as tdrel:	
		for t in csv.reader(tdrel, dialect="excel-tab"):
			tnd.append(t)
	return;

def ini_export():	
	global allfiles
	allfiles = glob.glob("C:\Users\gmarte\Documents\Ponches\LSTM\*.XLS")		
	tiendas()
	return;

def search_tienda( tnd_name ):
	for t in tnd:
		if tnd_name in t:
			return t[1]
	return;
ini_export()

with open('3months.csv', 'wb') as csvfile:    
	spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"',skipinitialspace = True, quoting=csv.QUOTE_MINIMAL)	
	for all in allfiles:
	#with open("C:\Users\gmarte\Documents\Ponches\LSTM\ponches20161213.XLS",'rb') as tsv:		
		with open(all,'rb') as tsv:
			#print(all)
			while counter < 5:
				next(tsv)
				counter += 1			
			for line in csv.reader(tsv, dialect="excel-tab"): #You can also use delimiter="\t" rather than giving a dialect.		
				if first == 0:				
					global date_data
					today = date.today()
					first = 1
					a = line					
					date_data = date( today.year, int(a[4][6:-2]), int(a[4][3:-5]))					
				elif len(line) > 0:		
					a = line
					#print(search_tienda(a[3]))
					try:
						a_parse =  [a[1],a[2],a[3],search_tienda(a[3]),a[4],date_data]
					except:
						continue
					#if a_parse[3] in checktiendas:
					array.append(a_parse)
			array = sorted(array,key=lambda l:l[2])
			spamwriter.writerows(array)			
			pf = pd.DataFrame(array)
			#pf = pf.transpose()
			cols = ['code','name','tnd','div','hora','date']
			try:
				pf.columns = cols
			except:
				continue
			newDF = newDF.append(pf,ignore_index = True)			
			counter = 0
			first = 0
			del array[:]
#print newDF.groupby('div')['div'].count()
tnd_results = newDF.groupby('div')['div'].count()
print tnd_results
tnd_results.to_csv('tiendas.csv')
#print newDF.groupby(['div','code'])['code'].count() % 2
group = newDF.groupby(['div','code'])['code'].count() % 2
impares = group.groupby(level=0).sum()
impares.to_csv('impares.csv')
print impares
aggregations = {
    'code':'count'	
}
#print newDF.groupby('div')['div'].count().agg(aggregations)
#print newDF.groupby('tnd').std()