1. neighbour.py 
input: cityjson file
Calculate neighbour numbers in one cluster, direct neighbour number and intersected area(with buffer=0.1)

2.cluster.py
input: feature .csv file, cityjson file
do cluster on calculated features, write the label to cityjson file

3. label(1).py
input: feature .csv file, geojson file
label system for geojson data

4. model.ipynb
input: label result .txt file, feature .csv file
classification

5. roofsegment.py
input: lod 1.3, lod 2.2 cityjson file
use lod 1,3 and lod 2,2 data, project them to x-y plane and do intersection. If the intersected area>0.9*(lod2.2 roofsurface area), then, it belongs to roof group set by lod 1.3 roof surface.

6.Zurich.ipynb
filter out small building parts