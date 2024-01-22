"""
Source code for loading satellite data from JSON files.
"""

import math
import json
import numpy as np
import pandas as pd


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
    
    
def load_satellites_data(file_path, n_samples=None):
    data_list = read_json_objects_from_file(file_path)
    
    if n_samples is None:
        n_samples = len(data_list)
    
    sample_idx = np.arange(n_samples)
    random_indices = np.random.choice(sample_idx, size=n_samples)

    lats, longs, alts, dfs = [], [], [], []

    for idx in random_indices:
        data = data_list[idx]
        df = pd.DataFrame(data['above'])
        lats.append(df['satlat'])
        longs.append(df['satlng'])
        alts.append(df['satalt'])
        dfs.append(df)
        
    data = pd.concat(dfs, axis=0)
    data.info()
    
    return data


def filter_data_tue(data_tue):
    # Filter by euclidean distance to Tübingen
    r = 6371 # earth radius (cancels out in the formula)
    gamma = 14.172
    gamma_in_meters = gamma * 2 * r * math.pi / 360
    tue_lat = 90 - 48.782536
    tue_long = 9.176995
    rome_lat = 41.52
    rome_long = 12.29
    
    data_tue_masked = data_tue[np.sqrt((2*r**2 - 2*r**2 *
                  ((math.sin(np.radians(tue_lat)) * data_tue['satlat'].apply(lambda x: math.sin(np.radians(90 - x))) 
                    * data_tue['satlng'].apply(lambda x: math.cos(np.radians(tue_long-x)))) 
                    + (math.cos(np.radians(tue_lat)) * data_tue['satlat'].apply(lambda x: math.cos(np.radians(90 - x))))))) <= gamma_in_meters]
    
    return data_tue_masked