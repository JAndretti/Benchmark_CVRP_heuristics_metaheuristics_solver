# Machine learning and metaoptimization: a hybrid approach to VRP and its constraints

## Project Presentation

This project focuses on testing and benchmarking various algorithms for the Capacitated Vehicle Routing Problem (CVRP). Specifically, the following methods are being evaluated:

- Heuristics:
    - Nearest Neighbor
    - 2-opt

- Solver:
    - Google OR-Tools

- Metaheuristic:
    - Simulated Annealing
## Data Representation

The data for the CVRP is represented in the following format:

- **Nodes**: Each node represents a customer or depot with specific coordinates.
- **Demands**: Each customer node has a demand value that must be satisfied.
- **Vehicles**: Each vehicle has a capacity that limits the total demand it can carry.
- **Distance Matrix**: A matrix that contains the distances between each pair of nodes.
### Solution Representation

A final solution is represented as follows:

```python
route = [0, 14, 19, 2, 4, 9, 6, 18, 7, 15, 0, 0, 8, 3, 1, 11, 5, 0, 0, 16, 13, 12, 10, 17, 0]
truck_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2]
```

- **Route**: The global path, where `0` represents the depot. Each segment from `0` to `0` is a route.
- **Truck List**: Indicates which truck is assigned to each segment of the route. The indices correspond to the indices in the `route` list.

## Project Structure

The project is organized into several directories and files, each serving a specific purpose:

- **code/**: Contains the main scripts to run the algorithms:
    - `nearest_neighbor_2opt.py`
    - `or_tools.py`
    - `simulated_annealing.py`
    - `...`

- **config/**: Contains configuration files:
    - `config.yaml`: Configuration for a session.
    - `requirements.txt`: Environment dependencies.

- **data/**: Contains generated datasets used for testing and benchmarking.

- **func/**: Contains utility functions used by the algorithms.

- **Scripts/**: Contains useful scripts, including the data generation script:
    - `data_generation.py`

## How to Use the Project

To get started with this project, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/JAndretti/PhD.git
    ```

2. **Install Python and dependencies**:
    Make sure you have Python installed. Then, install the required libraries:
    ```sh
    pip install -r config/requirements.txt
    ```

3. **Configure the project**:
    Open the configuration file and set the appropriate parameters:
    ```sh
    nano config/config.yaml
    ```

4. **Run the scripts**:
    Execute one of the main scripts from the `code` directory to start the algorithm:
    ```sh
    python code/nearest_neighbor_2opt.py
    # or
    python code/or_tools.py
    # or
    python code/simulated_annealing.py
    ```