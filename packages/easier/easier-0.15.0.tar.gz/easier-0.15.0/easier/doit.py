#! /usr/bin/env python

import numpy as np
import easier as ezr

x = np.linspace(-3.14, 3.14, 100)
yt = np.sin(x) 
y = yt + .1 * np.random.randn(len(x))
b = ezr.Bernstein(x=x, y=y, N=1000)
yf = b.predict(x)

xd = np.arange(-3, 4, 1)
ydf = np.array([b.predict(xx) for xx in xd])