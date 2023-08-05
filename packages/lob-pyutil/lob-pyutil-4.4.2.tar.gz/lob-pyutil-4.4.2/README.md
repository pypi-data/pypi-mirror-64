# pyutil

[![Build Status](https://travis-ci.org/lobnek/pyutil.svg?branch=master)](https://travis-ci.org/lobnek/pyutil)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/lobnek/pyutil/master?filepath=%2Fbinder)


Set of utility code used by Lobnek Wealth Management.


## Installation
```python
pip install git+http://github.com/lobnek/pyutil.git
```

## Running a strategy

Our main concern is to implement and maintain strategies in a robust way. We do not rewrite our codes for production servers 
in alternative programming languages. We use the same Python scripts both in research and production. 

A strategy is a script loading time series data from an archive and using parameters specified a priori.
For research it is helpful to interfere with the parameters before the strategy iterates in a backtest through history.



