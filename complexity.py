import random
import time
import csv
from main import *

def generate_random_problem(n):
    cost_matrix = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]
    temp_matrix = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]
    provisions = [sum(row) for row in temp_matrix]
    orders = [sum(temp_matrix[i][j] for i in range(n)) for j in range(n)]

    return cost_matrix, provisions, orders

def run_complexity_study():
    sizes = [10, 40, 100, 400, 1000, 4000, 10000]
    num_trials = 10

    with open('complexity_results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Matrix_Size_N', 'Trial_Number', 'NW_Time_Seconds', 'BH_Time_Seconds'])
        for n in sizes:
            print(f"\n--- Testing size n = {n} ---")

            for trial in range(1, num_trials + 1):
                cost_matrix, provisions, orders = generate_random_problem(n)

                start_time = time.perf_counter()
                NorthWest(cost_matrix, provisions.copy(), orders.copy(), verbose=False)
                nw_time = time.perf_counter() - start_time

                start_time = time.perf_counter()
                BalasHammer(cost_matrix, provisions.copy(), orders.copy(), verbose=False)
                bh_time = time.perf_counter() - start_time

                writer.writerow([n, trial, nw_time, bh_time])
                print(trial)

            print(f"Finished 100 trials for n={n}. Data saved to CSV.")




if __name__ == "__main__":
    run_complexity_study()
