#!/usr/bin/python

import sys,os
HOME=os.getenv("HOME")
sys.path.append('/%s/seiscomp3/share/gds/tools/' %HOME)

import seiscomp3.Core
import seiscomp3.DataModel

from lib import bulletin, filter

class copiaFilter(filter.Filter):

        def filter(self, ep):

                b=ep.event(0).publicID()

                return "%s" %(str(b))


if __name__ == "__main__":
        app = copiaFilter()
        sys.exit(app())
