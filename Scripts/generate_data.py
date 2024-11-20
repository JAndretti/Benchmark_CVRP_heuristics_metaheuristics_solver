import csv
import random
import os
import matplotlib.pyplot as plt


def generate_data(num_customers, filename, save=True):
    # Generate coordinates and demands
    data = []
    # fixed depot
    x = random.uniform(0.4, 0.6)
    y = random.uniform(0.4, 0.6)
    demand = 0
    data.append([0, x, y, demand])
    for i in range(1, num_customers):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        demand = random.randint(1, 9)
        data.append([i, x, y, demand])
    if save:
        # Ensure the data directory exists
        os.makedirs("data", exist_ok=True)
        # Write data to CSV file
        filepath = os.path.join("data", filename)
        with open(filepath, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["CustomerID", "X", "Y", "Demand"])
            writer.writerows(data)
    plot_generated_data(data)


def plot_generated_data(data):
    x_coords = [row[1] for row in data]
    y_coords = [row[2] for row in data]
    plt.figure(figsize=(10, 10))
    plt.scatter(x_coords, y_coords, c="b", marker="o")
    for i, txt in enumerate(data):
        plt.annotate(txt[0], (txt[1], txt[2]), fontsize=12)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Generated customer data")
    plt.grid(True)
    plt.show()


# Example usage
if __name__ == "__main__":
    num_customers = 100  # Change this value as needed
    filename = f"{num_customers}_customers.csv"  # Change this value as needed
    save = True
    generate_data(num_customers, filename, save=False)
    if save:
        print(f"Data generated and saved to 'data/{filename}'")
