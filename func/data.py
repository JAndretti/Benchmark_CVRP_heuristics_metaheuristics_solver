import yaml
import pandas as pd
import numpy as np
from func.distance import calculate_distance_matrix


# Function to load configuration from the YAML file
def load_config(yaml_file):
    """Load the configuration from a YAML file."""
    with open(yaml_file, "r") as file:
        config = yaml.safe_load(file)
    return config


def data_model(config):
    """Create the data model for the problem."""
    data = {}
    # read yaml file
    df = pd.read_csv(config["file"])
    coordinates = df[
        [
            "X",
            "Y",
        ]
    ].values
    demands = df["Demand"].values
    # Calculate the distance matrix
    dist_matrix = calculate_distance_matrix(coordinates)
    # Multiply by 100 to raise the valuer and avoid values are blended during rounding
    dist_matrix = np.array(dist_matrix) * config["matrix_factor"]
    mat = np.rint(dist_matrix).astype(int)
    data["distance_matrix"] = mat
    data["coordinates"] = coordinates
    data["demands"] = demands
    data["time"] = config["time"]  # Time limit in seconds
    data["num_vehicles"] = config["trucks"][
        "num_trucks"
    ]  # Specify the number of vehicles
    data["vehicle_capacities"] = (
        config["trucks"]["capacities"] * data["num_vehicles"]
    )  # Specify the capacity of vehicles
    data["depot"] = 0  # The index of the depot
    return df, data
