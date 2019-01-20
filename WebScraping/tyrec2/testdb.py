from bs4 import BeautifulSoup
import psycopg2 as pg2
import logging
import requests
import time
import csv
with open('att_url.csv', 'rb') as csvfile:
    u = list(csv.reader(csvfile))

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log1.log',
                    filemode='w')

page = 0
for x in u[0:3]:
    page = page + 1
    try:
        page_recq = requests.get('https://www.tripadvisor.com' + x[0], timeout=5)
        time.sleep(1)
    except:
        logging.exception("Fail to requestion link: %, page: %d", x[0], page)  
    soup = BeautifulSoup(page_recq.content, "html.parser")
    
#=====================================================================================================================
# Attraction name
#=====================================================================================================================
    try:
        attraction = soup.find('h1', {'id':'HEADING'}).getText()
        logging.info('page %d: %s', page, attraction)
    except:
        continue
#=====================================================================================================================
# Popularity ranking
#=====================================================================================================================
    try:
        ranking = soup.find('b', {'class':''}).getText()
    except:
        ranking = 'missing'
#=====================================================================================================================
# Rating
#=====================================================================================================================
    try:
        rating = soup.find('span', {'class':'overallRating'}).getText()
    except:
        rating = 'missing'
#=====================================================================================================================
# Number of reviews
#=====================================================================================================================
    try:
        nreview = soup.find('a', {'href':'#REVIEWS'}).getText().split()[0]
    except:
        nreview = 'missing'
#=====================================================================================================================
# Address
#=====================================================================================================================
    try:
        address = soup.find('div', {'class':'detail_section address'}).getText()
    except:
        address = 'missing'
#=====================================================================================================================
# Street
#=====================================================================================================================
    try:
        street = soup.find('span', {'class':'street-address'}).getText()
    except:
        street = 'missing' 
#=====================================================================================================================
# Locality
#=====================================================================================================================
    try:
        locality = soup.find('span', {'class':'locality'}).getText()
    except:
        locality = 'missing' 
#=====================================================================================================================
# Category
#=====================================================================================================================
    try:
        cate = soup.find('div', {'class':'detail'}).getText()
    except:
        cate = 'missing'
#=====================================================================================================================
# Phone
#=====================================================================================================================
    try:
        ph = soup.find('div', {'class':'detail_section phone'}).getText()
    except:
        ph = 'missing'
#=====================================================================================================================
# Visit Duration
#=====================================================================================================================
    try:
        duration = soup.find('div', {'class':'detail_section duration'}).getText()
    except:
        duration = 'missing'
#=====================================================================================================================
# Open Hours
#=====================================================================================================================
    try:
        hrs = soup.find('div', {'class':'detail_section hours'}).getText()
    except:
        hrs = 'missing'
#=====================================================================================================================
# Neighborhood
#=====================================================================================================================
    try:
        neighborhood = soup.find('div', {'class':'detail_section neighborhood'}).getText()
    except:
        neighborhood = 'missing'
#=====================================================================================================================
# Description
#=====================================================================================================================
    try:
        desc = soup.find('div', {'class':'modal-card-body'}).getText()
    except:
        desc = 'missing'
#=====================================================================================================================
# Tags
#=====================================================================================================================
    try:
        tags0 = soup.find_all('div', {'class':'tagWord'})
        tag = []
        for t in tags0:
            tag.append(t.getText()[1:-1])
        tags = '; '.join(tag)
    except:
        tags = 'missing'
#=====================================================================================================================
# Languages
#=====================================================================================================================
    try:
        langs = soup.find('ul', {'class':'langs'})
        l0 = langs.find_all('label', {'class':'filterLabel'})
        lang = []
        for l in l0:
            lang.append(l.getText()) 
        languages = '; '.join(lang)
    except:
        languages = 'missing'
        
#=====================================================================================================================
# Save to database
#=====================================================================================================================
    conn = pg2.connect(host="test.cd6otpnh2nbb.us-east-2.rds.amazonaws.com",
                       database="test", 
                       user="test", password="testtest")
    cur = conn.cursor()
    sql = """INSERT INTO a1(attraction, ranking, rating, review_num, address, street, locality, category, phone, duration, hours, neighborhood, description, tags, languages) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    cur.execute(sql, (attraction, ranking, rating, nreview, address, street, locality, cate, ph, duration, hrs, neighborhood, desc, tags, languages))
    conn.commit()
#=====================================================================================================================
# Reviews
#=====================================================================================================================
    r0 = soup.find_all('div', {'class':'reviewSelector'})
    for r in r0:

        try:
            user = r.find('div', {'class':'username mo'}).getText()
        except:
            continue

    #     
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

        try:
            user_location = r.find('div', {'class':'location'}).getText()
        except:
            user_location = 'missing'

        try:
            review_date = r.find('span', {'class':'ratingDate relativeDate'})['title']
        except:
            review_date = 'missing'

        try:
            viamobile = r.find('span', {'class':'viaMobile'}).getText()
        except:
            viamobile = 'no'

        try:
            quote = r.find('span', {'class':'noQuotes'}).getText()
        except:
            quote = 'missing'

        try:
            review = r.find('p', {'class':'partial_entry'}).getText()
        except:
            review = 'missing'

        sql = """INSERT INTO r2(userID, attraction, user_location, user_Contributions, user_UpVotes, viaMobile, review_quote, review_content) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"""
        cur.execute(sql, (user, attraction, user_location, user_Contributions, user_UpVotes, viamobile, quote, review))
        conn.commit()