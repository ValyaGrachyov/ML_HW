import pygame as pg
import numpy as np
import random as rnd
import colorsys

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other):
        return np.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class DBSCAN:
    def __init__(self, eps, min_samples):
        self.eps = eps
        self.min_samples = min_samples
        self.labels = None

    def fit(self, points):
        self.labels = [0] * len(points)
        cluster_id = 0

        for i, point in enumerate(points):
            if self.labels[i] != 0:
                continue
            neighbors = self.region_query(points, point)
            if len(neighbors) < self.min_samples:
                self.labels[i] = -1
            else:
                cluster_id += 1
                self.expand_cluster(points, point, neighbors, cluster_id)

    def region_query(self, points, point):
        neighbors = []
        for i, p in enumerate(points):
            if point.distance_to(p) < self.eps:
                neighbors.append(i)
        return neighbors

    def expand_cluster(self, points, point, neighbors, cluster_id):
        self.labels[points.index(point)] = cluster_id
        i = 0
        while i < len(neighbors):
            idx = neighbors[i]
            if self.labels[idx] == -1:
                self.labels[idx] = cluster_id
            elif self.labels[idx] == 0:
                self.labels[idx] = cluster_id
                new_neighbors = self.region_query(points, points[idx])
                if len(new_neighbors) >= self.min_samples:
                    neighbors += new_neighbors
            i += 1


def drawPoint(position):
    pg.draw.circle(screen, 'black', position, 5)
    pg.display.update()
    positions.append(Point(position[0], position[1]))

def generate_colors(n):
    colors = []
    for i in range(n):
        hue = i / n
        saturation = 0.7
        value = 0.9
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        colors.append((int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)))
    return colors


pg.init()

screen = pg.display.set_mode(size=(600, 600))
screen.fill(color="#FFFFFF")
pg.display.update()
status = True
minDist = 30
positions = [Point(0, 0)]
numOfRndPoints = 10

drawing = False

while status:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            status = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
                pos = event.pos
                drawPoint(pos)
                for x in range(rnd.randint(1, numOfRndPoints)):
                    drawPoint([pos[0] + rnd.randint(-10, 11), pos[1] + rnd.randint(-10, 11)])
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
        elif event.type == pg.MOUSEMOTION:
            if drawing:
                pos = event.pos
                if positions[-1].distance_to(Point(pos[0], pos[1])) > minDist:
                    drawPoint(pos)
                    for x in range(rnd.randint(1, numOfRndPoints)):
                        drawPoint([pos[0] + rnd.randint(-10, 11), pos[1] + rnd.randint(-10, 11)])
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                dbscan = DBSCAN(eps=20, min_samples=3)
                points = positions[1:]
                dbscan.fit(points)
                labels = dbscan.labels
                unique_labels = set(labels)
                colors = generate_colors(len(unique_labels))
                screen.fill('white')
                for i, point in enumerate(points):
                    if labels[i] != -1:
                        pg.draw.circle(screen, colors[labels[i] - 1], (point.x, point.y), 10)
                    else:
                        pg.draw.circle(screen, 'black', (point.x, point.y), 10)
                pg.display.flip()

pg.quit()
