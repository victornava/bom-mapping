#!/usr/bin/python

from bom.map.MapGenerator import MapGenerator
from bom.utils.bom_utils import Bbox

#bbox = ((-180,-90),(180,90))
#bbox = ((-180,-90),(180,90))
#bbox = ((540,-90),(700,90))
#bbox = ((90,-70),(180,20))

bbox = ((65,-50),(150,20))
#bbox = ((540,-40),(700,40))

b = Bbox(bbox)

print b.lon_min

mg = MapGenerator(b)
