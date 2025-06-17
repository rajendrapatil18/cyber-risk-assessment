import sys
from typing import List, Dict, Set

class AllpathsAnode:
    def __init__(self, no_of_vertices: int):
        self.v = no_of_vertices
        self.adjList = [[] for _ in range(no_of_vertices)]  # Adjacency list
        self.allpaths = [""] * 100000  # To store all found paths
        self.ap = 1  # Path counter

    def add_edge(self, u: int, v: int):
        """Add edge to the adjacency list"""
        self.adjList[u].append(v)

    def print_all_paths(self, s: int, d: int, no_of_vertices: int, vertices: List[List[int]]):
        """Find all paths from s to d, handling AND nodes"""
        isVisited = [False] * self.v
        pathList = [s]
        self._print_all_paths_util(s, d, no_of_vertices, vertices, isVisited, pathList)

    def _print_all_paths_util(self, u: int, d: int, no_of_vertices: int, vertices: List[List[int]], 
                            isVisited: List[bool], localPathList: List[int]):
        """Recursive helper function to find all paths"""
        if u == d:
            # Destination reached, store the path if unique
            newpath = str(localPathList)
            if newpath not in self.allpaths[:self.ap]:
                self.allpaths[self.ap] = newpath
                self.ap += 1
            return

        isVisited[u] = True

        for i in self.adjList[u]:
            if not isVisited[i]:
                localPathList.append(i)
                print(f"\t\tAdd vertex {i} to the localPathList")
                print(f"\t\tlocalPathList: {localPathList}")
                
                # Find the index of vertex i in vertices array
                verindex = -1
                for j in range(no_of_vertices):
                    if vertices[j][0] == i:
                        verindex = j
                        break

                if verindex != -1 and vertices[verindex][1] == 1:  # If i is an AND node
                    pflag = 0
                    # Check if current parent u is in unvisited parent list of i
                    for aparents in range(vertices[verindex][2]):
                        if u == vertices[verindex][3 + aparents]:
                            pflag = 1
                            vertices[verindex][3 + aparents] = -1  # Mark parent as visited

                    if pflag == 1:
                        clplsize = len(localPathList)
                        # Update local path list if current path is shorter
                        if clplsize <= vertices[verindex][vertices[verindex][2] + 3]:
                            vertices[verindex][vertices[verindex][2] + 3] = clplsize
                            for k in range(clplsize):
                                vertices[verindex][vertices[verindex][2] + 4 + k] = localPathList[k]

                        # Check if all parents are visited
                        allpflag = 0
                        for aparents in range(vertices[verindex][2]):
                            if vertices[verindex][3 + aparents] != -1:
                                allpflag = 1
                                break

                        if allpflag == 0:
                            # All parents visited, use stored local path
                            andlocalpathList = []
                            for k in range(vertices[verindex][vertices[verindex][2] + 3]):
                                andlocalpathList.append(vertices[verindex][vertices[verindex][2] + 4 + k])
                            
                            self._print_all_paths_util(i, d, no_of_vertices, vertices, isVisited, andlocalpathList)
                            localPathList.remove(i)
                        else:
                            localPathList.remove(i)
                    else:
                        localPathList.remove(i)
                else:  # Regular OR node
                    self._print_all_paths_util(i, d, no_of_vertices, vertices, isVisited, localPathList)
                    localPathList.remove(i)

        isVisited[u] = False

    def find_all_paths(self, vertices: List[List[int]], edges: List[List[int]], 
                      no_of_vertices: int, no_of_edges: int, s: int, d: int) -> List[str]:
        """Find all paths from s to d in the graph"""
        # Build the graph
        for e in range(no_of_edges):
            self.add_edge(edges[e][0], edges[e][1])
        
        self.print_all_paths(s, d, no_of_vertices, vertices)
        self.allpaths[0] = str(self.ap - 1)  # Store count of paths
        self.ap = 1  # Reset counter
        return self.allpaths


def main():
    try:
        vertices = []
        edges = []
        vertices_dictionary = [["-1", "0", ""] for _ in range(15000)]
        defense_dictionary = [["-1", ""] for _ in range(1000)]
        nop_dictionary = [["-1", ""] for _ in range(1000)]
        
        number_of_vertices = 0
        number_of_edges = 0
        number_of_defences = 0
        number_of_noparent_nodes = 0
        source = 0
        destination = 0

        # Read graph from file
        try:
            with open("sg_and.csv", "r") as file:
                for line in file:
                    edge_description = line.strip().split(",")
                    if len(edge_description) > 3:
                        edges.append([int(edge_description[0]), int(edge_description[1])])
                        
                        nodecode = edge_description[4]
                        nodetype = edge_description[5]
                        nodedesc = edge_description[6]
                        defcode = edge_description[7]
                        defdesc = edge_description[8]
                        nopcode = edge_description[9]
                        nopdesc = edge_description[10]
                        
                        # Add vertex if new
                        if not any(nodecode == item[0] for item in vertices_dictionary[:number_of_vertices]):
                            vertices_dictionary[number_of_vertices][0] = nodecode
                            vertices_dictionary[number_of_vertices][1] = nodetype
                            vertices_dictionary[number_of_vertices][2] = nodedesc
                            number_of_vertices += 1
                        
                        # Add defense if new
                        if not any(defcode == item[0] for item in defense_dictionary[:number_of_defences]):
                            defense_dictionary[number_of_defences][0] = defcode
                            defense_dictionary[number_of_defences][1] = defdesc
                            number_of_defences += 1
                        
                        # Add nop node if new
                        if not any(nopcode == item[0] for item in nop_dictionary[:number_of_noparent_nodes]):
                            nop_dictionary[number_of_noparent_nodes][0] = nopcode
                            nop_dictionary[number_of_noparent_nodes][1] = nopdesc
                            number_of_noparent_nodes += 1
                        
                        number_of_edges += 1
        except Exception as e:
            print(f"Error reading file: {e}")
            return

        print(f"Number of vertices: {number_of_vertices}")
        print(f"Number of edges: {number_of_edges}")
        print("Defences: ")
        for i in range(number_of_defences - 1):
            print(f"{i+1}: {defense_dictionary[i][0]}-{defense_dictionary[i][1]}")
        
        print("Noparent nodes: ")
        for i in range(number_of_noparent_nodes - 1):
            print(f"{i+1}: {nop_dictionary[i][0]}-{nop_dictionary[i][1]}")

        # Enable defenses
        enabled_defences = input("Enter Defence/s you want to enable (integer values separated by comma): ")
        enabled_defences_array = [int(x.strip()) for x in enabled_defences.split(",")]

        # Process edges based on enabled defenses and NOP nodes
        for i in range(number_of_edges):
            alldef = any(edges[i][0] == int(defense_dictionary[j][0]) for j in range(number_of_defences - 1))
            endef = any(edges[i][0] == ed for ed in enabled_defences_array)
            nopc = any(edges[i][0] == int(nop_dictionary[m][0]) for m in range(number_of_noparent_nodes - 1))

            if (alldef and not endef) or nopc:
                edges[i][0] = edges[1][0] if len(edges) > 1 else 0
                edges[i][1] = edges[1][1] if len(edges) > 1 else 0

        # Initialize vertices array
        vertices = [[0] * 1000 for _ in range(number_of_vertices)]
        for i in range(number_of_vertices):
            vertices[i][0] = int(vertices_dictionary[i][0])  # node
            vertices[i][1] = int(vertices_dictionary[i][1])  # node type
            vertices[i][2] = 0  # number of parents

        # Set destination
        source = 0
        destination = int(input("Enter the destination: "))
        print(f"\nSource: {source}\tDestination: {destination}\n")

        # Count parents for AND nodes and initialize their data
        for i in range(number_of_edges):
            u, v = edges[i][0], edges[i][1]
            for j in range(number_of_vertices):
                if vertices[j][0] == v and vertices[j][1] == 1:
                    vertices[j][2] += 1  # increment parent count
                    vertices[j][vertices[j][2] + 2] = u  # store parent
                    vertices[j][vertices[j][2] + 3] = 1000  # initialize local path list size

        # Find all paths
        g = AllpathsAnode(number_of_vertices)
        allpaths = g.find_all_paths(vertices, edges, number_of_vertices, number_of_edges, source, destination)
        
        ap = int(allpaths[0])
        print(f"\nAll paths in iteration are: {ap}\n")
        for p in range(1, ap + 1):
            print(f"{p}: {allpaths[p]}")

    except Exception as e:
        print(f"Exception in main: {e}")


if __name__ == "__main__":
    main()