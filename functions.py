def array_merge( first_array , second_array ):
     if isinstance( first_array , list) and isinstance( second_array , list ):
      return first_array + second_array
     #takes the new product add to the existing and merge to have one array with two products
     elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
      return dict( list( first_array.items() ) + list( second_array.items() ) )
     elif isinstance( first_array , set ) and isinstance( second_array , set ):
      return first_array.union( second_array )
     return False
def check_customer():
    if 'email' in session:
        return True
    else:
        return False                                            