#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Gter copyleft 
#Roberto Marzocchi

import sys,os

#import matplotlib
from matplotlib import pyplot as plt 
from PIL import Image, ImageDraw, ImageFont

# Connect to an existing database
import psycopg2
#sys.path.append(os.path.abspath("../../"))
from credenziali import *
conn = psycopg2.connect(host=ip, dbname=db, user=user, password=pwd, port=port)
#autocommit
conn.set_session(autocommit=True)
cur = conn.cursor()
cur2 = conn.cursor()


dirname=sys.path[0]
#print(dirname)
dirname2=os.path.join(dirname, '../media/grafici_p_t')
dirname2 = os.path.abspath(os.path.realpath(dirname2))


def crea_grafico(date, valore, titolo, nomefile, variabile):
    try:
        plt.title(titolo) 
        plt.xlabel("Date")
        plt.xticks(rotation=45)
        plt.ylabel(variabile) 
        plt.plot(date,valore)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.20)
        
        plt.savefig(nomefile,dpi=150, 
            optimize=True
        )
        plt.clf()
    except Exception as e:
        #print('entro qua')
        print(e)
        img = Image.new('RGB', (100, 30), color = (73, 109, 137))
        #fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 15)
        d = ImageDraw.Draw(img)
        d.text((10,10), "Hello world", fill=(255, 255, 0))
        img.save(nomefile)
        
        
query1="SELECT id_station, owner, \"use_P\", \"use_T\" FROM concerteaux.stations_p_t;"
#print(query1)
cur2.execute(query1)
x=cur2.fetchall()
#print(x)
for staz in x:
    id_station=staz[0]
    owner=staz[1]
    title = '{} ({})'.format(id_station,owner)
    print(title)
    print(staz[2])
    if staz[2]==True:
        jsonFile=os.path.join(dirname2, '{}_P.png'.format(staz[0]))
        query2="SELECT time, \"P\" FROM concerteaux.data_p_t WHERE id_station='{}' and time >  now() - interval '14 days';".format(staz[0])
        print(query2)
        cur2.execute(query2)
        p=cur2.fetchall()
        #print(x)
        time=[]
        pres=[]
        for pp in p:
            time.append(pp[0])
            pres.append(pp[1])
        print(time)
        print(pres)
        crea_grafico(time, pres, title, jsonFile, 'P[hPa]')
    if staz[3]==True:
        jsonFile=os.path.join(dirname2, '{}_T.png'.format(staz[0]))
        query2="SELECT time, \"T\" FROM concerteaux.data_p_t WHERE id_station='{}' and time >  now() - interval '14 days';".format(staz[0])
        print(query2)
        cur2.execute(query2)
        p=cur2.fetchall()
        #print(x)
        time=[]
        temp=[]
        for pp in p:
            time.append(pp[0])
            temp.append(pp[1])
        print(time)
        print(temp)
        crea_grafico(time, temp, title, jsonFile, 'T[°C]')
    