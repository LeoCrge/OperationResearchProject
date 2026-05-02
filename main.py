from contextlib import nullcontext
from pathlib import Path
from collections import deque

def readfile(file):
    """Read a transportation problem from src/Problems/ProblemX.txt."""
    path = Path("src/Problems") / f"Problem{file}.txt"
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    firstLine = lines[0].split()
    numProvision = int(firstLine[0])
    numOrders = int(firstLine[1])

    cost_matrix = []
    provisions = []

    for i in range(1, numProvision + 1):
        parts = lines[i].split()
        row_costs = [int(x) for x in parts[:numOrders]]
        cost_matrix.append(row_costs)
        provisions.append(int(parts[-1]))

    orders_line = lines[numProvision + 1].split()
    orders = [int(x) for x in orders_line]

    if sum(provisions) != sum(orders):
        raise ValueError(
            f"Unbalanced problem: total provisions={sum(provisions)}, total orders={sum(orders)}"
        )

    return path, numProvision, numOrders, cost_matrix, provisions, orders


def format_value(value, width=8):
    if value is None:
        return "-".rjust(width)
    return str(value).rjust(width)


def display_cost_matrix(cost_matrix, provisions, orders):
    """Display the cost matrix with provisions and orders."""
    n = len(provisions)
    m = len(orders)
    width = 8

    print("\nCOST MATRIX")
    print("".ljust(width) + "".join(f"C{j+1}".rjust(width) for j in range(m)) + "Provision".rjust(width + 2))
    for i in range(n):
        row = f"P{i+1}".ljust(width)
        row += "".join(format_value(cost_matrix[i][j], width) for j in range(m))
        # iterate through each [j] in the list [i] so for the row check every elem
        row += format_value(provisions[i], width + 2)
        #lastly print the provisions which is the last elem that was previously obtained when reading the files
        print(row)
        #finish printing it 
    print("Orders".ljust(width) + "".join(format_value(orders[j], width) for j in range(m)))

# later part when user ask either bh or nw
def display_transportation(proposal, cost_matrix=None, title="TRANSPORTATION PROPOSAL"):
    """Display a transportation proposal. If cost_matrix is provided, also show total cost."""
    n = len(proposal)
    m = len(proposal[0]) if n else 0
    width = 8

    print(f"\n{title}")
    print("".ljust(width) + "".join(f"C{j+1}".rjust(width) for j in range(m)))
    for i in range(n):
        row = f"P{i+1}".ljust(width)
        row += "".join(format_value(proposal[i][j], width) for j in range(m))
        print(row)

    if cost_matrix is not None:
        print("Total Cost:", calculate_total_cost(proposal, cost_matrix))

# type shit def just calculate the sum of every cell for proposal multiplied by initial one 
def calculate_total_cost(proposal, cost_matrix):
    total_cost = 0
    for i in range(len(proposal)):
        for j in range(len(proposal[0])):
            total_cost += proposal[i][j] * cost_matrix[i][j]
    return total_cost


def NorthWest(cost_matrix, provisions, orders):
    print("\n================ NORTH-WEST ALGORITHM ================")
    num_suppliers = len(provisions)
    num_customers = len(orders)
    row = 0
    col = 0

    prov_left = provisions.copy()
    ord_left = orders.copy()
    proposal = [[0 for _ in range(num_customers)] for _ in range(num_suppliers)]

    while row < num_suppliers and col < num_customers:
        allocated = min(prov_left[row], ord_left[col])
        proposal[row][col] = allocated
        print(f"Fill edge P{row+1}->C{col+1}: min({prov_left[row]}, {ord_left[col]}) = {allocated}")

        prov_left[row] -= allocated
        ord_left[col] -= allocated

        if prov_left[row] == 0:
            row += 1
        if col < num_customers and ord_left[col] == 0:
            col += 1

    total_cost = calculate_total_cost(proposal, cost_matrix)
    display_transportation(proposal, cost_matrix, "NORTH-WEST INITIAL PROPOSAL")
    return proposal, total_cost


def two_smallest(values):
    """Return the two smallest values of a non-empty list."""
    values_sorted = sorted(values)
    if len(values_sorted) == 1:
        return values_sorted[0], values_sorted[0]
    return values_sorted[0], values_sorted[1]


def compute_penalties(cost_matrix, active_rows, active_cols):
    """Compute Balas-Hammer/"""
    row_penalties = {}
    col_penalties = {}

    for i in active_rows:
        costs = [cost_matrix[i][j] for j in active_cols]
        smallest, second_smallest = two_smallest(costs)
        # redundance why did i implement it before hand to calculate the row penalty directly there
        # i should have ? maybe implement it in it ?
        # have to see that later on 
        row_penalties[i] = second_smallest - smallest

    for j in active_cols:
        costs = [cost_matrix[i][j] for i in active_rows]
        smallest, second_smallest = two_smallest(costs)
        col_penalties[j] = second_smallest - smallest

    return row_penalties, col_penalties


def display_penalties(row_penalties, col_penalties):
    print("\nPenalties:")
    print("Rows   :", "  ".join(f"P{i+1}={p}" for i, p in row_penalties.items()))
    print("Columns:", "  ".join(f"C{j+1}={p}" for j, p in col_penalties.items()))

# recuperer case utilise dans solutions 
def get_basic_cells(proposal):
    basic_cells = []
    for i in range(len(proposal)):
        for j in range(len(proposal[0])):
            if proposal[i][j] > 0:
                basic_cells.append((i, j))
    return basic_cells

# rajout de cette fonction pour l'equation pour avoir n+m-1 = required 
# fonction de merde 
# dcp ca je dois l'avoir pour la partie proposal pour avoir un lien
# 
def fix_degeneracy(basic_cells_set, n, m):
    required = n + m - 1
    if len(basic_cells_set) >= required:
        return basic_cells_set

    fake_matrix = [[0 for _ in range(m)] for _ in range(n)]
    for (r,c) in basic_cells_set:
        fake_matrix[r][c] = 1
    # basic step
    for i in range(n):
        for j in range(m):
            if len(basic_cells_set) >= required: #then this check if we already have a valid solution
                return basic_cells_set
            #if not 
            if (i, j) not in basic_cells_set:
                fake_matrix[i][j] = 1
                _ ,_ , test_cycle = breadthfs(fake_matrix, start_node=i)
                # we implement a new cell with value 0 to have a link and have the proper implementation
                if not test_cycle:
                    basic_cells_set.add((i, j))
                    print(f"Added cell at P{i+1}->C{j+1} to fix degeneracy")
                else:
                    fake_matrix[i][j] = 0
    return basic_cells_set

def BalasHammer(cost_matrix, provisions, orders):
    """Balas-Hammer algorithm, """
    print("\n================ BALAS-HAMMER ALGORITHM ================")
    n = len(provisions)
    m = len(orders)

    prov_left = provisions.copy()
    ord_left = orders.copy()
    proposal = [[0 for _ in range(m)] for _ in range(n)]

    active_rows = set(range(n))
    active_cols = set(range(m))
    step = 1

    while active_rows and active_cols:
        print(f"\n--- Step {step} ---")
        row_penalties, col_penalties = compute_penalties(cost_matrix, active_rows, active_cols)
        display_penalties(row_penalties, col_penalties)

        max_row_penalty = max(row_penalties.values()) if row_penalties else -1
        max_col_penalty = max(col_penalties.values()) if col_penalties else -1
        max_penalty = max(max_row_penalty, max_col_penalty)

        candidate_rows = [i for i, p in row_penalties.items() if p == max_penalty]
        candidate_cols = [j for j, p in col_penalties.items() if p == max_penalty]

        print("Maximum penalty:", max_penalty)
        if candidate_rows:
            print("Rows with maximum penalty:", ", ".join(f"P{i+1}" for i in candidate_rows))
        if candidate_cols:
            print("Columns with maximum penalty:", ", ".join(f"C{j+1}" for j in candidate_cols))

        # Choose the row/column with the cheapest available cell.
        candidates = []
        for i in candidate_rows:
            min_cost = min(cost_matrix[i][j] for j in active_cols)
            candidates.append((min_cost, "row", i))
        for j in candidate_cols:
            min_cost = min(cost_matrix[i][j] for i in active_rows)
            candidates.append((min_cost, "col", j))

        _, chosen_type, chosen_index = min(candidates, key=lambda x: (x[0], x[1], x[2]))

        if chosen_type == "row":
            i = chosen_index
            j = min(active_cols, key=lambda col: (cost_matrix[i][col], col))
            print(f"Chosen line: P{i+1}; cheapest edge is P{i+1}->C{j+1} with cost {cost_matrix[i][j]}")
        else:
            j = chosen_index
            i = min(active_rows, key=lambda row: (cost_matrix[row][j], row))
            print(f"Chosen column: C{j+1}; cheapest edge is P{i+1}->C{j+1} with cost {cost_matrix[i][j]}")

        allocated = min(prov_left[i], ord_left[j])
        proposal[i][j] = allocated
        print(f"Fill edge P{i+1}->C{j+1}: min({prov_left[i]}, {ord_left[j]}) = {allocated}")

        prov_left[i] -= allocated
        ord_left[j] -= allocated

        if prov_left[i] == 0 and i in active_rows:
            active_rows.remove(i)
            print(f"P{i+1} is satisfied and removed.")
        if ord_left[j] == 0 and j in active_cols:
            active_cols.remove(j)
            print(f"C{j+1} is satisfied and removed.")

        step += 1

    total_cost = calculate_total_cost(proposal, cost_matrix)
    display_transportation(proposal, cost_matrix, "BALAS-HAMMER INITIAL PROPOSAL")
    return proposal, total_cost


def breadthfs(matrix, start_node=0):
    n = len(matrix)
    m = len(matrix[0])
    total_nodes = n + m
    has_cycle = False
    is_complete = True
    visited = [False] * total_nodes
    queue = deque()
    visited[start_node] = True
    queue.append((start_node, -1))
    parent_list = [-1] * total_nodes
    cycle = []
    while queue:
        node, parent = queue.popleft()

        """ Print node
        if node < m:
            print(f"R{node}", end=" ")
        else:
            print(f"C{node - m}", end=" ")
        """

        # If it's row node
        if node < n:
            for j in range(m): #yes sir just m because you check every row but can miss one
                if matrix[node][j] != 0:
                    child = n + j  # column node
                    if not visited[child]:
                        visited[child] = True
                        parent_list[child] = node
                        queue.append((child, node))
                    elif child !=parent:
                        has_cycle = True

        # If it's column node
        else:
            col = node - n
            for i in range(n):
                if matrix[i][col] != 0:
                    child = i  # row node
                    if not visited[child]:
                        visited[child] = True
                        parent_list[child] = node
                        queue.append((child, node))
                    elif child !=parent:
                        if not cycle : #we want to only check for a single cycle no need for 2
                            # we want the cycle instead of just knowing that there's one
                            path_from_node = []
                            path_from_child = []
                            temp_node = node
                            temp_child = child
                            while temp_node != -1:
                                path_from_node.append(temp_node)
                                temp_node = parent_list[temp_node]
                            while temp_child != -1:
                                path_from_child.append(temp_child)
                                temp_child = parent_list[temp_child]

                            #meet point
                            i= len(path_from_node) -1
                            j = len(path_from_child) -1

                            while i >= 0 and j >= 0 and path_from_node[i] == path_from_child[j]:
                                i-=1
                                j-=1
                            cycle = path_from_node[:i +1] + path_from_child[j+1::-1]
                            #readd the first value at the end so that the cycle is closed
                            cycle.append(cycle[0])


    if False in visited :
        is_complete = False
    return visited, is_complete, cycle


def is_degen(proposal):
    E=0
    for i in proposal:
        for j in i:
            if j > 0 :
                E+=1
    V = len(proposal)+len(proposal[0])

    test = breadthfs(proposal)
    is_complete = test[1]
    is_cycle = len(test[2])
    if is_complete and is_cycle and E == V-1:
        return False
    elif is_cycle:
        return "cycle"  #has cycle
    elif E!= V-1:
        return "degen", E - (V-1)

def compute_potentials(cost_matrix, basic_cells_set):
    n = len(cost_matrix) # col
    m = len(cost_matrix[0]) # row
 
    u = [None] * n  #initiate at 0
    v = [None] * m  #initiate a 0 also since no value

    u[0] = 0 #initiate u0 = 0 as a starting point 

    while None in u or None in v:
        for i in range(n):
            if u[i] is None:
                u[i] = 0
                break
        changed = True
        while changed:
            changed = False

            for (i, j) in basic_cells_set:    #fuck this code
                #thats were the magic oppear we have
                if u[i] is not None and v[j] is None:

                    v[j] = cost_matrix[i][j] - u[i]
                    changed = True
                elif v[j] is not None and u[i] is None:
                    u[i] = cost_matrix[i][j] - v[j]
                    changed = True
    return u, v

def display_potentials(u, v):
    print("\nPOTENTIALS")

    print("Rows")
    for i in range(len(u)):
        print(f"u{i + 1} = {u[i]}")

    print("Cols")
    for j in range(len(v)):
        print(f"v{j + 1} = {v[j]}")


def display_matrix(matrix, title):
    n = len(matrix)
    m = len(matrix[0]) if n else 0
    width = 8

    print(f"\n{title}")
    print("".ljust(width) + "".join(f"C{j+1}".rjust(width) for j in range(m)))

    for i in range(n):
        row = f"P{i+1}".ljust(width)
        row += "".join(format_value(matrix[i][j], width) for j in range(m))
        print(row)

def compute_potential_costs(u, v):
    n = len(u)
    m = len(v)
    
    # for every cell (i,j), compute u[i] + v[j]
    potential_costs = []
    
    for i in range(n):
        row = []
        for j in range(m):
            row.append(u[i] + v[j])
        potential_costs.append(row)
    
    return potential_costs

def compute_marginal_costs(cost_matrix, basic_cells_set, u, v):
    n = len(cost_matrix)
    m = len(cost_matrix[0])
    # marginal[i][j]  None for basic cells
    # marginal[i][j] = cost[i][j] - (u[i] + v[j]) for non-basic cells
    marginal = [[None for _ in range(m)] for _ in range(n)]

    best_cell = None
    best_value = 0

    for i in range(n):
        for j in range(m):
            if (i, j) not in basic_cells_set:
                marginal[i][j] = cost_matrix[i][j] - (u[i] + v[j])
                # return the best value the minimum one which is negative to add it to it 
                if marginal[i][j] < best_value:
                    best_value = marginal[i][j]
                    best_cell = (i, j)
                    #update then the cell so that the variables contain it 

    return marginal, best_cell, best_value

#Because I care about my sanity we will convert the nodes in the cycle to real matrix input
def from_node_to_matrix(cycle, n): #n the number of provisions
    cells = []

    for k in range(len(cycle)-1):
        a =cycle[k]
        b =cycle[k+1]
        if a < n: # row to column
            i = a
            j = b - n
        else:
            i = b
            j = a - n
        cells.append((i, j))
    return cells

def fix_cycles(proposal, cycle_nodes, n, basic_cells_set, best_cell):

    cycle = from_node_to_matrix(cycle_nodes, n)

    if best_cell in cycle:
        index = cycle.index(best_cell)
        cycle = cycle[index:] + cycle[:index]
    delta = min(proposal[i][j] for k, (i, j) in enumerate(cycle) if k % 2 == 1)

    for k, (i, j) in enumerate(cycle):
        if k % 2 == 0:
            proposal[i][j] += delta
        else:
            proposal[i][j] -= delta

    # remove the variable (first zero in - position)
    for k in range(1, len(cycle), 2):
        i, j = cycle[k]
        if proposal[i][j] == 0:
            basic_cells_set.remove((i, j))
            break


    return proposal, basic_cells_set


def stepping_stone(cost_matrix, proposal, basic_cells_set, n, m):
    iteration = 1
    while True:
        print(f"\n============= STEPPING STONE: ITERATION {iteration} =============")
        if iteration > 3:
            break
        # 1. Degeneracy Fix (Using the set)
        if len(basic_cells_set) < n + m - 1:
            basic_cells_set = fix_degeneracy(basic_cells_set, n, m)

        u, v = compute_potentials(cost_matrix, basic_cells_set)

        marginal_costs, best_cell, best_value = compute_marginal_costs(cost_matrix, basic_cells_set, u, v)
        display_matrix(marginal_costs, "MARGINAL COSTS TABLE")

        if best_cell is None:
            print("\n>>> OPTIMAL SOLUTION FOUND. All marginal costs are >= 0")
            break

        print(f"\nBest improving edge: P{best_cell[0] + 1}->C{best_cell[1] + 1} with marginal cost {best_value}")

        # 5. Cycle Detection (The BFS Trick)
        proposal[best_cell[0]][best_cell[1]] = -1

        cells_to_reset = []
        for (i, j) in basic_cells_set:
            if proposal[i][j] == 0 and (i, j) != best_cell:
                proposal[i][j] = -1
                cells_to_reset.append((i, j))

        _, _, cycle_nodes = breadthfs(proposal, start_node=best_cell[0])

        proposal[best_cell[0]][best_cell[1]] = 0
        for (i, j) in cells_to_reset:
            proposal[i][j] = 0

        if not cycle_nodes:
            basic_cells_set.add(best_cell)
            for (i, j) in cells_to_reset:
                if (i,j) !=best_cell:
                    basic_cells_set.remove((i, j))
                    break

        basic_cells_set.add(best_cell)

        proposal, basic_cells_set = fix_cycles(proposal, cycle_nodes, n, basic_cells_set, best_cell)

        iteration += 1

    return proposal, basic_cells_set



def choose_problem_and_method():
    problem = input("Choose problem number (1-12): ").strip()
    method = input("Choose initial method (nw/bh): ").strip().lower()
    return problem, method


if __name__ == "__main__":
    problem, method = choose_problem_and_method()
    """ problem method initiated because we return the method and the problem
     the file will have as an argument the value return by method ChsePrblmMethod which is the user input 
     if we chose 6 the readfile takes 6 
    
    so we need multiple initialization to get the return argument of the function that we implement hence the multiple argument initiated
    """
    path, n, m, cost_matrix, provisions, orders = readfile(problem)
    print(f"\nLoaded file: {path}")
    print(f"Suppliers (n): {n}")
    print(f"Customers (m): {m}")
    print(f"Total provisions = {sum(provisions)} | Total orders = {sum(orders)}")

    display_cost_matrix(cost_matrix, provisions, orders)

    if method == "nw":
        proposal,total_cost = NorthWest(cost_matrix, provisions, orders)
    elif method == "bh":    
        proposal,total_cost = BalasHammer(cost_matrix, provisions, orders)
    else:
        print("Unknown method buddy your not a hacker trust me")
        exit()

    basic_cells = get_basic_cells(proposal) 
    basic_cells_set = set(basic_cells)


    status = is_degen(proposal)

    if status != 0:
        print("Degenerate solution my boy there is a problem")
        basic_cells_set = fix_degeneracy(basic_cells_set, n, m)
    #return the cells that are fulfilled after works of algo
    # Run the Master Loop!
    final_proposal, final_basic_cells = stepping_stone(cost_matrix, proposal, basic_cells_set, n, m)

    # Display the final, optimized results
    final_cost = calculate_total_cost(final_proposal, cost_matrix)
    display_transportation(final_proposal, cost_matrix, "FINAL OPTIMAL PROPOSAL")
    print(f"\nFinal Optimal Cost: {final_cost}")


