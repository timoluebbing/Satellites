import matplotlib.animation as animation
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import pandas as pd
import json
import cartopy.crs as ccrs
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend as an example, but you can try other backends
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from scipy import stats
import math

""" 
exp_SV_001_ExploreTimeComponent.py

Discover changes in satellite density over time.

Sebastian Volz, January 2024
"""

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



path_tue = '../dat/satellite_above_tue_90_5sek.txt'

# TUEBINGEN
data_list_tue = read_json_objects_from_file(path_tue)

dfs_tue = []
time_steps_tue = []
time_steps_tue.append(0)
ani_length = len(data_list_tue)
for idx in range(ani_length):
    data_tue = data_list_tue[idx]
    df_tue = pd.DataFrame(data_tue['above'])
    time_steps_tue.append(time_steps_tue[idx] + len(df_tue))
    dfs_tue.append(df_tue)

data_tue = pd.concat(dfs_tue, axis=0)
data_tue.info()

def animate_points(animation_name,  zoom, base_color, base_legend, only_starlink, single_point_name, single_point_color):
    df = data_tue

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.Robinson()})

    if zoom:
        ax.set_extent([-20, 40, 30, 70], crs=ccrs.PlateCarree())
    else:
        ax.set_global()

    ax.coastlines(resolution='50m', color='black', linewidth=1)

    # Initialize scatter plots
    scatter_base = ax.scatter([], [], color=base_color, marker='o', s=5, label=base_legend, transform=ccrs.PlateCarree())
    scatter_single = ax.scatter([], [], color=single_point_color, marker='o', s=5, label='STARLINK-1226',
                                   transform=ccrs.PlateCarree())

    # Customize other plot elements if needed
    ax.set_title('Points Over Time')
    gl = ax.gridlines(draw_labels=True)
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

    # Define the initialization function
    def init():
        # Initialize scatter with some dummy data
        scatter_base.set_offsets([[0, 0]])
        scatter_single.set_offsets([[0, 0]])
        return scatter_base, scatter_single

    # Define the update function
    def update(frame):
        start_idx = time_steps_tue[frame]
        end_idx = time_steps_tue[frame + 1]
        df_frame = df.iloc[start_idx:end_idx]
        if only_starlink:
            df_filtered = df_frame[df_frame['satname'].str.contains("STARLINK", case=False, na=False)]
            df_frame = df_filtered
            is_starlink = df_frame['satname'].str.contains("STARLINK", case=False, na=False)
            scatter_base.set_offsets(df_frame[is_starlink][['satlng', 'satlat']].values)
        # Check if 'sat_name' contains the string "STARLINK"
        else:
            scatter_base.set_offsets(df_frame[['satlng', 'satlat']].values)

        scatter_single.set_offsets(
            df_frame[df_frame['satname'] == single_point_name][['satlng', 'satlat']].values)

        title = data_list_tue[frame]["date"]
        ax.set_title(title)

        return scatter_base, scatter_single

    # Add a legend
    ax.legend(loc='upper left')

    # Calculate the number of frames based on the size of each time frame
    num_frames = len(df) // 3100




    # Create the animation
    ani = animation.FuncAnimation(fig, update, frames=num_frames, init_func=init, interval=100)
    ani.save(f'../doc/animation/{animation_name}.mp4', writer='ffmpeg', fps=20)
    # Display the animation
    plt.show()


# doesnt work

def animate_density():
    def has_nan_or_inf(lst):
        return any(math.isnan(x) or math.isinf(x) for x in lst)

    # KERNEL DENSITY:
    # Color map
    cmap = plt.get_cmap('CMRmap')
    my_cmap = cmap(np.arange(cmap.N))
    my_cmap[:, -1] = np.linspace(0, 1, cmap.N)
    my_cmap = ListedColormap(my_cmap)

    def kernel_density(lats, longs, projection, k, extend):
        geo = ccrs.Geodetic()

        h = projection.transform_points(geo, lats, longs)[:, :2].T

        zw1 = [x for x in h[0] if not (math.isnan(x) or math.isinf(x))]
        zw2 = [x for x in h[1] if not (math.isnan(x) or math.isinf(x))]
        h = [zw1, zw2]

        kde = stats.gaussian_kde(h)
        # Coordinates of the four corners of the map.
        x0, x1, y0, y1 = extend
        # Create the grid.
        tx, ty = np.meshgrid(np.linspace(x0, x1, 2 * k),
                            np.linspace(y0, y1, k))
        # Reshape the grid for the kde() function.
        mesh = np.vstack((tx.ravel(), ty.ravel()))
        # Evaluate the kde() function on the grid.
        v = kde(mesh).reshape((k, 2 * k))

        return v


    longs = np.array(np.array(data_tue['satlng']))
    lats = np.array(np.array(data_tue['satlat']))

    # longs = np.array(data_tue_starlink_masked['satlng'])
    # lats = np.array(data_tue_starlink_masked['satlat'])

    crs_round = ccrs.Orthographic(9, 48)
    extend = [-15, 75, 25, 65]
    extend_transf = crs_round.transform_points(ccrs.Geodetic(), np.array(extend[:2]), np.array(extend[2:]))[:, :2].T.flatten().tolist()
    k = 100
    v = kernel_density(longs, lats, projection=crs_round, k=k, extend=extend_transf)

    # Plot the heat map
    ax = plt.axes(projection=crs_round)
    ax.coastlines()
    #ax.stock_img() # Add a stock background image
    ax.imshow(v, origin='lower',
              extent=extend_transf,
            interpolation='bilinear',
            cmap=my_cmap)
    plt.show()


if __name__ == "__main__":
    animate_points(animation_name="starlink_5sek_europe", zoom=True, base_color="blue", base_legend="Starlink",
                   only_starlink=True, single_point_name="STARLINK-1227",
                   single_point_color="red")
