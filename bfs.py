from collections import defaultdict

grid = [[0 for y in range(10)] for x in range(10)]
z = 0
for x in range(10):
    for y in range(10):
        grid[x][y] = z
        z += 1

class Graph: 
  
    def __init__(self):  
        self.graph = defaultdict(list) 
  
    def addEdge(self,u,v): 
        self.graph[u].append(v) 
    
    def shortest_distance(self, src, dest):
        pred = [0 for i in range(100)]
        dist = [0 for i in range(100)]
        adj = self.graph

        if (self.bfs(adj, src, dest, pred, dist) == False): 
            print("Not connected")
            return 
  
        path = [] 
        crawl = dest 
        path.append(crawl) 
        while (pred[crawl] != -1):
            path.append(pred[crawl]); 
            crawl = pred[crawl]; 
        
        print("distance to destination:", dist[dest], "units") 
        for i in range(len(path)-1, -1, -1):
            print(path[i])

    def bfs(self, adj, src, dest, pred, dist):
        visited, queue = [], []

        for i in range(100):
            visited.append(False)
            dist[i] = 999; 
            pred[i] = -1; 

        visited[src] = True 
        dist[src] = 0
        queue.append(src)

        while len(queue) > 0: 
            u = queue.pop(0)
            len(self.graph[u])
            for i in range(len(adj[u])): 
                if (visited[adj[u][i]] == False): 
                    visited[adj[u][i]] = True 
                    dist[adj[u][i]] = dist[u] + 1
                    pred[adj[u][i]] = u; 
                    queue.append(adj[u][i])
    
                    if (adj[u][i] == dest):
                        return True
  
        return False 


g = Graph()

for x in range(1, 9):
    for y in range(1, 9):
        g.addEdge(grid[x][y], grid[x-1][y])
        g.addEdge(grid[x][y], grid[x+1][y])
        g.addEdge(grid[x][y], grid[x][y-1])
        g.addEdge(grid[x][y], grid[x][y+1])

for x in range(1, 9):
    g.addEdge(grid[x][0], grid[x-1][0])
    g.addEdge(grid[x][0], grid[x+1][0])
    g.addEdge(grid[x][0], grid[x][1])
    g.addEdge(grid[x][9], grid[x-1][9])
    g.addEdge(grid[x][9], grid[x+1][9])
    g.addEdge(grid[x][9], grid[x][8])

for y in range(1, 9):
    g.addEdge(grid[0][y], grid[0][y-1])
    g.addEdge(grid[0][y], grid[0][y+1])
    g.addEdge(grid[0][y], grid[1][y])
    g.addEdge(grid[9][y], grid[9][y-1])
    g.addEdge(grid[9][y], grid[9][y+1])
    g.addEdge(grid[9][y], grid[8][y])

g.addEdge(grid[0][0], grid[1][0])
g.addEdge(grid[0][0], grid[0][1])

g.addEdge(grid[9][9], grid[9][8])
g.addEdge(grid[9][9], grid[8][9])

g.addEdge(grid[0][9], grid[0][8])
g.addEdge(grid[0][9], grid[1][9])

g.addEdge(grid[9][0], grid[8][0])
g.addEdge(grid[9][0], grid[9][1])

#g.BFS(grid[1][1])
#print(grid)
#print(g.graph)
g.shortest_distance(0,99)