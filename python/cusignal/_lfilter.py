# Copyright (c) 2019-2020, NVIDIA CORPORATION.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from scipy import signal
import numpy as np

def _linear_filter(b, a, x, axis=-1, zi=None):
    '''
    Assume zi is none and a[0] = 1
    TODO: Add normalization
    '''
    y = np.ones(x.shape)
    
    l = a.shape[0] - 1 # largest index in a
    j = b.shape[0] - 1 # largest index in b

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

#b = np.asarray([1])
b = np.asarray([1, 0.25])
a = np.asarray([1, 0.5, 0.25])
x = np.asarray([1,2,3,4,5])
y = _linear_filter(b,a,x)

print(y)