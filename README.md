[![Build Status](https://travis-ci.org/icgc-dcc/egasub.png)](https://travis-ci.org/icgc-dcc/egasub)

#EGASUB - ICGC EGA Submission CLI

EGASUB is a command line tool assists ICGC members submitting their NGS sequence data to EGA repository.


##Installation

```
# install pipsi
curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | python

# clone the source code
git clone git@github.com:icgc-dcc/egasub.git

# run tests
cd egasub
python setup.py test

# install egasub
pipsi install .
```

## Run

Once installed, you can invoke the tool as follow. This will display information about how to use sub-commands and their options.
```
egasub
```
