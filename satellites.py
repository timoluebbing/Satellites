import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from plotly.subplots import make_subplots
import json
import random
import sys

# funct irgendwie nicht:
# sys.path.append( YOUR_PROJECT_DIR )
# sys.path.append("C:/Users/timol/OneDrive/Documents/Studium/Master/Semester1/DataLiteracy/Satellites/")

path = 'Satellites/Data/satellite_above_45.txt'

def read_json_objects_from_file(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
        # Split the content based on semicolons
        json_objects = file_content.split(';')
        # Remove any leading or trailing whitespaces from each JSON object
        json_objects = [json_object.strip() for json_object in json_objects]
        # Init output list
        data_list = []
        # Parse each JSON object
        for index, json_object in enumerate(json_objects):
            try:
                # Load JSON object
                data = json.loads(json_object)
                data_list.append(data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON object {index}: {e}")
                
        return data_list


def main(plot_plt, plot_px):
    
    # geyser = sns.load_dataset("geyser")
    # print(type(geyser))
    # sns.kdeplot(data=geyser, x="waiting", y="duration")
    # plt.show()
    
    
    data_list = read_json_objects_from_file(path)
    n_samples = len(data_list)
    
    n = 100
    # np.random.seed(0)
    sample_idx = np.arange(n_samples)
    random_indices = np.random.choice(sample_idx, size=n)
    print(random_indices)
    
    lats = []
    longs = []
    dfs = []
    
    for idx in random_indices:
        data = data_list[idx]
        df = pd.DataFrame(data['above'])
        lats.append(df['satlat'])
        longs.append(df['satlng'])
        dfs.append(df)
        
    data = pd.concat(dfs, axis=0)
    data.info()
    
    X = data[['satlng', 'satlat']].copy()
    X = X.iloc[:(len(X) // 4)]
    X.info()
    
    
    kde = sns.kdeplot(
        X, 
        x='satlng', 
        y='satlat', 
        fill=True, 
        # color='r',
        # palette='rocket', 
        levels=10
    )

    plt.title('Kernel Density Estimation')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    plt.show()

    if plot_plt:
        fig, ax = plt.subplots()

        for lat, long in zip(lats, longs):
            ax.scatter(long, lat, alpha=1/n, color='b', marker='.')
        # ax.scatter(long, lat)
        # ax.scatter(long2, lat2, color='black')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_title('Satellite Positions')

        plt.show()

    if plot_px:
        
        data = data_list[0]
        data2 = data_list[-1]
        # print(data['above'])

        df = pd.DataFrame(data['above'])
        df2 = pd.DataFrame(data2['above'])
        df.info()
        
        # fig = px.scatter_geo(df,lat='satlat',lon='satlng', hover_name="satid")
        # fig.update_layout(title = 'World map', title_x=0.5)
        # fig.show()
        
        fig = px.scatter_mapbox(df, 
                                lat="satlat", 
                                lon="satlng", 
                                hover_name="satid",
                                zoom=2, 
                                height=800,
                                width=800)
        # fig.add_trace(
        #     px.scatter_mapbox(df2,
        #                     lat='satlat',
        #                     lon="satlng", 
        #                     hover_name="satid",
        #                     zoom=2, 
        #                     height=800,
        #                     width=800)
        # )
        
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.show()


if __name__ == "__main__":
    main(plot_plt=False, plot_px=False)