import pandas as pd
import googlemaps
import psycopg2 as pg2
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log2gm.log',
                    filemode='w')

d=pd.read_csv('london_d0.csv',sep='\t')
gmaps = googlemaps.Client(key='AIzaSyCeWemE0s3KVIITCX-XmJinQA3Nt9rQOTI')
def latlng(x):
    geocode_result=gmaps.geocode(x)
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    return [lat,lng]



page = 0
for i in range(d.shape[0]):
    try:
        attraction = d.iloc[i].attraction
        logging.info('%s', attraction)
        ll = latlng(d.iloc[i].address)
        page = page + 1
        print page
    except:
        ll = ['missing','missing']
        logging.exception("Fail to requestion: %s, page: %d", attraction, page)
    
    try:
        conn = pg2.connect(host="tourlondon.cd6otpnh2nbb.us-east-2.rds.amazonaws.com",database="london", user="zty", password="54321zty",connect_timeout=10)
        cur = conn.cursor()
        sql = """INSERT INTO address0(attraction, latitude, longitude) VALUES(%s, %s, %s);"""
        cur.execute(sql, (attraction, ll[0], ll[1]))
        conn.commit()
    except:
        logging.exception('Data base (dest) error on page %d: %s', page, a)