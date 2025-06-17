import math
import heapq
from typing import List, Tuple, Dict

class YenkspDijpqAnodeDijpqMinedgesUtfun:
    def __init__(self):
        self.path = []
        self.path_weights = []
        self.temp_path = []
        self.spurNode = 0
        self.ad_mat_ttc = []
        self.ad_mat_sp = []
        self.copyadj_mat_ttc = []
        self.copyadj_mat_sp = []
        self.copyvertices = []
        self.allkpaths = ""
        self.allkpathsweights = ""
        self.allkpathswithweights = ""

    def findkshortestpaths(self, K: int, no_of_vertices: int, vertices: List[List[int]], 
                          no_of_edges: int, edges: List[List[int]], 
                          adj_mat_ttc: List[List[float]], adj_mat_sp: List[List[float]], 
                          source: int, destination: int, alpha: float) -> str:
        
        self.copyvertices = [[0]*5 for _ in range(no_of_vertices)]
        
        try:
            print(f"\nStart YEN's Algo over graph: {alpha}")
            
            self.allkpaths = ""
            self.allkpathsweights = ""
            self.allkpathswithweights = ""
            total_temp_paths = 0
            
            # Initialize matrices with extra space
            max_nodes = no_of_vertices + 1000
            self.ad_mat_ttc = [[float('inf')] * max_nodes for _ in range(max_nodes)]
            self.ad_mat_sp = [[float('inf')] * max_nodes for _ in range(max_nodes)]
            self.copyadj_mat_ttc = [[float('inf')] * max_nodes for _ in range(max_nodes)]
            self.copyadj_mat_sp = [[float('inf')] * max_nodes for _ in range(max_nodes)]
            
            self.path = [[0.0]*no_of_vertices for _ in range(K)]
            self.temp_path = [[0.0]*no_of_vertices for _ in range(no_of_vertices*10)]
            
            # Copy vertices
            for i in range(no_of_vertices):
                for j in range(5):
                    self.copyvertices[i][j] = vertices[i][j]
            
            # Copy adjacency matrices
            for i in range(no_of_vertices):
                for j in range(no_of_vertices):
                    u = vertices[i][0]
                    v = vertices[j][0]
                    self.copyadj_mat_ttc[u][v] = adj_mat_ttc[u][v]
                    self.copyadj_mat_sp[u][v] = adj_mat_sp[u][v]
            
            # Get first shortest path using Dijkstra
            dpamuf = DijkstraPriorityQANDnodeMinEdgesUtilityFunction()
            self.path[0] = dpamuf.dijkstra_algorithm(no_of_vertices, self.copyvertices, 
                                                    adj_mat_ttc, adj_mat_sp, 
                                                    source, destination, alpha)
            
            if self.path[0][1] != -1:
                print("\nFirstpath:", end="")
                for i in range(2, int(self.path[0][1])):
                    print(f"-{int(self.path[0][i])}", end="")
                print(f" Cost: {self.path[0][0]}")
                
                print("\nAnd nodes and parents:", end="")
                pathlength = int(self.path[0][1])
                
                # Remove edges for AND nodes
                for an in range(int(self.path[0][pathlength])):
                    for i in range(no_of_vertices):
                        if self.copyvertices[i][0] != int(self.path[0][((an*2)+2)+pathlength]):
                            u = self.copyvertices[i][0]
                            v = int(self.path[0][((an*2)+1)+pathlength])
                            self.copyadj_mat_ttc[u][v] = float('inf')
                            self.copyadj_mat_sp[u][v] = float('inf')
                            print(f"\nRemoved edges:{u}-{v}")
                
                # Find K-1 additional paths
                for k in range(1, K):
                    spurPath = [0.0] * no_of_vertices
                    totalPath = [0.0] * no_of_vertices
                    
                    for n in range(2, int(self.path[k-1][1])):
                        # Reset adjacency matrices for this iteration
                        for i in range(no_of_vertices):
                            for j in range(no_of_vertices):
                                u = self.copyvertices[i][0]
                                v = self.copyvertices[j][0]
                                self.ad_mat_ttc[u][v] = self.copyadj_mat_ttc[u][v]
                                self.ad_mat_sp[u][v] = self.copyadj_mat_sp[u][v]
                        
                        if self.path[k-1][n] != destination:
                            self.spurNode = self.path[k-1][n]
                            rootpathlength = 0.0
                            
                            if n > 2:
                                print(f"{int(self.path[k-1][2])}-", end="")
                                for i in range(2, n+1):
                                    if i != n:
                                        u = int(self.path[k-1][i])
                                        v = int(self.path[k-1][i+1])
                                        ttc = self.ad_mat_ttc[u][v]
                                        scp = self.ad_mat_sp[u][v]
                                        rootpathlength += (alpha * ttc) + ((1-alpha) * (math.log10(1/scp)))
                            
                            # Remove edges from previous paths
                            for p in range(k):
                                flag = 0
                                for m in range(2, n+1):
                                    if self.path[p][m] == self.path[k-1][m]:
                                        flag = 1
                                        break
                                
                                if flag == 1:
                                    u = int(self.path[p][n])
                                    v = int(self.path[p][n+1])
                                    self.ad_mat_ttc[u][v] = float('inf')
                            
                            # Remove nodes from root path
                            for m in range(2, n):
                                for i in range(no_of_edges):
                                    if self.path[k-1][m] == edges[i][0] or self.path[k-1][m] == edges[i][1]:
                                        u = edges[i][0]
                                        v = edges[i][1]
                                        self.ad_mat_ttc[u][v] = float('inf')
                            
                            # Find spur path from spur node to destination
                            new_source = int(self.path[k-1][n])
                            dpqm = DijkstraPriorityQMinEdgesUtilityFunction()
                            spurPath = dpqm.dijkstra_algorithm(no_of_vertices, self.copyvertices, 
                                                             self.ad_mat_ttc, self.ad_mat_sp, 
                                                             new_source, destination, alpha)
                            
                            if spurPath[1] != -1:
                                tp = 2
                                if n > 2:
                                    for i in range(2, n):
                                        totalPath[tp] = self.path[k-1][i]
                                        tp += 1
                                
                                for i in range(2, int(spurPath[1])):
                                    totalPath[tp] = spurPath[i]
                                    tp += 1
                                
                                totalPath[0] = spurPath[0] + rootpathlength
                                totalPath[1] = tp
                                
                                # Add to temp paths if not duplicate
                                if total_temp_paths == 0:
                                    for i in range(int(totalPath[1])):
                                        self.temp_path[total_temp_paths][i] = totalPath[i]
                                    total_temp_paths += 1
                                else:
                                    check = 0
                                    for temp_path_no in range(total_temp_paths):
                                        flag1 = 0
                                        for pn in range(2, int(totalPath[1])):
                                            if totalPath[pn] != self.temp_path[temp_path_no][pn]:
                                                flag1 = 1
                                                break
                                        
                                        if flag1 == 0:
                                            check = 1
                                            break
                                    
                                    if check != 1:
                                        for i in range(int(totalPath[1])):
                                            self.temp_path[total_temp_paths][i] = totalPath[i]
                                        total_temp_paths += 1
                    
                    # Find the minimum cost path among temp paths
                    min_cost = float('inf')
                    min_edges = float('inf')
                    found_index = 0
                    
                    for temp_path_no in range(total_temp_paths):
                        if self.temp_path[temp_path_no][0] == min_cost and min_edges > self.temp_path[temp_path_no][1]:
                            min_edges = self.temp_path[temp_path_no][1]
                            found_index = temp_path_no
                        elif self.temp_path[temp_path_no][0] < min_cost:
                            min_cost = self.temp_path[temp_path_no][0]
                            min_edges = self.temp_path[temp_path_no][1]
                            found_index = temp_path_no
                    
                    # Store the found path
                    for i in range(int(self.temp_path[found_index][1])):
                        self.path[k][i] = self.temp_path[found_index][i]
                    
                    # Mark this path as used
                    self.temp_path[found_index][0] = 1001.0
            
            # Prepare output strings
            for k in range(K):
                for pn in range(int(self.path[k][1])):
                    if 2 <= pn < self.path[k][1]-1:
                        self.allkpaths += f"{int(self.path[k][pn])}-"
                    elif pn == self.path[k][1]-1:
                        self.allkpaths += f"{int(self.path[k][pn])}"
                    elif pn == 0:
                        self.allkpathsweights += f"{self.path[k][pn]}"
                
                self.allkpaths += "@"
                self.allkpathsweights += "@"
            
            self.allkpathswithweights = self.allkpaths + self.allkpathsweights
            
            # Reset matrices
            for i in range(no_of_vertices):
                for j in range(no_of_vertices):
                    u = self.copyvertices[i][0]
                    v = self.copyvertices[j][0]
                    self.copyadj_mat_ttc[u][v] = float('inf')
                    self.copyadj_mat_sp[u][v] = float('inf')
        
        except Exception as yenex:
            print(f"In Yen {yenex}")
        
        return self.allkpathswithweights


class DijkstraPriorityQANDnodeMinEdgesUtilityFunction:
    # This would be the same implementation as provided in the previous conversion
    pass


class DijkstraPriorityQMinEdgesUtilityFunction:
    # This would be a simplified version without AND node handling
    pass


def main():
    import sys
    from collections import defaultdict
    
    no_of_edges = 0
    no_of_vertices = 3000
    source = 0
    destination = 221
    vercnt = 0
    defcnt = 0
    nopcnt = 0
    
    edges = [[0, 0] for _ in range(25000)]
    edge_ttc = [0.0] * 25000
    edge_scp = [0.0] * 25000
    
    vertices_dictionary = [["-1", "0", ""] for _ in range(15000)]
    defense_dictionary = [["-1", ""] for _ in range(1000)]
    nop_dictionary = [["-1", ""] for _ in range(1000)]
    
    try:
        print("The graph is loaded from the file...!!!")
        with open("sg_and.csv", "r") as file:
            for line in file:
                edge_description = line.strip().split(",")
                if len(edge_description) > 3:
                    edges[no_of_edges][0] = int(edge_description[0].strip())
                    edges[no_of_edges][1] = int(edge_description[1].strip())
                    edge_ttc[no_of_edges] = float(edge_description[2].strip())
                    edge_scp[no_of_edges] = float(edge_description[3].strip())
                    
                    nodecode = edge_description[4]
                    nodetype = edge_description[5]
                    nodedesc = edge_description[6]
                    dcode = edge_description[7]
                    defdesc = edge_description[8]
                    nopcode = edge_description[9]
                    nopdesc = edge_description[10]
                    
                    # Check if node exists
                    found = False
                    for h in range(vercnt+1):
                        if nodecode == vertices_dictionary[h][0]:
                            found = True
                            break
                    
                    if not found:
                        vertices_dictionary[vercnt][0] = nodecode
                        vertices_dictionary[vercnt][1] = nodetype
                        vertices_dictionary[vercnt][2] = nodedesc
                        vercnt += 1
                    
                    # Check if defense exists
                    dfound = False
                    for h in range(defcnt+1):
                        if dcode == defense_dictionary[h][0]:
                            dfound = True
                            break
                    
                    if not dfound:
                        defense_dictionary[defcnt][0] = dcode
                        defense_dictionary[defcnt][1] = defdesc
                        defcnt += 1
                    
                    # Check if nop exists
                    nopfound = False
                    for h in range(nopcnt+1):
                        if nopcode == nop_dictionary[h][0]:
                            nopfound = True
                            break
                    
                    if not nopfound:
                        nop_dictionary[nopcnt][0] = nopcode
                        nop_dictionary[nopcnt][1] = nopdesc
                        nopcnt += 1
                    
                    no_of_edges += 1
    except Exception as e:
        print(f"Something wrong: {e}")
    
    no_of_vertices = vercnt
    print(f"Number of vertices: {no_of_vertices}")
    print(f"Number of edges: {no_of_edges}")
    print("Defences: ")
    
    for i in range(defcnt-1):
        print(f"{i+1}: {defense_dictionary[i][0]}-{defense_dictionary[i][1]}")
    
    print("Nop: ")
    for i in range(nopcnt-1):
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
    for i in range(no_of_edges):
        alldef = any(edges[i][0] == int(defense_dictionary[j][0]) for j in range(defcnt-1))
        endef = any(edges[i][0] == edefences[k] for k in range(edefcount))
        nopc = any(edges[i][0] == int(nop_dictionary[m][0]) for m in range(nopcnt-1))
        
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
    vertices = [[0]*5 for _ in range(no_of_vertices)]
    for i in range(no_of_vertices):
        vertices[i][0] = int(vertices_dictionary[i][0])  # node
        vertices[i][1] = int(vertices_dictionary[i][1])  # node type
        vertices[i][2] = 0  # for storing number of parent
    
    # Initialize adjacency matrices
    adj_mat_ttc = [[float('inf')] * (no_of_vertices + 1) for _ in range(no_of_vertices + 1)]
    adj_mat_sp = [[float('inf')] * (no_of_vertices + 1) for _ in range(no_of_vertices + 1)]
    
    for i in range(no_of_vertices):
        for j in range(no_of_vertices):
            u = vertices[i][0]
            v = vertices[j][0]
            if u == v:
                adj_mat_ttc[u][v] = 0.0
                adj_mat_sp[u][v] = 0.0
            else:
                adj_mat_ttc[u][v] = float('inf')
                adj_mat_sp[u][v] = float('inf')
    
    # Populate adjacency matrices
    for i in range(no_of_edges):
        u = edges[i][0]
        v = edges[i][1]
        sigma_2 = (edge_ttc[i] * edge_ttc[i]) / 12
        adj_mat_ttc[u][v] = (edge_ttc[i]/2) - sigma_2
        adj_mat_sp[u][v] = edge_scp[i]
        
        # Count parents for AND nodes
        for j in range(no_of_vertices):
            if vertices[j][0] == v and vertices[j][1] == 1:
                vertices[j][2] += 1
    
    source = int(input("Enter the source: "))
    destination = int(input("Enter the destination: "))
    K = int(input("Enter the number of paths to be computed: "))
    
    alpha = 0.5
    ksp = YenkspDijpqAnodeDijpqMinedgesUtfun()
    allkspwithwt = ksp.findkshortestpaths(K, no_of_vertices, vertices, no_of_edges, 
                                         edges, adj_mat_ttc, adj_mat_sp, 
                                         source, destination, alpha)
    
    kspwithwt = allkspwithwt.split("@")
    print("\nReturned k shortest paths")
    for pathinksp in range(K):
        print(f"\n{kspwithwt[pathinksp]}-{kspwithwt[pathinksp+K]}", end="")
    print("\n")

if __name__ == "__main__":
    main()