#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Gter copyleft 
#Roberto Marzocchi

import sys,os

import shutil
import urllib.request as request
from contextlib import closing

import csv

# Connect to an existing database
import psycopg2
#sys.path.append(os.path.abspath("../../"))
from credenziali import *
conn = psycopg2.connect(host=ip, dbname=db, user=user, password=pwd, port=port)
#autocommit
conn.set_session(autocommit=True)
cur = conn.cursor()
cur2 = conn.cursor()


ftp_path='ftp://omiv.unice.fr/bendola/'
file_prefix='weewxPosteriori_CONCERTEAUX'
#file='weewxPosteriori_CONCERTEAUX-B1-ARCHIVE.csv'

check_archive=0 # usare 1 per importare i dati storici (ARCHIVE.csv)
stazioni=['B1','B4']



def calcola_pmare(press, elev):
    p_mare=[]
    or_disc= 1013.25* (-1 +(1 + 0.0000226*elev)**(-5.25593))
    for i in range(len(press)):
        if press[i] == '99999':
            pm = 99999
            p_mare.append(pm)
        else:
            pm = float(press[i])- or_disc
            #print(pm)
            p_mare.append(pm)
    return p_mare




for staz in stazioni:
    print('Sto leggendo i dati della stazione {}'.format(staz))
    query1="SELECT ele FROM concerteaux.stations_p_t WHERE id_station='{}'".format(staz)
    cur2.execute(query1)
    x=cur2.fetchall()
    #print(x)
    for el in x:
        ele=el[0]
    print(ele)
    #exit()
    if check_archive==1:
        file='{}-{}-ARCHIVE.csv'.format(file_prefix,staz)
    else:
        file='{}-{}.csv'.format(file_prefix,staz)
    with closing(request.urlopen('{}{}'.format(ftp_path,file))) as r:
        with open(os.path.join(sys.path[0],file), 'wb') as f:
            shutil.copyfileobj(r, f)
        with open(os.path.join(sys.path[0],file), mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            #DT=[]
            #TT=[]
            #PP=[]
            #PSPS=[]
            
            for row in csv_reader:
                query2="INSERT INTO concerteaux.data_p_t(id_station, time"
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                dt=row["dateTime"] 
                if row["TempNow"] :
                    T=float(row["TempNow"])
                    query2='{}, "T" '.format(query2)
                #else:
                #    T=None
                if row["barometerNow"]:
                    P=float(row["barometerNow"])
                    P_sea_level=P-(1013.25* (-1 +(1 + 0.0000226*ele)**(-5.25593)))
                    query2='{}, "P", "P_mare" '.format(query2)
                #else:
                #    P=None
                #    P_sea_level=None
                #DT.append(dt)
                #TT.append(T)
                #PP.append(P)
                #PSPS.append(P_sea_level)
               
                query2="{}) VALUES ('{}', '{}'".format(query2,staz,dt)
                if row["TempNow"] :
                    query2='{}, {} '.format(query2,T)
                if row["barometerNow"] :
                    query2='{}, {},{} '.format(query2,P, P_sea_level)
                query2='{})'.format(query2)
                #print(query2)
                try:
                    cur2.execute(query2)
                except Exception as e:
                    #print ("violazione chiave primaria", query2)
                    print(e)
                    print("The failed query is ",query2)
                line_count += 1
            print(f'Processed {line_count} lines.')
            #dataText10=','.join(cur.mogrify('(\'%s\',\'%s\',%s,%s,%s)'%(staz,DT[j],TT[j],PP[j],PSPS[j])) for j in range(0,line_count))
	
	        #cur.execute("INSERT INTO concerteaux.data_p_t (id_station, time, \"T\", \"P\", \"P_mare\") VALUES " + dataText10 + ";" )

