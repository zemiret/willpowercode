from collections import deque


def dbscan(points_set, e, min_points):
    queue = deque()
    noise = {}
    visited = {}
    clusters = []

    def get_neighbours(point):
        return filter(lambda p: p != point and abs(point[0] - p[0]) <= e and abs(point[1] - p[1]) <= e, points_set)

    def scan_cluster():
        cluster = []
        while len(queue) > 0:
            p = queue.popleft()
            cluster.append(p)
            for n in get_neighbours(p):
                if n not in visited:
                    visited[n] = True
                    queue.append(n)
        return cluster

    for point in points_set:
        if point in visited:
            continue
        neighbours = get_neighbours(point)
        if len(neighbours) >= min_points:
            visited[point] = True
            queue.append(point)
            c = scan_cluster()
            clusters.append(c)
        else:
            noise[point] = True

    for cluster in clusters:
        for point in cluster:
            noise[point] = False

    return clusters, [x[0] for x in filter(lambda y: y[1] is True, noise.items())]
