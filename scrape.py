from lxml import html
import requests
from tinydb import TinyDB,where

links = [
  'http://www.philzcoffee.com/Online-Store/Dark-Roast-Blends',
  'http://www.philzcoffee.com/Online-Store/Medium-Roast-Blends',
  'http://www.philzcoffee.com/Online-Store/Light-Roast-Blends',
  'http://www.philzcoffee.com/Online-Store/Specialty',
  'http://www.philzcoffee.com/Online-Store/Teas-Spices'
]
  #'''http://www.philzcoffee.com/Online-Store/Decaf','''
  #'''http://www.philzcoffee.com/Online-Store/Varietals','''

uniq_count = 0

def get_json(url):
  global uniq_count
  res = requests.get(url)
  tree = html.fromstring(res.text)
  ret = []
  name = tree.xpath("//div[@class='iteminfo']/h3/a/text()")
  des = tree.xpath("//div[@class='iteminfo']/text()")
  descrip = []
  for i in des:
    if len(i.strip()) > 10:
      descrip.append(i.strip())
  for i,j in zip(name,descrip):
    ret.append({"id":uniq_count,"name":i,"description":j})
    db = TinyDB('db/'+str(uniq_count)+'.json')
    uniq_count = uniq_count +1
  return ret

def get_all():
  db = TinyDB('db/coffee.json')
  for i in links:
    print i
    s = i.split('/')
    flav = s[len(s)-1]
    temp = get_json(i)
    print flav
    print temp
    for i in temp:
      db.insert(i)

get_all()



