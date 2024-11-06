import matplotlib.pyplot as plt


# Function to plot the routes
def plot_routes(routes, x_coords, y_coords, depot, nbr_colors=5):
    plt.figure(figsize=(20, 10))
    colors = plt.cm.get_cmap(None, nbr_colors)
    for i, route in enumerate(routes):
        route_x = [x_coords[loc] for loc in route]
        route_y = [y_coords[loc] for loc in route]
        plt.plot(route_x, route_y, color=colors(i), marker="o", label=f"Truck {i+1}")
        for j, loc in enumerate(route):
            plt.text(x_coords[loc], y_coords[loc], str(loc), fontsize=12)
    plt.scatter(x_coords[depot], y_coords[depot], c="black", label="Depot", s=100)
    plt.title("Truck routes")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True)
    plt.show()
