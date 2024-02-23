from algorithm_plot import AlgorithmVisualizer
import copy, time

side_of_array = 0

class A_Star_node():
    def __init__(self, xy: tuple, diagonal: bool, goal_node: tuple, parent: object, is_start_node: tuple = False):
        x, y = xy
        self.ids = f"({str(x)}, {str(y)})"
        self.x = x
        self.y = y
        self.xy = xy
        if is_start_node:
            self.f = 0
        elif not diagonal:
            self.f = 10
        else:
            self.f = 14
        self.g = self._calculateG(goal_node)
        self.h = self.f + self.g
        self.parent = parent
    
    def _calculateG(self, goal_node):
        x, y = goal_node
        g = (abs(self.x - x) + abs(self.y - y)) * 10
        return g
    
def printArray(array):
    for row in array:
        for element in row:
            print(element, end=" ")  # Use end=" " to print elements in the same row
        print()

def getBestNode(open_list):
    if not open_list:
        return None
    best_score = open_list[0].h
    best_node = open_list[0]
    for node in open_list:
        if node.h < best_score:
            best_score = node.h
            best_node = node
    return best_node

def translateXYtoArray(xy: tuple, YX: bool = False) -> tuple:
    """Returns `(Y, X)` or `(X, Y)`"""
    x, y = xy
    new_y = (y + side_of_array - (2 * y))
    if YX:
        return (new_y, x)
    else:
        return (x, new_y)

def generateNeighbors(current_node, goal_xy, open_list, closed_list, array):
    i, j = translateXYtoArray(current_node.xy, YX=True) 
    for y in range(-1, 2):
        for x in range(-1, 2):
            if (y == 0 and x == 0):
                continue
            y_axis = i + y
            x_axis = j + x
            if y_axis < 0 or x_axis < 0 or y_axis > side_of_array or x_axis > side_of_array:
                continue
            if array[y_axis][x_axis] == 0:
                diagonal = False
                if abs(x + y) == 2 or x + y == 0:
                    diagonal = True
                generated_node = A_Star_node(xy=(translateXYtoArray((x_axis, y_axis), YX=False)), diagonal=diagonal, goal_node=goal_xy, parent=current_node)
                if closed_list.get(generated_node.ids):
                    continue
                else:
                    array[y_axis][x_axis] = 2
                    open_list.append(generated_node)

def findPath(node):
    path = [node]
    check_node = node.parent
    while (True):
        if check_node is None:
            break
        path.append(check_node)
        check_node = check_node.parent
    return path

def A_star(plot: AlgorithmVisualizer):
    start_xy = plot.start
    goal_xy = plot.end
    
    if start_xy is None:
        plot.errorMessage("* Start Coordinate is absent")
        return
    elif goal_xy is None:
        plot.errorMessage("* End Coordinate is absent")
        return
    else:
        plot.errorMessage("")
    #plot.drawAllSquares()
    
    global side_of_array
    side_of_array = plot.size - 1
    
    search_array = copy.deepcopy(plot.array)
    
    current_node = None
    open_list = []
    closed_list = {}
    
    path = []
    final_path = ""
    
    start_node = A_Star_node(xy=start_xy, diagonal=False, goal_node=goal_xy, parent=None, is_start_node=True)
    open_list.append(start_node)
    
    while(True):
        best_node = getBestNode(open_list)
        if best_node is None:
            plot.errorMessage(f"Solution doesn't exist")
            print("Solution doesn't exist")
            return
        open_list.remove(best_node)
        current_node = best_node
        
        if current_node.xy == goal_xy: # Arrived at goal
            print("Found Goal!")
            break
        
        generateNeighbors(current_node, goal_xy, open_list, closed_list, search_array)
        closed_list[current_node.ids] = current_node
    
    path = findPath(current_node)
    path.reverse()
    for num, node in enumerate(path):
        final_path += f"({str(node.x)},{str(node.y)})"
        final_path += " -> " if node != path[-1] else ""
        if (num + 1) % 3 == 0:
            final_path += "\n"
        time.sleep(0.05)
        if (node.xy != start_xy and node.xy != goal_xy):
            plot.drawSquare(node.xy, plot.blue)
    plot.errorMessage(f"Path:\n{final_path}")
    print(final_path)