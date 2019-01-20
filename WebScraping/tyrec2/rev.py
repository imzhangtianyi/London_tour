from bs4 import BeautifulSoup
import psycopg2 as pg2
import logging
import requests
import time
import csv
with open('rsites.csv', 'rb') as csvfile:
    u = list(csv.reader(csvfile))

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log1.log',
                    filemode='w')

page = 0
for x in u:
    for i in range(10,int(x[2])+1,10):
        page = page+1
        try:
            url = 'https://www.tripadvisor.com' + x[1].replace('-Reviews-','-Reviews-or{}-'.format(i))
            page_recq = requests.get(url, timeout=200)
            time.sleep(2)
            logging.info('%s', url)
            print page
        except:
            logging.exception("Fail to request link: %", x[1])
            break
        soup = BeautifulSoup(page_recq.content, "html.parser")
#=====================================================================================================================
# Reviews
#=====================================================================================================================
        r0 = soup.find_all('div', {'class':'reviewSelector'})
        for r in r0:
#=====================================================================================================================
# User name
#=====================================================================================================================
            try:
                user = r.find('div', {'class':'username mo'}).getText()
            except:
                logging.warning("Fail to aquire userid: site: %s", x[0])
                continue

#=====================================================================================================================
# User contributions and up votes
#=====================================================================================================================
            try:
                cu = r.find('div', {'class':'memberBadgingNoText'})
                cuv = cu.find_all('span', {'class':'badgetext'})
                user_Contributions = cuv[0].getText()
            except:
                user_Contributions = 0
                user_UpVotes = 0
            try:
                user_UpVotes = cuv[1].getText()
            except:
                user_UpVotes = 0
#=====================================================================================================================
# User location
#=====================================================================================================================
            try:
                user_location = r.find('div', {'class':'location'}).getText()
            except:
                user_location = 'missing'
#=====================================================================================================================
# Rating
#=====================================================================================================================
            try:
                user_rating = r.find('div', {'class':'ratingInfo'}).next['class'][1][-2:]
            except:
                user_rating = 'missing'
#=====================================================================================================================
# Review date
#=====================================================================================================================
            try:
                review_date = r.find('span', {'class':'ratingDate relativeDate'})['title']
            except:
                review_date = 'missing'
#=====================================================================================================================
# Mobile?
#=====================================================================================================================
            try:
                viamobile = r.find('span', {'class':'viaMobile'}).getText()
            except:
                viamobile = 'no'
#=====================================================================================================================
# Review quote
#=====================================================================================================================
            try:
                quote = r.find('span', {'class':'noQuotes'}).getText()
            except:
                quote = 'missing'

            try:
                review = r.find('p', {'class':'partial_entry'}).getText()
            except:
                review = 'missing'

            try:
                rlink = r.find('span', {'class':'noQuotes'}).previous['href']
            except:
                rlink = 'missing'
#=====================================================================================================================
# Save to database
#=====================================================================================================================
            try:
                conn = pg2.connect(host="tourlondon.cd6otpnh2nbb.us-east-2.rds.amazonaws.com",database="london", user="zty", password="54321zty",connect_timeout=10)
                cur = conn.cursor()
                sql = """INSERT INTO reviews0(userID, attraction, user_rating, user_location, user_Contributions, user_UpVotes, viaMobile, review_quote, review_content, reviewlink) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
                cur.execute(sql, (user, x[0], user_rating, user_location, user_Contributions, user_UpVotes, viamobile, quote, review, rlink))
                conn.commit()
            except:
                logging.exception('Database error: %s', url)
