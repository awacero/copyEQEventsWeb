#!/usr/bin/env seiscomp-python

import sys,os

sys.path.append( os.path.join(os.environ['SEISCOMP_ROOT'],'share/gds/tools/'))

import seiscomp3.Core
import seiscomp3.DataModel

from lib import bulletin, filter

import logging
import logging.config

logging_file = os.path.join(os.environ['SEISCOMP_ROOT'],'var/log/','gds_service_copiaEvento.log')
logging.basicConfig(filename=logging_file, format='%(asctime)s %(message)s')
logger = logging.getLogger("copiaEvento")
logger.setLevel(logging.DEBUG)

class copiaFilter(filter.Filter):

    def filter(self, event_parameter):
        
                
        event_id = event_parameter.event(0).publicID()
        logger.info("Start filter_copia for: %s" %event_id)

        return "%s" %event_id


if __name__ == "__main__":
    app = copiaFilter()
    sys.exit(app())
