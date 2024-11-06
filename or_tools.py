# https://github.com/Farid-Najar/TransportersDilemma/blob/master/transporter.py

"""Capacited Vehicles Routing Problem (CVRP)."""

from ortools.constraint_solver import (
    routing_enums_pb2,
)
from ortools.constraint_solver import (
    pywrapcp,
)
from func import (
    plot_routes,
    calculate_and_display_distances,
    load_config,
    data_model,
)


def print_solution(
    data,
    manager,
    routing,
    solution,
):
    """Prints solution on console and returns routes as list of lists."""
    print(f"Objective: {solution.ObjectiveValue()}")
    total_distance = 0
    total_load = 0
    routes = []  # This will store the routes for each vehicle
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route = []  # Store the route for this vehicle
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route.append(node_index)  # Add node to the route
            route_load += data["demands"][node_index]
            plan_output += f" {node_index} Load({route_load}) -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index,
                index,
                vehicle_id,
            )
        route.append(manager.IndexToNode(index))  # Add the depot at the end
        if len(route) <= 2:  # Do not include empty routes
            continue
        routes.append(route)  # Add the route to the list of routes
        plan_output += f" {manager.IndexToNode(index)} Load({route_load})\n"
        plan_output += f"Distance of the route: {route_distance}m\n"
        plan_output += f"Load of the route: {route_load}\n"
        print(plan_output)
        total_distance += route_distance
        total_load += route_load

    print(f"Total distance of all routes: {total_distance}m")
    print(f"Total load of all routes: {total_load}")

    return routes  # Return the list of routes


def main():
    """Solve the CVRP problem."""
    # Instantiate the data problem.

    config = load_config("config/config.yaml")

    (df, data) = data_model(config)

    # TO FORCE NUMBER OF TRUCKS TO 100 TO ENSURE A SOLUTION

    data["num_vehicles"] = (
        100  # Specify the number of vehicles !
        # FIX it TO 100 so algorithme finds a solution anyway
    )
    data["vehicle_capacities"] = [data["vehicle_capacities"][0]] * data["num_vehicles"]

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]),
        data["num_vehicles"],
        data["depot"],
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    # Create and register a transit callback.
    def distance_callback(
        from_index,
        to_index,
    ):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)

        # Ensure the indices are within valid range
        if from_node >= len(data["distance_matrix"]) or to_node >= len(
            data["distance_matrix"]
        ):
            raise ValueError(
                f"Invalid node indices: from_node={from_node}, to_node={to_node}"
            )

        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.
    def demand_callback(
        from_index,
    ):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data["vehicle_capacities"],  # vehicle maximum capacities
        True,  # start cumul to zero
        "Capacity",
    )

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.FromSeconds(data["time"])

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        routes = print_solution(
            data,
            manager,
            routing,
            solution,
        )

    plot_routes(
        routes,
        data["coordinates"][:, 0],
        data["coordinates"][:, 1],
        data["depot"],
        len(routes),
    )
    print(f"Number of trucks {len(routes)}")
    truck_distances, total_distance = calculate_and_display_distances(
        routes, data["distance_matrix"]
    )


if __name__ == "__main__":
    main()
