from func import (
    load_config,
    plot_routes,
    calculate_and_display_distances,
    data_model,
    simulated_annealing,
    greedy,
    generate_list_of_sites,
)

# Load the YAML configuration
config = load_config("config/config.yaml")


df, data = data_model(config)

site = generate_list_of_sites(data)

full_route, routes, truck_list = greedy(data, site)

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

# Paramètres de recuit simulé
initial_temp = 100000000
cooling_rate = 0.995
min_temp = 1

# Appliquer l'algorithme de recuit simulé
optimized_route, optimized_truck_list, optimized_distance, optimized_routes = (
    simulated_annealing(
        full_route, truck_list, data, initial_temp, cooling_rate, min_temp
    )
)

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
