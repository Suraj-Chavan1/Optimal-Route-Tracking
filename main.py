import math
import matplotlib.pyplot as plt

class AStar:
    def _init_(self, coordinates, adj, N, start, end, k, avgspeed):
        self.coordinates = coordinates
        self.adj = adj
        self.N = N
        self.start = start
        self.end = end
        self.speed = avgspeed
        self.parent = [-1] * N

    def dist(self):
        pq = []
        gscore = [math.inf] * self.N
        pq.append((self.getHeuristics(self.start, self.end), self.start))
        gscore[self.start] = 0

        while pq:
            f = pq.pop(0)
            currgscore = gscore[f[1]]

            for neighbour in self.adj[f[1]]:
                tempgscore = neighbour[1] + currgscore
                if tempgscore < gscore[neighbour[0]]:
                    gscore[neighbour[0]] = tempgscore
                    self.parent[neighbour[0]] = f[1]
                    fscore = gscore[neighbour[0]] + self.getHeuristics(neighbour[0], self.end)
                    pq.append((fscore, neighbour[0]))
            pq.sort()

    def getHeuristics(self, currnode, endnode):
        x1, y1 = self.coordinates[currnode]
        x2, y2 = self.coordinates[endnode]
        return math.ceil(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / self.speed)

    def getShortestPath(self):
        self.dist()
        path = []
        node = self.end
        while node != self.start:
            path.append(node)
            node = self.parent[node]
        path.append(self.start)
        path.reverse()
        return path

    def plotGraph(self, shortest_path):
        plt.figure(figsize=(8, 8))
        for i, (x, y) in enumerate(self.coordinates):
            plt.scatter(x, y, color='blue', s=100)
            plt.text(x, y, f'{i}', fontsize=12, ha='center', va='center')

        for node, neighbors in enumerate(self.adj):
            for neighbor, _ in neighbors:
                plt.plot([self.coordinates[node][0], self.coordinates[neighbor][0]],
                         [self.coordinates[node][1], self.coordinates[neighbor][1]], color='black')

        for i in range(len(shortest_path) - 1):
            node1 = shortest_path[i]
            node2 = shortest_path[i + 1]
            plt.plot([self.coordinates[node1][0], self.coordinates[node2][0]],
                     [self.coordinates[node1][1], self.coordinates[node2][1]], color='red', linewidth=2)

        plt.scatter(self.coordinates[self.start][0], self.coordinates[self.start][1], color='green', s=150, marker='o')
        plt.scatter(self.coordinates[self.end][0], self.coordinates[self.end][1], color='orange', s=150, marker='o')
        plt.title('Graph with Shortest Path')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.grid(True)
        plt.show()

# Example usage
coordinates = [(0, 0), (100, 100), (200, 200), (300, 50), (150, 250), (50, 300), (250, 150)]
adj = [[(1, 1), (5, 2)], [(2, 2), (3, 3)], [(4, 2), (6, 2)], [(4, 1)], [], [(6, 1)], [(3, 1)]]
N = 7
start = 0
end = 6
k = 1
avgspeed = 1

astar = AStar(coordinates, adj, N, start, end, k, avgspeed)
shortest_path = astar.getShortestPath()
print("Shortest path:", shortest_path)
astar.plotGraph(shortest_path)