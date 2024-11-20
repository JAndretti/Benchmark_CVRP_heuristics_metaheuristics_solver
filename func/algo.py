from .distance import calculate_total_distance
from .utils import convert_routes_to_multiple_routes
from .check import check_capacity, check_and_correct_route

import numpy as np
import random
from tqdm import tqdm


# NEAREST NEIGHBOR


def nearest_neighbor_algorithme(df, data):
    route = [0]
    visited = [0]
    not_visited = df["CustomerID"].tolist()
    not_visited.remove(0)
    current_demande = 0
    current_node = data["depot"]
    current_demande += data["demands"][current_node]
    current_truck = 0
    truck_list = [current_truck]

    while not_visited:
        found = False
        distances = [
            (node, data["distance_matrix"][current_node][node])
            for node in not_visited
            if node != 0
        ]
        distances.sort(key=lambda x: x[1])

        for next_node, _ in distances:
            if (
                current_demande + data["demands"][next_node]
                <= data["vehicle_capacities"][current_truck]
            ):
                visited.append(next_node)
                not_visited.remove(next_node)
                current_demande += data["demands"][next_node]
                current_node = next_node
                route.append(next_node)
                found = True
                truck_list.append(current_truck)
                break

        if not found:
            current_demande = 0
            current_node = data["depot"]
            route.append(current_node)
            truck_list.append(current_truck)
            current_truck = (current_truck + 1) % (data["num_vehicles"])
            route.append(current_node)
            truck_list.append(current_truck)

    route.append(data["depot"])
    truck_list.append(truck_list[-1])

    routes = convert_routes_to_multiple_routes(route)
    return routes, truck_list, route


# 2 OPT


# 2-opt algorithm implementation with capacity check
def opt2_inside(route, distance_matrix):
    """Apply the 2-opt algorithm to optimize a route."""
    best_route = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1:
                    continue
                new_route = route[:i] + route[i:j][::-1] + route[j:]
                if calculate_total_distance(
                    new_route, distance_matrix
                ) < calculate_total_distance(best_route, distance_matrix):
                    best_route = new_route
                    improved = True
        route = best_route
    return best_route


def opt2_outside(route, truck_list, distance_matrix, demands, vehicle_capacity):
    """Apply the 2-opt algorithm to a route."""
    best_route = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1:
                    continue
                new_route = route[:i] + route[i:j][::-1] + route[j:]
                if calculate_total_distance(
                    new_route, distance_matrix
                ) < calculate_total_distance(
                    best_route, distance_matrix
                ) and check_capacity(
                    new_route, truck_list, demands, vehicle_capacity
                ):
                    best_route = new_route
                    improved = True
        route = best_route
    routes = convert_routes_to_multiple_routes(route)
    return routes, route


# SIMULATED ANNEALING


def move_transformation(route, truck_list, data):
    """Apply the move transformation."""
    new_route = route[:]
    new_truck_list = truck_list[:]

    # Find five pairs of customers with the shortest distances
    pairs = []
    for i in range(len(route) - 1):
        pairs.append((i, i + 1, data["distance_matrix"][route[i]][route[i + 1]]))
    pairs.sort(key=lambda x: x[2])
    pairs = pairs[:5]

    # Select five random customers excluding the depot
    # and the customers at positions vi+1
    random_customers = random.sample(
        [
            node
            for node in route
            if node != 0 and node not in [route[p[1]] for p in pairs]
        ],
        5,
    )

    # Remove the random customers from their routes
    for customer in random_customers:
        idx = new_route.index(customer)
        new_route.pop(idx)
        new_truck_list.pop(idx)

    # Insert the random customers into random routes based on capacity constraint
    for customer in random_customers:
        inserted = False
        while not inserted:
            random_route_idx = random.randint(0, len(new_route) - 1)
            tmp_new_route = (
                new_route[:random_route_idx] + [customer] + new_route[random_route_idx:]
            )
            tmp_new_truck_list = (
                new_truck_list[:random_route_idx]
                + [new_truck_list[random_route_idx]]
                + new_truck_list[random_route_idx:]
            )
            tmp_new_route, tmp_new_truck_list = check_and_correct_route(
                tmp_new_route, tmp_new_truck_list
            )
            if check_capacity(
                tmp_new_route,
                tmp_new_truck_list,
                data["demands"],
                data["vehicle_capacities"],
            ):
                new_route = tmp_new_route
                new_truck_list = tmp_new_truck_list
                inserted = True

    return new_route, new_truck_list


def replace_highest_average_transformation(route, truck_list, data):
    """Apply the replace highest average transformation."""
    new_route = route[:]
    new_truck_list = truck_list[:]

    # Calculate the average distance of every pair of customers
    averages = []
    for i in range(1, len(route) - 1):
        avg_distance = (
            data["distance_matrix"][route[i - 1]][route[i]]
            + data["distance_matrix"][route[i]][route[i + 1]]
        ) / 2
        averages.append((i, avg_distance))
    averages.sort(key=lambda x: x[1], reverse=True)
    highest_averages = averages[:5]

    # Remove the five vertices with the largest average distances
    highest_customers = [route[i[0]] for i in highest_averages]
    for customer in highest_customers:
        idx = new_route.index(customer)
        new_route.pop(idx)
        new_truck_list.pop(idx)

    # Insert the five selected customers into random
    # routes with the resulting minimum cost
    for customer in highest_customers:
        best_route = None
        best_truck_list = None
        best_distance = float("inf")
        for i in range(len(new_route)):
            temp_route = new_route[:i] + [customer] + new_route[i:]
            temp_truck_list = (
                new_truck_list[:i] + [new_truck_list[i]] + new_truck_list[i:]
            )
            temp_route, temp_truck_list = check_and_correct_route(
                temp_route, temp_truck_list
            )
            if check_capacity(
                temp_route, temp_truck_list, data["demands"], data["vehicle_capacities"]
            ):
                temp_distance = calculate_total_distance(
                    temp_route, data["distance_matrix"]
                )
                if temp_distance < best_distance:
                    best_route = temp_route
                    best_truck_list = temp_truck_list
                    best_distance = temp_distance
        new_route = best_route
        new_truck_list = best_truck_list

    return new_route, new_truck_list


def swap_transformation(route, truck_list, data):
    """Apply the swap transformation."""
    new_route = route[:]
    new_truck_list = truck_list[:]

    # Select two random customers to swap
    i, j = random.sample(range(1, len(route) - 1), 2)
    new_route[i], new_route[j] = new_route[j], new_route[i]
    # new_truck_list[i], new_truck_list[j] = new_truck_list[j], new_truck_list[i]

    # Check and correct the route if necessary
    new_route, new_truck_list = check_and_correct_route(new_route, new_truck_list)

    return new_route, new_truck_list


def simulated_annealing(
    full_route, truck_list, data, initial_temp, cooling_rate, min_temp
):
    """Optimize the solution using simulated annealing."""
    current_route = full_route[:]
    current_truck_list = truck_list[:]
    best_route = full_route[:]
    best_truck_list = truck_list[:]
    current_distance = calculate_total_distance(current_route, data["distance_matrix"])
    best_distance = current_distance
    temperature = initial_temp
    iteration = 0

    while temperature > min_temp:
        # Choose a transformation
        transformation_choice = random.random()
        if transformation_choice < 0.33:
            new_route, new_truck_list = move_transformation(
                current_route, current_truck_list, data
            )
        elif transformation_choice < 0.66:
            new_route, new_truck_list = replace_highest_average_transformation(
                current_route, current_truck_list, data
            )
        else:
            new_route, new_truck_list = swap_transformation(
                current_route, current_truck_list, data
            )

        # Check if the new route respects the capacity constraints
        if check_capacity(
            new_route, new_truck_list, data["demands"], data["vehicle_capacities"]
        ):
            new_distance = calculate_total_distance(new_route, data["distance_matrix"])

            # Accept the new solution with a probability
            if new_distance < current_distance or random.uniform(0, 1) < np.exp(
                (current_distance - new_distance) / temperature
            ):
                current_route = new_route
                current_truck_list = new_truck_list
                current_distance = new_distance

                # Update the best solution found
                if new_distance < best_distance:
                    best_route = new_route
                    best_truck_list = new_truck_list
                    best_distance = new_distance

        # Cool down the temperature
        temperature *= cooling_rate
        iteration += 1

        # Print progress every 100 iterations
        if iteration % 100 == 0:
            print(f"Temperature: {temperature:.2f}, Best Distance: {best_distance:.2f}")

    routes = convert_routes_to_multiple_routes(best_route)

    return best_route, best_truck_list, best_distance, routes


# GREEDY


def generate_list_of_sites(data):
    len_site = len(data["coordinates"])
    site = [i for i in range(len_site)]
    site = site[1:]
    return site


def generate_multiple_lists_of_sites(data, nbr_of_seed=1000000):
    """Generate multiple lists of sites."""
    len_site = len(data["coordinates"])
    site = [i for i in range(len_site)]
    site = site[1:]
    uniques = set()
    print("Generating multiple lists of sites...")
    for seed in tqdm(range(nbr_of_seed)):
        random.seed(seed)
        list_shuffle = site[:]
        random.shuffle(list_shuffle)

        uniques.add(tuple(list_shuffle))

    return [list(p) for p in uniques]


def greedy(data, site):
    """Apply the greedy algorithm to a list of site."""
    route = []
    truck_routes = []
    truck_routes.append(0)
    route.append(0)
    current_capacity = 0
    current_truck = 0
    while site:
        if (
            data["demands"][site[0]] + current_capacity
            <= data["vehicle_capacities"][current_truck]
        ):
            current_capacity += data["demands"][site[0]]
            truck_routes.append(current_truck)
            route.append(site[0])
            site.pop(0)
        else:
            route.append(0)
            route.append(0)
            truck_routes.append(current_truck)
            current_truck = (current_truck + 1) % data["num_vehicles"]
            truck_routes.append(current_truck)
            current_capacity = 0
    route.append(0)
    truck_routes.append(current_truck)

    routes = convert_routes_to_multiple_routes(route)

    return route, routes, truck_routes
