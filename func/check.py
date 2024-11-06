# Function to check if conditions are met for a route


def check_capacity(route, truck_list, demands, vehicle_capacities):
    """Verify if the route meets the capacity constraints for each vehicle."""
    current_demand = [0] * len(vehicle_capacities)
    current_vehicle = truck_list[0]

    for i, node in enumerate(route):
        if node == 0:
            if current_demand[current_vehicle] > vehicle_capacities[current_vehicle]:
                return False
            if i < len(truck_list):
                current_vehicle = truck_list[i]
            current_demand[current_vehicle] = 0
        else:
            current_demand[current_vehicle] += demands[node]

    return True


def check_and_correct_route(route, truck_list):
    # Check that the route starts and ends with 0
    if route[0] != 0:
        route.insert(0, 0)
        truck_list.insert(0, truck_list[0])
    if route[-1] != 0:
        route.append(0)
        truck_list.append(truck_list[-1])

    # Traverse the route to check for isolated zeros in the middle
    i = 1  # Start from the second position to ignore the first 0
    while i < len(route) - 1:
        if route[i] == 0 and route[i + 1] != 0 and route[i - 1] != 0:
            # If an isolated zero is found, insert another zero after it
            route.insert(i + 1, 0)
            truck_list.insert(i + 1, truck_list[i + 1])
        i += 1  # Move to the next position
    return route, truck_list
