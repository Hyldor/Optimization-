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

if __name__ == "__main__":
    # Generate an instance with 5 items
    generate_quadratic_knapsack_instance(5)

    # Read the generated instance
    num_items, weights, values, quadratic_coefficients = read_quadratic_knapsack_instance("quadratic_knapsack_instance.txt")

    # Set knapsack capacity
    capacity = sum(weights) // 2

    # Solve using the greedy heuristic
    selected_items = greedy_quadratic_knapsack(num_items, weights, values, quadratic_coefficients, capacity)

    # Print the selected items
    print("Selected items:", selected_items)