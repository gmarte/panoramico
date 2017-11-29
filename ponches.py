import csv
from itertools import islice
import numpy as np
import glob
import matplotlib.pyplot as plt
from matplotlib import style
import time
from datetime import date,timedelta
import codecs
import pandas as pd
style.use('ggplot')

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
	allfiles = glob.glob("files\*.XLS")
	#allfiles = glob.glob("*.XLS")		
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
newDF.index=newDF['date']
#mask = (newDF['date'] ==  str(date.today()))
#newDF.loc[mask]
yesterday = date.today() - timedelta(days=1)
tnd_results = newDF[(newDF.date == yesterday )].groupby('div')['div'].size().reset_index(name='count')
g2 = newDF.groupby(['date','div'])['code'].size().reset_index(name='count')
g3 = g2.groupby('div')['count'].mean().reset_index(name='mean')
g4 = g2.groupby('div')['count'].std().reset_index(name='std')
#tnd_results['avg'] = newDF[(newDF.date == yesterday )].groupby('div')['div'].agg('count').mean()
g3.set_index(['div'],inplace=True)
g4.set_index(['div'],inplace=True)
tnd_results.set_index(['div'],inplace=True)



#tnd_results.to_csv('tiendas.csv')
#print newDF.groupby(['div','code'])['code'].count() % 2
group = newDF[(newDF.date == yesterday )].groupby(['div','code'])['code'].count() % 2
impares = group.groupby(level=0).sum().reset_index(name='impares')
impares.set_index(['div'],inplace=True)
#impares.to_csv('impares.csv')
gt_ponches = pd.concat([tnd_results,g3,g4,impares],axis = 1)
gt_ponches['diff'] = gt_ponches['count'] - ( gt_ponches['mean'] - gt_ponches['std']/2 )
gt_ponches.to_csv('ponches.csv')
print(gt_ponches)
gt_ponches.drop(gt_ponches[gt_ponches['diff'] > 0].index, inplace=True) 



#### PLOT #####

N = len(gt_ponches.index)
ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence
xtra_space = 0.05
p1 = plt.bar(ind, gt_ponches['count'], width, color='orange', yerr=gt_ponches['impares'])
p2 = plt.bar(ind + width + xtra_space, gt_ponches['mean'], width, color='g', yerr=gt_ponches['std'])

plt.ylabel('Cantidades')
plt.title('Ponches / Imparidades')
plt.xticks( (ind+ width/2 + xtra_space), gt_ponches.index)
plt.yticks(np.arange(0, 600, 20))
plt.legend((p1[0], p2[0]), ('Ponches/Impares', 'Promedio/STDEV'))

plt.show()

aggregations = {
    'code':'count'	
}
#print newDF.groupby('div')['div'].count().agg(aggregations)
#print newDF.groupby('tnd').std()