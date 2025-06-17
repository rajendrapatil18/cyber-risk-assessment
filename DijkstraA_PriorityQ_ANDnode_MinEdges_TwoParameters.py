import heapq
import math

class DijkstraPriorityQANDnodeMinEdgesUtilityFunction:
    def __init__(self):
        self.distances = []
        self.pnodes = []
        self.settled = set()
        self.priority_queue = []
        self.number_of_nodes = 0
        self.adjacency_matrix_ttc = []
        self.adjacency_matrix_scp = []
        self.visited_and = []
        self.nodes = []
        self.NO_PARENT = -1
        self.parents = []
        self.stack = []
        self.cnt_path = 0
        self.path = []
        self.alpha = 0.0

    def dijkstra_algorithm(self, number_of_vertices, vertices, adjacency_matrix_ttc, adjacency_matrix_scp, source, destination, alpha_value):
        self.alpha = alpha_value
        self.cnt_path = 2
        self.number_of_nodes = number_of_vertices
        self.distances = [float('inf')] * (self.number_of_nodes + 1)
        self.pnodes = [0] * (self.number_of_nodes + 1)
        self.settled = set()
        self.priority_queue = []
        self.adjacency_matrix_ttc = [[float('inf')] * (self.number_of_nodes + 1) for _ in range(self.number_of_nodes + 1)]
        self.adjacency_matrix_scp = [[float('inf')] * (self.number_of_nodes + 1) for _ in range(self.number_of_nodes + 1)]
        self.nodes = [[0]*4 for _ in range(self.number_of_nodes)]
        self.parents = [self.NO_PARENT] * (self.number_of_nodes + 1)
        max_possible_edges = (self.number_of_nodes * (self.number_of_nodes - 1)) // 2
        self.stack = [0] * max_possible_edges
        self.path = [0.0] * max_possible_edges
        self.visited_and = [0.0] * max_possible_edges

        for i in range(number_of_vertices):
            for j in range(3):
                self.nodes[i][j] = vertices[i][j]

        for i in range(number_of_vertices):
            for j in range(number_of_vertices):
                u = vertices[i][0]
                v = vertices[j][0]
                self.adjacency_matrix_ttc[u][v] = adjacency_matrix_ttc[u][v]
                self.adjacency_matrix_scp[u][v] = adjacency_matrix_scp[u][v]

        for i in range(number_of_vertices):
            node_id = self.nodes[i][0]
            if self.nodes[i][1] == 1:  # AND node
                self.distances[node_id] = -77283  # Special value for AND nodes
            else:
                self.distances[node_id] = float('inf')
            self.pnodes[node_id] = 0
            if i < len(self.visited_and):
                self.visited_and[i] = 0

        self.parents[source] = self.NO_PARENT
        heapq.heappush(self.priority_queue, (0, source))
        self.distances[source] = 0
        self.pnodes[source] = 0

        while self.priority_queue:
            evaluation_node = self.get_node_with_minimum_distance()
            self.settled.add(evaluation_node)
            self.evaluate_neighbors(evaluation_node, destination)

        if self.distances[destination] != float('inf'):
            self.print_solution(source, destination)
            if self.visited_and[0] > 0:
                path_length = int(self.path[1])
                self.path[path_length] = self.visited_and[0]
                for an in range(int(self.visited_and[0])):
                    self.path[(an * 2 + 1) + path_length] = self.visited_and[(an * 2 + 1)]
                    self.path[(an * 2 + 2) + path_length] = self.visited_and[(an * 2 + 2)]
        else:
            self.path[1] = -1

        return self.path

    def get_node_with_minimum_distance(self):
        cost, node = heapq.heappop(self.priority_queue)
        return node

    def evaluate_neighbors(self, evaluation_node, destination):
        try:
            for child in range(self.number_of_nodes):
                child_node = self.nodes[child][0]
                if child_node not in self.settled:
                    if self.adjacency_matrix_ttc[evaluation_node][child_node] != float('inf'):
                        edge_distance = (self.alpha * self.adjacency_matrix_ttc[evaluation_node][child_node]) + \
                                      ((1 - self.alpha) * (math.log10(1 / self.adjacency_matrix_scp[evaluation_node][child_node])))
                        new_distance = self.distances[evaluation_node] + edge_distance
                        prenodes = self.pnodes[evaluation_node] + 1

                        if self.nodes[child][1] == 1:  # AND node
                            if self.distances[child_node] <= new_distance:
                                self.distances[child_node] = new_distance
                                self.pnodes[child_node] = prenodes
                                self.parents[child_node] = evaluation_node
                            
                            self.nodes[child][2] -= 1  # Decrement parent count
                            
                            if self.nodes[child][2] == 0:
                                heapq.heappush(self.priority_queue, (self.distances[child_node], child_node))
                                self.visited_and[int(self.visited_and[0]) * 2 + 1] = child_node
                                self.visited_and[int(self.visited_and[0]) * 2 + 2] = evaluation_node
                                self.visited_and[0] += 1
                        else:  # Regular node
                            if new_distance == self.distances[child_node] and prenodes < self.pnodes[child_node]:
                                self.parents[child_node] = evaluation_node
                                self.pnodes[child_node] = prenodes
                                heapq.heappush(self.priority_queue, (self.distances[child_node], child_node))
                            
                            if new_distance < self.distances[child_node]:
                                self.parents[child_node] = evaluation_node
                                self.distances[child_node] = new_distance
                                self.pnodes[child_node] = prenodes
                                heapq.heappush(self.priority_queue, (self.distances[child_node], child_node))
        except Exception as e:
            print(f"\nSource: {e}")

    def print_solution(self, source, destination):
        print(f"\nSource: {source} Destination: {destination} Destination dist: {self.distances[destination]}")
        self.print_path(destination)
        self.path[0] = self.distances[destination]
        self.path[1] = float(self.cnt_path)

    def print_path(self, current_vertex):
        if current_vertex == self.NO_PARENT:
            return
        self.print_path(self.parents[current_vertex])
        self.path[self.cnt_path] = float(current_vertex)
        self.cnt_path += 1
        print(f"\n{self.cnt_path} :currentVertex: {current_vertex}")


def main():
    print("The graph is loaded from the file...!!!")
    
    # Initialize data structures
    vertices_dictionary = [["-1", "0", ""] for _ in range(15000)]
    defense_dictionary = [["-1", ""] for _ in range(1000)]
    nop_dictionary = [["-1", ""] for _ in range(1000)]
    
    edges = [[0, 0, 0] for _ in range(25000)]
    edge_ttc = [0.0] * 25000
    edge_scp = [0.0] * 25000
    
    number_of_edges = 0
    vercnt = 0
    defcnt = 0
    nopcnt = 0
    
    try:
        with open("sg_and.csv", "r") as file:
            for line in file:
                edge_description = line.strip().split(",")
                if len(edge_description) > 3:
                    edges[number_of_edges][0] = int(edge_description[0])
                    edges[number_of_edges][1] = int(edge_description[1])
                    edge_ttc[number_of_edges] = float(edge_description[2])
                    edge_scp[number_of_edges] = float(edge_description[3])
                    
                    nodecode = edge_description[4]
                    nodetype = edge_description[5]
                    nodedesc = edge_description[6]
                    dcode = edge_description[7]
                    defdesc = edge_description[8]
                    nopcode = edge_description[9]
                    nopdesc = edge_description[10]
                    
                    # Check if node exists in vertices_dictionary
                    found = any(nodecode == item[0] for item in vertices_dictionary)
                    if not found:
                        vertices_dictionary[vercnt][0] = nodecode
                        vertices_dictionary[vercnt][1] = nodetype
                        vertices_dictionary[vercnt][2] = nodedesc
                        vercnt += 1
                    
                    # Check if defense exists in defense_dictionary
                    dfound = any(dcode == item[0] for item in defense_dictionary)
                    if not dfound:
                        defense_dictionary[defcnt][0] = dcode
                        defense_dictionary[defcnt][1] = defdesc
                        defcnt += 1
                    
                    # Check if nop exists in nop_dictionary
                    nopfound = any(nopcode == item[0] for item in nop_dictionary)
                    if not nopfound:
                        nop_dictionary[nopcnt][0] = nopcode
                        nop_dictionary[nopcnt][1] = nopdesc
                        nopcnt += 1
                    
                    number_of_edges += 1
    except Exception as e:
        print(f"Something wrong: {e}")
    
    number_of_vertices = vercnt
    print(f"Number of vertices: {number_of_vertices}")
    print(f"Number of edges: {number_of_edges}")
    print("Defences: ")
    
    for i in range(defcnt - 1):
        print(f"{i+1}: {defense_dictionary[i][0]}-{defense_dictionary[i][1]}")
    
    print("Nop: ")
    for i in range(nopcnt - 1):
        print(f"{i+1}: {nop_dictionary[i][0]}-{nop_dictionary[i][1]}")
    
    print("Which Defence/s you want to enable?: ")
    moredef = 1
    edefcount = 0
    edefences = [0] * defcnt
    
    while moredef == 1:
        edefences[edefcount] = int(input("Enter the defence code: "))
        edefcount += 1
        moredef = int(input("Do you want to enable more defences? Yes=1/No=0 "))
    
    # Process edges based on enabled defenses and NOPs
    for i in range(number_of_edges):
        alldef = any(edges[i][0] == int(defense_dictionary[j][0]) for j in range(defcnt - 1))
        endef = any(edges[i][0] == edefences[k] for k in range(edefcount))
        nopc = any(edges[i][0] == int(nop_dictionary[m][0]) for m in range(nopcnt - 1))
        
        if alldef and not endef:
            edges[i][0] = edges[1][0]
            edges[i][1] = edges[1][1]
            edge_ttc[i] = edge_ttc[1]
            edge_scp[i] = edge_scp[1]
        
        if nopc:
            edges[i][0] = edges[1][0]
            edges[i][1] = edges[1][1]
            edge_ttc[i] = edge_ttc[1]
            edge_scp[i] = edge_scp[1]
    
    # Initialize vertices
    vertices = [[0]*3 for _ in range(number_of_vertices)]
    for i in range(number_of_vertices):
        vertices[i][0] = int(vertices_dictionary[i][0])  # node
        vertices[i][1] = int(vertices_dictionary[i][1])  # node type
        vertices[i][2] = 0  # for storing number of parent
    
    # Initialize adjacency matrices
    adjacency_matrix_ttc = [[float('inf')] * (number_of_vertices + 1) for _ in range(number_of_vertices + 1)]
    adjacency_matrix_scp = [[float('inf')] * (number_of_vertices + 1) for _ in range(number_of_vertices + 1)]
    
    for i in range(number_of_vertices):
        for j in range(number_of_vertices):
            u = vertices[i][0]
            v = vertices[j][0]
            if u == v:
                adjacency_matrix_ttc[u][v] = 0
                adjacency_matrix_scp[u][v] = 0
            else:
                adjacency_matrix_ttc[u][v] = float('inf')
                adjacency_matrix_scp[u][v] = float('inf')
    
    source = 0
    destination = int(input("Enter the destination: "))
    print(f"\nSource: {source}\tDestination: {destination}\n")
    
    # Populate adjacency matrices and count parents for AND nodes
    for i in range(number_of_edges):
        u = edges[i][0]
        v = edges[i][1]
        sigma_2 = (edge_ttc[i] * edge_ttc[i]) / 12
        adjacency_matrix_ttc[u][v] = (edge_ttc[i] / 2) - sigma_2
        adjacency_matrix_scp[u][v] = edge_scp[i]
        
        for j in range(number_of_vertices):
            if vertices[j][0] == v and vertices[j][1] == 1:
                vertices[j][2] += 1
    
    alpha = 0.5
    dpqm = DijkstraPriorityQANDnodeMinEdgesUtilityFunction()
    spath = dpqm.dijkstra_algorithm(number_of_vertices, vertices, adjacency_matrix_ttc, adjacency_matrix_scp, source, destination, alpha)
    
    if spath[1] != -1:
        print("\nThe Shortest Path is:", end="")
        for i in range(2, int(spath[1])):
            print(f"-{int(spath[i])}", end="")
        print(f"\twith cost: {spath[0]}\n", end="")
        
        for i in range(2, int(spath[1])):
            for j in range(vercnt):
                if str(int(spath[i])) == vertices_dictionary[j][0]:
                    print(f"-{vertices_dictionary[j][2]}", end="")
        print(f"\twith cost: {spath[0]}")
        
        print("And nodes and parents:", end="")
        path_length = int(spath[1])
        for an in range(int(spath[path_length])):
            print(f"-{int(spath[(an * 2 + 1) + path_length])}-{int(spath[(an * 2 + 2) + path_length])}", end="")
    else:
        print("\nThere is no path !!!")

if __name__ == "__main__":
    main()