from collections import defaultdict
import constants as cons
row = cons.width
col = cons.height
grid = [[(y,x) for y in range(row)] for x in range(col)]
class Graph: 
  
    def __init__(self):  
        self.graph = defaultdict(list) 
  
    def addEdge(self,u,v): 
        self.graph[u].append(v) 
    
    def shortest_distance(self, src, dest):
        pred, dist = {}, {}
        adj = self.graph
        if (self.bfs(adj, src, dest, pred, dist) == False): 
            return 
  
        path = [] 
        crawl = dest 
        path.append(crawl) 
        while (pred[crawl] != -1):
            path.append(pred[crawl]); 
            crawl = pred[crawl]; 
        path.reverse()
        return path

    def bfs(self, adj, src, dest, pred, dist):
        visited, queue = {}, []

        for i in range(row):
            for j in range(col):
                visited[(j, i)] = False
                dist[(j, i)] = 999; 
                pred[(j, i)] = -1; 

        visited[src] = True 
        dist[src] = 0
        queue.append(src)

        while len(queue) > 0: 
            u = queue.pop(0)
            for i in range(len(adj[u])): 
                if (visited[adj[u][i]] == False): 
                    visited[adj[u][i]] = True 
                    dist[adj[u][i]] = dist[u] + 1
                    pred[adj[u][i]] = u; 
                    queue.append(adj[u][i])
    
                    if (adj[u][i] == dest):
                        return True
  
        return False 


def create():
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

    return g









'''

    for i in range(row):
        for j in range(col):
            if(i==0):
                if(j==0): 
                    g.addEdge(grid[i][j],grid[i][j+1])
                    g.addEdge(grid[i][j],grid[i+1][j])
                    continue

                elif(j>0 and j<col-1):
                    g.addEdge(grid[i][j],grid[i][j-1])
                    g.addEdge(grid[i][j],grid[i][j+1])
                    g.addEdge(grid[i][j],grid[i+1][j])
                    continue

                else:
                    g.addEdge(grid[i][j],grid[i][j-1])
                    g.addEdge(grid[i][j],grid[i+1][j])
                    continue

            elif(i>0 and i<row-1):
                if(j==0):
                    g.addEdge(grid[i][j],grid[i][j+1])
                    g.addEdge(grid[i][j],grid[i-1][j])
                    g.addEdge(grid[i][j],grid[i+1][j])
                    continue
                
                elif(j>0 and j<col-1):
                    g.addEdge(grid[i][j],grid[i][j-1])
                    g.addEdge(grid[i][j],grid[i][j+1])
                    g.addEdge(grid[i][j],grid[i-1][j])
                    g.addEdge(grid[i][j],grid[i+1][j])
                    continue

                else:
                    g.addEdge(grid[i][j],grid[i][j-1])
                    g.addEdge(grid[i][j],grid[i-1][j])
                    g.addEdge(grid[i][j],grid[i+1][j])
                    continue

            else:
                if(j==0): 
                    g.addEdge(grid[i][j],grid[i][j+1])
                    g.addEdge(grid[i][j],grid[i-1][j])
                    continue
                
                elif(j>0 and j<col-1):
                    g.addEdge(grid[i][j],grid[i][j-1])
                    g.addEdge(grid[i][j],grid[i][j+1])
                    g.addEdge(grid[i][j],grid[i-1][j])
                    continue

                else:
                    g.addEdge(grid[i][j],grid[i][j-1])
                    g.addEdge(grid[i][j],grid[i-1][j])
                    continue
    return g'''