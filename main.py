
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
    return numProvision, numOrders, cost_matrix, provisions, orders


if __name__ == '__main__':
    readfile("2")
