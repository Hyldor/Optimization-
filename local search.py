import random

def generate_quadratic_knapsack_instance(num_items):
    # Generate random weights, values, and quadratic coefficients
    weights = [random.randint(1, 10) for _ in range(num_items)]
    values = [random.randint(1, 10) for _ in range(num_items)]
    quadratic_coefficients = [[random.randint(-5, 5) for _ in range(num_items)] for _ in range(num_items)]

    # Write the instance to a file
    with open("quadratic_knapsack_instance.txt", "w") as f:
        f.write(f"{num_items}\n")
        f.write(" ".join(map(str, weights)) + "\n")
        f.write(" ".join(map(str, values)) + "\n")
        for row in quadratic_coefficients:
            f.write(" ".join(map(str, row)) + "\n")

def read_quadratic_knapsack_instance(file_path):
    with open(file_path, "r") as f:
        num_items = int(f.readline())
        weights = list(map(int, f.readline().split()))
        values = list(map(int, f.readline().split()))
        quadratic_coefficients = [list(map(int, line.split())) for line in f]

    return num_items, weights, values, quadratic_coefficients

def greedy_quadratic_knapsack(num_items, weights, values, quadratic_coefficients, capacity):
    # Initialize variables
    selected_items = [0] * num_items
    remaining_capacity = capacity

    # Greedy heuristic: Select items with the highest value-to-weight ratio
    value_to_weight_ratio = [v / w for v, w in zip(values, weights)]

    for _ in range(num_items):
        max_ratio_index = max(range(num_items), key=lambda i: value_to_weight_ratio[i])

        # Check if the item can be added without exceeding capacity
        if weights[max_ratio_index] <= remaining_capacity:
            selected_items[max_ratio_index] = 1
            remaining_capacity -= weights[max_ratio_index]

        # Set the ratio of the selected item to zero to avoid selecting it again
        value_to_weight_ratio[max_ratio_index] = 0

    return selected_items

def evaluate_solution(selected_items, quadratic_coefficients):
    # Calculate the objective value of the solution
    objective_value = 0
    for i in range(len(selected_items)):
        for j in range(len(selected_items)):
            objective_value += quadratic_coefficients[i][j] * selected_items[i] * selected_items[j]

    return objective_value

def hill_climbing_local_search(initial_solution, quadratic_coefficients):
    current_solution = initial_solution.copy()
    current_value = evaluate_solution(current_solution, quadratic_coefficients)

    # Print the initial solution
    print("Initial solution:", current_solution, "Value:", current_value)

    while True:
        # Generate neighbors by flipping a random bit
        neighbor = current_solution.copy()
        index_to_flip = random.randint(0, len(neighbor) - 1)
        neighbor[index_to_flip] = 1 - neighbor[index_to_flip]

        # Evaluate the neighbor
        neighbor_value = evaluate_solution(neighbor, quadratic_coefficients)

        # If the neighbor is better, update the current solution
        if neighbor_value > current_value:
            current_solution = neighbor
            current_value = neighbor_value

            # Print the feasible solution
            print("Feasible solution:", current_solution, "Value:", current_value)
        else:
            # If no improvement is found, break the loop
            break

    return current_solution

if __name__ == "__main__":
    # Generate an instance with 5 items
    generate_quadratic_knapsack_instance(10)

    # Read the generated instance
    num_items, weights, values, quadratic_coefficients = read_quadratic_knapsack_instance("quadratic_knapsack_instance.txt")

    # Set knapsack capacity
    capacity = sum(weights) // 20

    # Solve using the greedy heuristic
    initial_solution = greedy_quadratic_knapsack(num_items, weights, values, quadratic_coefficients, capacity)

    # Evaluate the greedy solution
    greedy_value = evaluate_solution(initial_solution, quadratic_coefficients)

    # Perform local search (hill climbing)
    final_solution = hill_climbing_local_search(initial_solution, quadratic_coefficients)

    # Evaluate the final solution
    final_value = evaluate_solution(final_solution, quadratic_coefficients)

    # Calculate the percentage deviation
    percentage_deviation = abs(final_value - greedy_value) / greedy_value * 100

    # Print the final selected items and percentage deviation
    print("Final selected items:", final_solution)
    print("Percentage Deviation:", percentage_deviation)
