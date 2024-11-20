from func import (
    load_config,
    plot_routes,
    calculate_and_display_distances,
    data_model,
    greedy,
    generate_list_of_sites,
)

# Load the YAML configuration
config = load_config("config/config.yaml")

df, data = data_model(config)

site = generate_list_of_sites(data)

route, routes, truck_routes = greedy(data, site)

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
