from func import (
    load_config,
    plot_routes,
    calculate_and_display_distances,
    data_model,
    nearest_neighbor_algorithme,
    opt2_inside,
    opt2_outside,
)

# Load the YAML configuration
config = load_config("config/config.yaml")


df, data = data_model(config)


routes, truck_list, full_route = nearest_neighbor_algorithme(df, data)

# Display the data

truck_distances, total_distance = calculate_and_display_distances(
    routes, data["distance_matrix"]
)

plot_routes(
    routes,
    data["coordinates"][:, 0],
    data["coordinates"][:, 1],
    data["depot"],
    len(routes),
)

routes, route = opt2_outside(
    full_route,
    truck_list,
    data["distance_matrix"],
    data["demands"],
    data["vehicle_capacities"],
)

truck_distances, total_distance = calculate_and_display_distances(
    routes, data["distance_matrix"]
)

plot_routes(
    routes,
    data["coordinates"][:, 0],
    data["coordinates"][:, 1],
    data["depot"],
    len(routes),
)

optimized_routes = []
for route in routes:
    optimized_route = opt2_inside(route, data["distance_matrix"])
    optimized_routes.append(optimized_route)


truck_distances, total_distance = calculate_and_display_distances(
    optimized_routes, data["distance_matrix"]
)

plot_routes(
    optimized_routes,
    data["coordinates"][:, 0],
    data["coordinates"][:, 1],
    data["depot"],
    len(optimized_routes),
)
