#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import libHREELS as hh
import os, json

file= os.path.join(hh.__path__[0],'materials.json')
with open(file) as json_file:
    materials = json.load(json_file)

print('\n\nAll available materials:')
print(materials.keys())

print('\n\nOne example "STO":\n')
print(hh.importMaterials('STO'))

