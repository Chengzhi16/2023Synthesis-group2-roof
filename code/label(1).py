import geopandas as gpd
import matplotlib.pyplot as plt
import argparse
import geopandas as gpd
import numpy as np
import matplotlib.colors as colors
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter.simpledialog import askinteger
import os
from copy import deepcopy
import threading
from tkinter import simpledialog
import random

from pathlib import Path
from copy import deepcopy
# from cjio import cityjson
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
plt.close('all')
# from sklearn.preprocessing import FunctionTransformer
# from sklearn import cluster
import numpy as np





# Create a Tkinter root window
# Hide the root window

# Define the path to store building labels
label_file = 'Rotterdam_test.txt'

# Load existing building labels if the file exists
building_labels = {}


if os.path.exists(label_file):
    with open(label_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            building_id, label = line.strip().split(',')
            building_labels[building_id] = int(label)



# Replace 'your_geojson_file.geojson' with the path to your GeoJSON file
parser = argparse.ArgumentParser(description='A script that takes command-line arguments.')
parser.add_argument('--path', '-p', type=str, default='Rotterdam_left.geojson', help='An optional path argument')
parser.add_argument('--buffer', '-b', type=int, default=100, help='distance of buffer')
args = parser.parse_args()
path = args.path
buffer_dist = args.buffer
geojson_file = path

# Open the GeoJSON file using GeoPandas
import pandas as pd
munich = pd.read_csv("Rotterdam_1018.csv")


gdf = gpd.read_file(geojson_file)
gdf['centroid'] = gdf.centroid
print(gdf.columns)
gdf = pd.merge(gdf,munich,how = "left",left_on = "building_id",right_on = "id")

grouped = gdf.groupby('building_id')
probability = 0.02
for building_id, group in grouped:
    random_value = random.random()

    if random_value > probability:
        continue
    if building_id in building_labels:
        continue  # Skip already labeled buildings
    building_point = group['centroid'].iloc[0]

    selected_geometries = gdf['geometry'][(gdf['centroid'].distance(building_point)<buffer_dist) & ((gdf['building_id'] != building_id))]
    print(sum((gdf['centroid'].distance(building_point)<buffer_dist) & ((gdf['building_id'] != building_id))))
    
    def return_polygons(group,colors = 'red'):
        maxx, minx, maxy, miny, maxz, minz = (0, 10**9, 0, 10**9, 0, 10**9)
        polygons = []
        for geom in group:
            x, y, z = zip(*geom.exterior.coords)

            if min(x) < minx:
                minx = min(x)
            if min(y) < miny:
                miny = min(y)
            if min(z) < minz:
                minz = min(z)
            if max(x) > maxx:
                maxx = max(x)
            if max(y) > maxy:
                maxy = max(y)
            if max(z) > maxz:
                maxz = max(z)
            coords = np.array(list(zip(x, y, z)))
            coords = [np.array(list(coord)) for coord in coords]

            polygon = Poly3DCollection([coords])
            polygon.set_color(colors)
            polygon.set_edgecolor('k')
            polygons.append(polygon)
        return polygons, maxx,minx,maxy,miny,maxz,minz
    
    
        

    n_count = group["I_count"].values[0]
    n_direct=group["N_direct"].values[0]
    polygons,maxx,minx,maxy,miny,maxz,minz = return_polygons(group['geometry'],'red')
    polygons_surroundings,maxx2, minx2, maxy2, miny2, maxz2, minz2 = return_polygons(selected_geometries,'blue')
    height = maxz - minz
    width = maxx - minx
    length = maxy - miny
    area = width * length

    def plot(maxx, minx, maxy, miny, maxz, minz,polygons,polygons_surroundings,
            maxx2, minx2, maxy2, miny2, maxz2, minz2):
        fig = plt.figure()
        ax1 = fig.add_subplot(121,projection='3d')
        ax2 = fig.add_subplot(122,projection='3d')
        
        
        polygons2 = deepcopy(polygons)
        for polygon in polygons2:
            ax2.add_collection3d(polygon)
        for polygon in polygons:
            ax1.add_collection3d(polygon)
           
            
        for polygon in polygons_surroundings:
            ax2.add_collection3d(polygon)
        
        widths = max(abs(minx-maxx),abs(miny-maxy))
        ax1.set_xlim(minx, minx+widths)
        ax1.set_ylim(miny, miny+widths)

        ax1.set_zlim(minz, minz+widths)
        ax2.set_xlim(minx2, maxx2)
        ax2.set_ylim(miny2, maxy2)
        ax2.set_zlim(minz2, minz+abs(minx2-maxx2))
        
        
        
        
        textsr = f"Building ID: {building_id} \n Height: {height:.2f} \n Est Floor:{height/3:.2f} \n Width: {width:.2f} \n Length: {length:.2f} \
                \n Footprint Area: {area:.2f} \n n_count: {n_count:.2f} \n n_direct:{n_direct:.2f}"
        plt.figtext(0.1, 0.95,textsr, transform=ax1.transAxes, fontsize=10)

        info_text = plt.figtext(0.1,0.85, '',transform=ax1.transAxes,fontsize=10,color= "red")


        # Create an input box
        from matplotlib.widgets import TextBox
        input_box = TextBox(plt.axes([0.1, 0.05, 0.2, 0.05]), "Enter label:")

        # Update the information text
        def update_text(text):
            info_text.set_text(text)
            plt.draw()

        # Connect the keyboard event handler

        def on_key(event):

                if event.key == 'enter':

                    label = input_box.text
                    try:
                        label = int(label)
                        if 1 <= label <= 15:
                            building_labels[building_id] = label
                            update_text(f"Labeled as {label}")
                            print("you have input label",label)

                        elif label == -1:
                            building_labels[building_id] = label
                            update_text("Unlabeled")
                        elif label == 0:
                            building_labels[building_id] = label
                            update_text("undecided")

                        else:
                            update_text("Invalid input. Enter a label between 0 and 25 or -1 for unlabelled.")

                    except ValueError:
                        update_text("Invalid input. Enter a label between 0 and 25 or -1 for unlabelled.")

                        input_box.set_val("")
        fig.canvas.mpl_connect('key_press_event', on_key)
        plt.show()
   



    # Display building information and prompt for label input using a GUI window
    if height < 2:
        label = 0
        building_labels[building_id]=label
    elif area < 20:
        label = 0
        building_labels[building_id]=label
    elif width <3 or length < 3:
        label = 0
        building_labels[building_id] = label
    #no 3 anymore!
    elif area<200 and n_direct==2:
        continue
    else:
        plot(maxx, minx, maxy, miny, maxz, minz, polygons,polygons_surroundings,
            maxx2, minx2, maxy2, miny2, maxz2, minz2)

    if building_id in building_labels.keys():
        print("the labelled label is:", building_labels[building_id])
        print("total labels is: ",len(building_labels.keys()))

    #input_label()


    # Save building labels to the file after each building is labeled
    with open(label_file, 'w') as f:
        for b_id, b_label in building_labels.items():
            f.write(f"{b_id},{b_label}\n")
    
      # Close the current plot window

gdf = gdf.drop(columns='centroid')
# Update the GeoDataFrame with building labels
gdf['label'] = gdf['building_id'].map(building_labels)

# Save the GeoDataFrame to a new GeoJSON file
output_geojson = 'labeled_buildings.geojson'
gdf.to_file(output_geojson, driver='GeoJSON')
print(f"GeoJSON file with labels saved as {output_geojson}")
