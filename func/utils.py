def convert_routes_to_multiple_routes(route):
    """Convert a single route to multiple routes."""
    routes = []
    current_route = []
    for node in route:
        current_route.append(node)
        if node == 0 and len(current_route) > 1:
            if current_route != [0, 0]:
                routes.append(current_route)
            current_route = []
            current_route.append(0)
    return routes
