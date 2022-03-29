from pylab import *

import sys
sys.path.append('./../')

figures_directory = './../figures/'


from LeastSquareCalib import CalibSeries

x = linspace(0,1,50)
y = 5*x + 0.5*sin(2*pi*x) + 0.5*rand(len(x))
plot(x, y, '.', label = 'data')

calib = CalibSeries().from_dict( [
    dict( expression = 'x**i', coeffs = [0]*2 ),
    dict( expression = 'np.sin( x*2*np.pi*( i + 1) )', coeffs = [0]*1 )
    ], safe = True )

calib.fit_to_data( x, y )

print( calib.to_dict() )

plot(x, calib.evaluate(x), '--', label = 'fit')

legend()

savefig( figures_directory + 'simple_fit.svg', bbox_inches = 'tight' )

show()
