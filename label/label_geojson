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

import threading
from tkinter import simpledialog

# Create a Tkinter root window
# Hide the root window

# Replace 'your_geojson_file.geojson' with the path to your GeoJSON file
geojson_path = 'new_bldg_df_munich.geojson'

# Define the path to store building labels
label_file = '{}_building_labels.txt'.format(geojson_path)

# Load existing building labels if the file exists
building_labels = {}


if os.path.exists(label_file):
    with open(label_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            building_id, label = line.strip().split(',')
            building_labels[building_id] = int(label)


parser = argparse.ArgumentParser(description='A script that takes command-line arguments.')
parser.add_argument('--path', '-p', type=str, default=geojson_path, help='An optional path argument')
args = parser.parse_args()
path = args.path
geojson_file = path

# Open the GeoJSON file using GeoPandas
gdf = gpd.read_file(geojson_file)
grouped = gdf.groupby('building_id')

print('-----Start to label the GeoJSON:, {}'.format(geojson_path))

for building_id, group in grouped:
    if building_id in building_labels:
        continue  # Skip already labeled buildings


    maxx, minx, maxy, miny, maxz, minz = (0, 10**9, 0, 10**9, 0, 10**9)
    polygons = []
    for geom in group['geometry']:
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
        polygon.set_color(colors.rgb2hex(np.random.rand(3)))
        polygon.set_edgecolor('k')
        polygons.append(polygon)
    height = maxz - minz
    width = maxx - minx
    length = maxy - miny
    area = width * length
    def plot(maxx, minx, maxy, miny, maxz, minz,polygons):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        for polygon in polygons:
            ax.add_collection3d(polygon)

        ax.set_xlim(minx, maxx)
        ax.set_ylim(miny, maxy)
        ax.set_zlim(minz, maxz)
        textsr = f"Building ID: {building_id} \n Height: {height:.2f} \n Width: {width:.2f} \nLength: {length:.2f} \
                \n Footprint Area: {area:.2f} \n"
        ax.text(0.5, 0.15, 0.8, textsr, transform=ax.transAxes, fontsize=10, ha='left', va='top')

        info_text = ax.text(1.9, 2.9, 0.2, '', transform=ax.transAxes, fontsize=10)

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
                        if 1 <= label <= 25:
                            building_labels[building_id] = label
                            update_text(f"Labeled as {label}")
                            print("you have input label", label)

                        elif label == -1:
                            building_labels[building_id] = label
                            update_text("Unlabeled")

                        else:
                            update_text("Invalid input. Enter a label between 0 and 25 or -1 for unlabelled.")

                    except ValueError:
                        update_text("Invalid input. Enter a label between 0 and 25 or -1 for unlabelled.")

                        input_box.set_val("")
        fig.canvas.mpl_connect('key_press_event', on_key)
        plt.show()



    # Display building information and prompt for label input using a GUI window



    plot(maxx, minx, maxy, miny, maxz, minz, polygons)
    if building_id in building_labels.keys():
        print("the labelled label is:", building_labels[building_id])

    #input_label()


    # Save building labels to the file after each building is labeled
    with open(label_file, 'w') as f:
        for b_id, b_label in building_labels.items():
            f.write(f"{b_id},{b_label}\n")

      # Close the current plot window


# Update the GeoDataFrame with building labels
gdf['label'] = gdf['building_id'].map(building_labels)

# Save the GeoDataFrame to a new GeoJSON file
output_geojson = '{}_labeled_buildings.geojson'.format(geojson_path)
gdf.to_file(output_geojson, driver='GeoJSON')
print(f"GeoJSON file with labels saved as {output_geojson}")
