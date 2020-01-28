from scipy import signal
import numpy as np

def _linear_filter(b, a, x, axis=-1, zi=None):
    '''
    Assume zi is none, all pole filter (b = [1]), and a[0] = 1
    '''
    y = np.ones(x.shape)
    
    l = a.shape[0] - 1 # largest index in a
    j = b.shape[0] - 1

    for m, n in enumerate(range(len(x))): # len(x) on the correct axis
        
        mm = l < m and l or m
                
        y[m] = x[m]
        
        count = mm - 1
        for k in range(1, mm+1):
            y[n] -= a[mm - count]*y[m-k]
            count -= 1

        mm = j < m and j or m

        if j > 0:
            count = mm - 1
            for k in range(1, mm+1):
                y[n] += b[mm - count]*x[m-k]
                count -= 1
            
    return y

b = np.asarray([1, 0.25])
a = np.asarray([1, 0.5, 0.25])
x = np.asarray([1,2,3,4,5])
y = _linear_filter(b,a,x)

print(y)