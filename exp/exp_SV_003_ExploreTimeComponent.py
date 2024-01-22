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



path_tue = '../dat/satellite_above_tübingen_90.txt'

# TUEBINGEN
data_list_tue = read_json_objects_from_file(path_tue)


def animate_points():
    lats_tue = []
    longs_tue = []
    alts_tue = []
    dfs_tue = []

    ani_length = len(data_list_tue)
    for idx in range(ani_length):
        data_tue = data_list_tue[idx]
        df_tue = pd.DataFrame(data_tue['above'])
        lats_tue.append(df_tue['satlat'])
        longs_tue.append(df_tue['satlng'])
        alts_tue.append(df_tue['satalt'])
        dfs_tue.append(df_tue)

    data_tue = pd.concat(dfs_tue, axis=0)
    data_tue.info()

    df = data_tue

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.Robinson()})

    #ax.set_extent([-20, 40, 30, 70], crs=ccrs.PlateCarree())
    ax.set_global()
    ax.coastlines(resolution='50m', color='black', linewidth=1)

    # Initialize an empty scatter plot
    scatter = ax.scatter([], [], color='red', marker='o', s=5, transform=ccrs.PlateCarree())

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
        scatter.set_offsets([[0, 0]])
        return scatter,

    # Define the update function
    def update(frame):
        start_idx = frame * 3100
        end_idx = (frame + 1) * 3100
        df_frame = df.iloc[start_idx:end_idx]
        #df_filtered = df_frame[df_frame['satname'].str.contains("STARLINK", case=False, na=False)]
        title = data_list_tue[frame]["date"]
        #height = df_filtered["satalt"]
        if 'satlat' in df_frame.columns and 'satlng' in df_frame.columns:
            scatter.set_offsets(df_frame[['satlng', 'satlat']].values)
            ax.set_title(title)
        else:
            print(f"Skipping frame {frame} due to unexpected DataFrame structure.")
        return scatter,

    # Calculate the number of frames based on the size of each time frame
    num_frames = len(df) // 3100




    # Create the animation
    ani = animation.FuncAnimation(fig, update, frames=num_frames, init_func=init, interval=100)
    #ani.save('animation.mp4', writer='ffmpeg', fps=20)
    # Display the animation
    plt.show()


def animate_desnity():
    # KERNEL DENSITY:
    # Color map
    cmap = plt.get_cmap('CMRmap')
    my_cmap = cmap(np.arange(cmap.N))
    my_cmap[:, -1] = np.linspace(0, 1, cmap.N)
    my_cmap = ListedColormap(my_cmap)

    def kernel_density(lats, longs, projection, k, extend):
        geo = ccrs.Geodetic()

        h = projection.transform_points(geo, lats, longs)[:, :2].T

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
    ax.stock_img() # Add a stock background image
    ax.imshow(v, origin='lower',
              extent=extend_transf,
            interpolation='bilinear',
            cmap=my_cmap)
    plt.show()


if __name__ == "__main__":
    animate_points()
