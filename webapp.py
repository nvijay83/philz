from tinydb import TinyDB
from flask import Flask, request, render_template, redirect, url_for, abort,flash, jsonify,send_from_directory
from  TinyDbCore import *

# noinspection PyUnresolvedReferences
#from flask.ext.login import LoginManager, login_user
# noinspection PyUnresolvedReferences
#from flask.ext.security import login_required

app = Flask(__name__, static_folder='static', template_folder='templates')
#app.config.from_envvar('WEBAPP_SETTINGS')
'''
@app.route('/live',methods=['GET','POST'])
def live():
  racers, finished = Racer.get_live_scoreboard()
  sorted_racers = [racers[i] for i in racers]
  if not finished:
    sorted_racers.sort(key=lambda k: k['kart'])
  else:
    sorted_racers.sort(key=lambda k: k['nickname'])
  return render_template('live.html', racers=sorted_racers, finished=finished)


@app.route('/create', methods=['GET','POST'])
def create():
  init_fuel = int(request.form['init_fuel'])
  max_fuel = int(request.form['max_fuel'])
  races = int(request.form['races'])
  print request.form['track']
  track_id = int(request.form['track'])
  create_race(init_fuel, max_fuel, races, track_id)
  init_race()
  return render_template('admin.html')

@app.route('/fix', methods=['GET','POST'])
def fix():
  cur_race = Race.get_in_progress_race()
  if cur_race is  None:
    return "No race in progress"
  else:
    racers = Racer.get_racers(cur_race)
  racers.sort(key=lambda k:k['kart'])
  return render_template("fix.html", update_string="", racers=racers)

@app.route('/correction',methods=['POST'])
def correction():
  cust_id = int(request.form['cust_id'])
  fuel = int(request.form['fuel'])
  update_string="updated: cust_id is %d, fuel is %d"%(cust_id,fuel)
  print update_string
  cur_race = Race.get_in_progress_race()
  add_fuel_correction(cust_id, fuel)
  if cur_race is  None:
    return "No race in progress"
  else:
    racers = Racer.get_racers(cur_race)
  racers.sort(key=lambda k:k['kart'])
  return render_template("fix.html",update_string=update_string, racers=racers)

@app.route('/up',methods=['GET','POST'])
def up():
  cur_race = Race.get_in_progress_race()

  if cur_race is  None:
    return "No race in progress"
  else:
    racers = Racer.get_racers(cur_race)
  racers.sort(key=lambda k:k['kart'])
  return render_template("up.html", racers=racers)

@app.route('/update', methods=['GET','POST'])
def update():
  cust_id = int(request.form['cust_id'])
  print request.form['fuel']
  fuel = int(request.form['fuel'])
  add_fuel(cust_id, fuel)
  cur_race = Race.get_in_progress_race()
  if cur_race is  None:
    return "No race in progress"
  else:
    racers = Racer.get_racers(cur_race)
  racers.sort(key=lambda k:k['kart'])
  print "added cust_id %d, fuel %s"%(cust_id,fuel)
  return render_template("up.html", racers=racers)

@app.route('/cr')
def cr():
  tracks = ClubSpeedApi.get_tracks_api()
  return render_template("index.html",tracks=tracks)
'''

def get_coffees(active):
  name = ''
  name_link = ''
  nav_links = []
  description = ''
  db = TinyDB('db/coffee.json')
  coffee = db.all()
  count = 0
  coffee_id = 0
  for i in coffee:
    if active == -1 and count == 0:
      nav_links.append(("/"+str(i['id']),"active",i['name']))
      name = i['name']
      description = i['description']
      coffee_id = i['id']
    elif active == -1 and count > 0:
      nav_links.append(("/"+str(i['id']),"",i['name']))
    elif active == i['id']:
      nav_links.append(("/"+str(i['id']),"active",i['name']))
      name = i['name']
      description = i['description']
      coffee_id = i['id']
    else:
      nav_links.append(("/"+str(i['id']),"",i['name']))
    name_link = '/'+str(i['id'])
    count = count+1
  for i in nav_links:
    print i
  print name
  print name_link

  return nav_links, name, name_link, description, coffee_id


@app.route('/review', methods=['GET', 'POST'])
def review():
  print "in review"
  print request.form['comment']
  print int(request.form['coffee'])
  print int(request.form['rating'])
  name = 'Anonymous'
  id = int(request.form['coffee'])
  rating = int(request.form['rating'])
  comment = request.form['comment']
  if rating > 0:
    insertEntry('db/'+str(id)+'.json',name,rating,comment)
  return spec_coffee(id)

@app.route('/<id>')
def spec_coffee(id):
  print id
  nav_links, name, name_link, description,coffee_id = get_coffees(int(id))
  db = 'db/'+str(id)+'.json'
  reviews = getReviews(db)
  ratings = getStarRatings(db)
  ratings_float = getRatings(db)
  total_reviews = len(reviews)

  return render_template('index.html', nav_links=nav_links, name=name, name_link=name_link, description=description,
                         reviews=reviews, ratings=ratings, ratings_float=ratings_float,total_reviews=total_reviews,
                         coffee_id = coffee_id)

@app.route('/')
def index():
  nav_links, name, name_link,description,coffee_id = get_coffees(0)
  db = 'db/0.json'
  reviews = getReviews(db)
  print reviews
  ratings = getStarRatings(db)
  ratings_float = getRatings(db)
  total_reviews = len(reviews)
  return render_template('index.html', nav_links=nav_links, name=name, name_link=name_link, description = description,
                         reviews=reviews, ratings=ratings, ratings_float=ratings_float,total_reviews=total_reviews,
                         coffee_id=coffee_id)

'''
@app.route('/maxfuel', methods=['GET','POST'])
def max_fuel():
  print "here"
  print ""
  cust_id = int(request.form['cust_id'])
  print cust_id
  i,m,a,b = get_config()
  laps_empty = Racer.get_laps_empty(cust_id)
  cur_race = Race.get_in_progress_race()
  if cur_race is not None:
    racer, created = Racer.get_racer(cust_id,None, None, None, None, None, cur_race)
    max_fuel = m - (laps_empty['laps_empty'] - racer.laps)
    return str(max_fuel)
  else:
    return str(0)

'''
'''
import sys
sys.path.append("unit/")
from fake_race import *
test1()
'''

if __name__ == "__main__":
    # TODO: move to config
    app.run(host="0.0.0.0", port=5000, threaded=False,debug=True)

