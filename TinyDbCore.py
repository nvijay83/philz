from tinydb import TinyDB, where
import pdb

# Define APIs for callers to insert, query and update
# Json/python dict
'''
Table per item where item == 'Ether' or .. some other type
{
   'customer_id' : id of the customer
   'ratings' : dict of rating with customer-id to int Eg: 1 - 5
   'comments' : 'text' Eg: coffee is great! < attaches user-id >
}
'''

def contains( db, customer_id ):
   for entry in db.all():
      if entry[ 'customer_id' ] == customer_id:
         return True
   return False

# Inserts the customer feedback/rating into the db.table_name == item
def insertEntry( dbName, customer_id, rating=None, comment=None ):
   db = TinyDB( dbName )
   entry = \
         {
            'customer_id' : customer_id,
            'rating' : rating,
            'comment' : comment
         }
   if not contains( db, customer_id ):
      db.insert( entry )
   else:
      db.update( entry, where( 'customer_id' ) == customer_id )

def cleanup( dbName ):
   db = TinyDB( dbName )
   db.purge()

def getDb( dbName ):
   return TinyDB( dbName )

if __name__ == '__main__':
   cleanup( 'Arabica' )
   insertEntry( 'Arabica', 1 )
   insertEntry( 'Arabica', 1, 5 )
   insertEntry( 'Arabica', 1, 5, "Hello" )
   pdb.set_trace()
