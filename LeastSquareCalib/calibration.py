import numpy as np
from numpy.linalg import lstsq

class SeriesTerm :
    
    def __init__( self, expression, safe = False ) :
        
        '''
        SeriesTerm( func )
        
        expression (str) : expression meant to be evaluated to define a function of an order integer i and a variable x.
        For instance, 'x**i' will be evaluated as 'lambda i, x : x**i'.
        
        safe (Boolean) : Ask before evaluating
        '''
        
        self.expression = expression
        
        if expression == 'polynomial' :
            self.func = lambda i, x : x**i
        
        else :
            
            if not safe :
                
                if input( 'Evaluate expression ' + expression + ' ?') in ['y', 'Y', ] :
                    safe = True                    
                    
            if safe :
                self.func = eval( 'lambda i, x :' + expression )
            
            else :
                print( 'Not evaluating expression.' )
                self.func = None

class Series :
    
    def __init__( self, term = None, coeffs = None ) :
        
        self.term = term
        self.coeffs = coeffs
    
    def to_dict( self ) :
        return dict( expression = self.term.expression, coeffs = self.coeffs )

    def from_dict( self, d, safe = False ) :
        
        self.coeffs = d['coeffs']
        self.term = SeriesTerm( d['expression'], safe = safe )
        
        return self
        

class CalibSeries:

    '''
    Series of series terms, for instance a polynomial.
    '''
    
    def __init__( self, *args ) :
        
        self.series = []
        
        self.append( *args )


    def append( self, *args ) :
        
        for series in args :
            self.series += [ series ]     
        

    def evaluate( self, x ) :

        y = x*0
   
        for series in self.series :
            
            for i, coeff in enumerate( series.coeffs ) :
                y += coeff*series.term.func( i, x ) 

        return y



    def to_dict( self ) :
        
        d = []
        
        for series in self.series :
            
            d += [ series.to_dict() ]
        
        return d


    
    def from_dict( self, d, safe = False, append = False ) :
        
        new_series = []
        
        for series in d :
            
            new_series += [ Series().from_dict( series, safe = safe ) ]
        
        if append :
            self.append( new_series )
        
        else :
            self.series = new_series
        
        return self
    
    
    def get_least_squares_matrix( self, x ) :
        
        A = []
        
        for series in self.series :
            
            for i, _ in enumerate( series.coeffs ) :
                
                A += [ series.term.func( i, x ) ]
        
        return np.array(A).T
 
 
    def fit_to_data( self, x, y ) :
 
        least_square_result = lstsq( self.get_least_squares_matrix( x ), y.T, rcond = None )
        fit = least_square_result[0].tolist()

        for series in self.series :
            n = len( series.coeffs )
            series.coeffs = fit[ :n ]
            fit = fit[n:]
 
        return least_square_result

##################
#
# Try it out
#
##################

if __name__ == '__main__' :
    
    # ~ p = SeriesTerm( 'x**i', safe = True )
    # ~ s = Series( p, [0, 0, 0])
    # ~ cs = CalibSeries( s )
    
    # ~ cs.from_dict( cs.to_dict(), safe = True )
  
    calib = CalibSeries().from_dict( [
        dict( expression = 'x**i', coeffs = [0]*2 ),
        dict( expression = 'sin( x*2*pi*( i + 1) )', coeffs = [0]*3 )
        ], safe = True )
    
    from pylab import *
    
    x = linspace(0,1,50)
    y = 5*x + sin(2*np.pi*x) + 0.3*rand(len(x))
    
    calib.fit_to_data( x, y )
    
    print(calib.to_dict())

    plot(x, y, '.')
    plot(x, calib.evaluate(x), '--')

    show()
