
def readfile(file):
    path="src/Problems/Problem" + str(file) + ".txt"
    with open(path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    firstLine = lines[0].split()
    numProvision = int(firstLine[0])
    numOrders = int(firstLine[1])
    print(numProvision, numOrders)
    cost_matrix = []
    provisions = []
    orders = []

    for i in range(1, numProvision + 1):
        parts = lines[i].split()
        row_costs = [int(x) for x in parts[:numOrders]]
        cost_matrix.append(row_costs)

        provisions.append(int(parts[-1]))
    orders_line =  lines[numProvision + 1].split()
    orders = [int(x) for x in orders_line]

    print("Suppliers (n):", numProvision)
    print("Customers (m):", numOrders)
    print("Cost Matrix:", cost_matrix)
    print("Provisions:", provisions)
    print("Orders:", orders)

    print("North West")

    startR = 0  # start row
    startC = 0  # start col
    ans = 0
    # loop runs until it reaches the bottom right corner
    while (startR != len(cost_matrix) and startC != len(cost_matrix[0])):
        # if demand is greater than supply
        if (provisions[startR] <= orders[startC]):
            ans += provisions[startR] * cost_matrix[startR][startC]
            # subtract the value of supply from the demand
            orders[startC] -= provisions[startR]
            startR += 1
        # if supply is greater than demand
        else:
            ans += orders[startC] * cost_matrix[startR][startC]
            # subtract the value of demand from the supply
            provisions[startR] -= orders[startC]
            startC += 1

    print("The initial feasible basic solution is ", ans)

    return path, numProvision, numOrders, cost_matrix, provisions, orders



def NorthWest (cost_matrix, provisions, orders):
    print("North West")
    num_suppliers = len(provisions)
    num_customers = len(orders)
    row = 0  # start row
    col = 0  # start col
    total_cost = 0

    prov_left = provisions.copy()
    ord_left = orders.copy()

    proposal = [[0 for j in range(num_customers)] for i in range(num_suppliers)]

    while (row < num_suppliers and col < num_customers):
        allocated = min(prov_left[row], ord_left[col])
        proposal[row][col] = allocated
        total_cost += allocated * cost_matrix[row][col]
        prov_left[row] -= allocated
        ord_left[col] -= allocated
        if prov_left[row] == 0:
            row += 1
        if ord_left[col] == 0:
            col += 1

    print("Total Cost:", total_cost)
    return proposal, total_cost







if __name__ == '__main__':
    readfile("2")

