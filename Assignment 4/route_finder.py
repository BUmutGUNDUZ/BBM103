
from sys import argv

def main():
    int_file = argv[1]
    out_file = argv[2]

    with open(int_file,mode="r") as int_file:
        lines = int_file.readlines()
        locations = []
        for element in lines:
            if not element.strip():
                continue
            else:
                element = element.strip().split()
                locations.append(list(map(int, element)))
        cost1, cost2, cost3 = locations[0]
        locations.remove(locations[0])

        #The costs are copied to be stored in the same way as the map and are modified below.
        costs = [row[:] for row in locations]
        rows, columns = len(locations), len(locations[0])

        # In the code block below, the costs of all points are calculated sequentially.
        for i in range(rows):
            for j in range(columns):
                if locations[i][j] == 0:
                    costs[i][j] = 0
                    continue
                else:
                    left = j > 0 and locations[i][j - 1] == 0
                    right = j < columns - 1 and locations[i][j + 1] == 0
                    up = i > 0 and locations[i - 1][j] == 0
                    down = i < rows - 1 and locations[i + 1][j] == 0

                    up_left = i > 0 and j > 0 and locations[i -1][j - 1] == 0
                    up_right = i > 0 and j < columns - 1 and locations[i -1][j + 1] == 0
                    down_left = i < rows - 1 and j > 0 and locations[i +1][j - 1] == 0
                    down_right = i < rows - 1 and j < columns - 1 and locations[i+1][j + 1] == 0
                    
                if left or right or up or down:
                    costs[i][j] = cost3
                elif up_left or up_right or down_left or down_right:
                    costs[i][j] = cost2
                else:
                    costs[i][j] = cost1

        best_result = find_route(locations, costs, path=None, cost=0, visited=None, best_result=None)

    with open(out_file, mode="w") as out_file:
        if best_result['cost'] == float('inf'):
            out_file.write(f"There is no possible route!")
        else:
            out_file.write(f"Cost of the route: {best_result['cost']}\n")
            result_grid = [['1' if locations[i][j] == 1 else '0' for j in range(columns)] for i in range(rows)]
            for x, y in best_result['path']:
                result_grid[x][y] = 'X'
            out_file.write("\n".join(" ".join(row) for row in result_grid))

def find_route(locations, costs, path, cost, visited, best_result):
    rows, columns = len(locations), len(locations[0])

    if visited is None:
        visited = set()

    if best_result is None:
        best_result = {'cost': float('inf'), 'path': []}

    # It starts sequentially with all the ones on the left.
    if path is None:
        for i in range(rows):
            if locations[i][0] == 1:
                path = [(i, 0)]
                visited.add((i, 0))
                cost = costs[i][0]
                find_route(locations, costs, path, cost, visited, best_result)
        return best_result

    current_pos = path[-1]

    if cost >= best_result['cost']:
        return best_result

    # It checks whether the rightmost side has been reached.
    if current_pos[1] == columns - 1:
        if cost < best_result['cost']:
            best_result['cost'] = cost
            best_result['path'] = path[:]
        return best_result

    # Check Right
    if current_pos[1] + 1 < columns and (current_pos[0], current_pos[1] + 1) not in visited and locations[current_pos[0]][current_pos[1] + 1] == 1:
        visited.add((current_pos[0], current_pos[1] + 1))
        path.append((current_pos[0], current_pos[1] + 1))
        find_route(locations, costs, path, cost + costs[current_pos[0]][current_pos[1] + 1], visited, best_result)
        path.pop()
        visited.remove((current_pos[0], current_pos[1] + 1))

    # Check Up
    if current_pos[0] - 1 >= 0 and (current_pos[0] - 1, current_pos[1]) not in visited and locations[current_pos[0] - 1][current_pos[1]] == 1:
        visited.add((current_pos[0] - 1, current_pos[1]))
        path.append((current_pos[0] - 1, current_pos[1]))
        find_route(locations, costs, path, cost + costs[current_pos[0] - 1][current_pos[1]], visited, best_result)
        path.pop()
        visited.remove((current_pos[0] - 1, current_pos[1]))

    # Check Down
    if current_pos[0] + 1 < rows and (current_pos[0] + 1, current_pos[1]) not in visited and locations[current_pos[0] + 1][current_pos[1]] == 1:
        visited.add((current_pos[0] + 1, current_pos[1]))
        path.append((current_pos[0] + 1, current_pos[1]))
        find_route(locations, costs, path, cost + costs[current_pos[0] + 1][current_pos[1]], visited, best_result)
        path.pop()
        visited.remove((current_pos[0] + 1, current_pos[1]))

    # Check Left
    if current_pos[1] - 1 >= 0 and (current_pos[0], current_pos[1] - 1) not in visited and locations[current_pos[0]][current_pos[1] - 1] == 1:
        visited.add((current_pos[0], current_pos[1] - 1))
        path.append((current_pos[0], current_pos[1] - 1))
        find_route(locations, costs, path, cost + costs[current_pos[0]][current_pos[1] - 1], visited, best_result)
        path.pop()
        visited.remove((current_pos[0], current_pos[1] - 1))

    return best_result

if __name__ == '__main__':
    main()