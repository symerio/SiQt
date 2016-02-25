# SiQt




## Installation notes

 This package requires Python 2.7 or 3.2-3.5 with the following modules installed: `numpy>=1.9`, `scipy`, `pandas`, `matplotlib`, `scikit-learn`, `six`, `setuptools`, `nose`.

 To install this module run,
    
    python setup.py install


## Unit tests

 The unit tests suite can be run from the command line,

    $ cd siqt/tests/
    $ nosetests -s .

or from within Python with,
 
    import siqt.tests; siqt.tests.run()
