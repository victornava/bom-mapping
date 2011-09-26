#!/usr/bin/python


from bom.utils.bom_utils import Bbox
from bom.controller import Controller
#from bom.map.MapGenerator import MapGenerator

#bbox = ((-180,-90),(180,90))
#bbox = ((-180,-90),(180,90))
#bbox = ((540,-90),(700,90))
#bbox = ((90,-70),(180,20))

bbox = ((65,-50),(50,20))
#bbox = ((540,-40),(700,40))

b = Bbox(bbox)

c = Controller(b)
c.getMap()
#print b.lon_min

#mg = MapGenerator(b)
