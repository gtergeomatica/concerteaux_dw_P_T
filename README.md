# concerteaux_dw_P_T
Download data Pressure and Temperature from different source of data (Concerteaux project)

All the script require a credenziali.py script 

```
#credenziali DB 
ip='XXX.XXX.X.XXX' 
db='dbname'
user='user_name'
pwd='pwd'
port='XXXX' # e.g. standard port 5432
```


Actually we download data from:

* *cnrs_download.py*: public ftp of CNRS
* *arpal_download.py*: public WS OMIRL of Arpa Liguria using the followig repo: https://github.com/gtergeomatica/omirl_data_ingestion


Finally the script *crea_grafici.py* create the plot using the python library matplotlib (the path are actually configured for our gishosting repository)

Scripts  are sheduled on the server crontab

