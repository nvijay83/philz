from tinydb import TinyDB, where
import pdb
import datetime
import random
import time

# Define APIs for callers to insert, query and update
# Json/python dict
'''
Table per item where item == 'Ether' or .. some other type
{
   'customer_id' : id of the customer
   'ratings' : dict of rating with customer-id to int Eg: 1 - 5
   'stars' : list of boolean
   'dateTime' : 'Date/ time when the query was added
   'comments' : 'text' Eg: coffee is great! < attaches user-id >
}
'''

NUM_STARS = 5

def contains( db, customer_id ):
   for entry in db.all():
      if entry[ 'customer_id' ] == customer_id:
         return True
   return False

def starRating( rating ):
   result = [ 0 ] * NUM_STARS
   if not rating:
      return result

   for i in range( rating ):
      result[ i ] = 1
   return result

# Inserts the customer feedback/rating into the db.table_name == item
def insertEntry( dbName, customer_id, rating=None, comment=None ):
   db = TinyDB( dbName )
   #dateTime = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
   entry = \
         {
            'customer_id' : customer_id,
            'rating' : rating,
            'stars' : starRating( rating ),
            'comment' : comment,
            'date' : time.time()
         }
   #if not contains( db, customer_id ):
   db.insert( entry )
   #else:
    #  db.update( entry, where( 'customer_id' ) == customer_id )

# returns Average rating and return a star rating
def getRatings( dbName ):
   db = getDb( dbName )
   if len( db ) == 0:
      return 0

   totalRatings = 0
   for entry in db.all():
      totalRatings += entry[ 'rating' ]

   return totalRatings / len( db.all() )

def getStarRatings( dbName ):
   return starRating( getRatings( dbName ) )

def getReviews( dbName ):
   db = getDb( dbName )
   reviews = []
   entries = db.all()
   entries.sort(key=lambda k: k['date'],reverse=True)
   for entry in entries:
      if entry[ 'comment' ]:
         reviews.append({'customer_id':entry[ 'customer_id' ],
                        'comment':entry[ 'comment' ],
                        'stars':entry[ 'stars' ],
                        'date':datetime.datetime.fromtimestamp(entry['date']).strftime("%I:%M%p on %B %d, %Y")})
   return reviews

def cleanup( dbName ):
   db = TinyDB( dbName )
   db.purge()

def getDb( dbName ):
   return TinyDB( dbName )

# Test code Apis to populate some random entries
def getRandomComment():
   return 'random-comment-%d' % random.randint( 1, 100 )


names = ['Vijay', 'John', 'Jeff', 'Anonymous','Anderson', 'Willy', 'Miller', 'Moore', 'Einstein', 'Young', 'Baker',
         'king', 'Phillips', 'Turner', 'Mary', 'Patricia', 'Linda', 'Donna', 'Lily', 'Sarah', 'Ashley', 'Sharon', 'Betty',
         'Deborah', 'Steven', 'Susan', 'barbara', 'Carol', 'Michelle', 'Ram', 'Nathan', 'Maria', 'Edward', 'Kartik', 'Lee',
         'Yang', 'Andrew', 'William', 'Sandy', 'Sandra', 'Laura', 'Brian', 'Le', 'Chang', 'Thomas', 'Rita', 'Mark']

comments = ['Nice flavor',
            'I love this coffee',
            'Amazing after taste',
            'Too strong',
            'One of my fav coffees',
            'Baristas are really nice at Philz',
            'This is how I start my day!',
            'This is probably the best coffee! Give it a try']

prob = [1,2,2,3,3,3,4,4,4,4,5,5,5,5,5]

def populateRandomData( dbName ):
   global names
   global comments
   global prob
   for j in range(0,random.randint(0,10)):
     i = random.randint(0,len(names)-1)
     customer_name = names[i]
     i = random.randint(0,len(comments)-1)
     comment = comments[i]
     i = random.randint(0,len(prob)-1)
     rating = prob[i]
     insertEntry(dbName, customer_name, rating, comment)

