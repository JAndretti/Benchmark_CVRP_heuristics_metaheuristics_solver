from func import (
    load_config,
    data_model,
    greedy,
    generate_multiple_lists_of_sites,
    calculate_total_distance,
    nearest_neighbor_algorithme,
    opt2_outside,
)
import matplotlib.pyplot as plt
from tqdm import tqdm

# Load the YAML configuration
config = load_config("config/config.yaml")

df, data = data_model(config)
nbr_of_seed = 500000
all_sites = generate_multiple_lists_of_sites(data, nbr_of_seed)
print(f"Number of lists: {len(all_sites)}")

list_distances = []

print("Calculating distances for all lists...")
for site in tqdm(all_sites):
    route, routes, truck_routes = greedy(data, site)
    list_distances.append(calculate_total_distance(route, data["distance_matrix"]))

print(f"Minimum distance: {min(list_distances):.2f}")
print(f"Maximum distance: {max(list_distances):.2f}")

routes, truck_list, full_route = nearest_neighbor_algorithme(df, data)
routes, route = opt2_outside(
    full_route,
    truck_list,
    data["distance_matrix"],
    data["demands"],
    data["vehicle_capacities"],
)
print(
    f"Distance with nearest neighborhood : "
    f"{calculate_total_distance(route, data['distance_matrix'])}"
)
print("OR Tools distance : 126317.00")

plt.hist(list_distances, bins=20, color="skyblue", edgecolor="black")
plt.xlabel("Total distance")
plt.ylabel("Number of occurrences")
plt.title("Histogram of total distances")
plt.show()
