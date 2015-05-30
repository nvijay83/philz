import TinyDbCore
import pdb

if __name__ == '__main__':
   TinyDbCore.cleanup( 'Arabica' )
   TinyDbCore.insertEntry( 'Arabica', 1 )
   TinyDbCore.insertEntry( 'Arabica', 1, 5 )
   assert len( TinyDbCore.getReviews( 'Arabica' ) ) == 0
   assert len( TinyDbCore.getDb( 'Arabica' ) ) == 1
   TinyDbCore.insertEntry( 'Arabica', 1, 5, 'Hello' )
   assert len( TinyDbCore.getDb( 'Arabica' ) ) == 1
   assert len( TinyDbCore.getReviews( 'Arabica' ) ) == 1
   TinyDbCore.insertEntry( 'Arabica', 2, 3, 'Hello' )
   assert len( TinyDbCore.getDb( 'Arabica' ) ) == 2
   assert TinyDbCore.getRatings( 'Arabica' ) == 4
   assert TinyDbCore.getStarRatings( 'Arabica' ) == [ 1, 1, 1, 1, 0 ]
   reviews = TinyDbCore.getReviews( 'Arabica' )
   assert set( [ 1, 2 ] ) == set( reviews.keys() )

   TinyDbCore.cleanup( 'Arabica' )

