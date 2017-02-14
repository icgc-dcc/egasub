[![Build Status](https://travis-ci.org/icgc-dcc/egasub.png)](https://travis-ci.org/icgc-dcc/egasub)

#EGASUB - ICGC EGA Submission CLI

EGASUB is a command line tool assists ICGC members submitting their NGS sequence data to EGA repository.


##Installation

Install pipsi first (if not installed yet)
```
# install pipsi
curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | python

# modify PATH to find pipsi, you may want to add this to the '.bashrc' file
export PATH="~/.local/bin:$PATH"
```

Install latest `egasub` release
```
pipsi install egasub
```

Note: to install a specific version of `egasub`, e.g., `0.1.0rc3` do this:
```
pipsi install egasub==0.1.0rc3
```

If you'd like to play with the latest development version (not recommended for production use), install it from source as below.

```
# clone the source code
git clone https://github.com/icgc-dcc/egasub.git

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

## SOP for ICGC submitters

Detailed SOP for ICGC submitters is availabe [here](https://wiki.oicr.on.ca/display/DCCBIO/EGA+Submission+Tool+SOP).

## Support

Should you need assistance, please contact ICGC DCC at dcc-support@icgc.org.

