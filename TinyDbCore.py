from tinydb import TinyDB, where
import pdb
import datetime
import random

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
   dateTime = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
   entry = \
         {
            'customer_id' : customer_id,
            'rating' : rating,
            'stars' : starRating( rating ),
            'comment' : comment,
            'date' : dateTime
         }
   if not contains( db, customer_id ):
      db.insert( entry )
   else:
      db.update( entry, where( 'customer_id' ) == customer_id )

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
   for entry in db.all():
      if entry[ 'comment' ]:
         reviews.append({'customer_id':entry[ 'customer_id' ],
                        'comment':entry[ 'comment' ],
                        'stars':entry[ 'stars' ],
                        'date':entry[ 'date' ]})
   return reviews

def cleanup( dbName ):
   db = TinyDB( dbName )
   db.purge()

def getDb( dbName ):
   return TinyDB( dbName )

# Test code Apis to populate some random entries
def getRandomComment():
   return 'random-comment-%d' % random.randint( 1, 100 )

def populateRandomData( dbName ):
   customer_name = [ 'foo-%d' % i for i in range( 10 ) ]
   entries = {}
   for customer_id in customer_name:
      comment = getRandomComment()
      rating = random.randint( 0, 5 )
      insertEntry( dbName, customer_id, rating, comment )

