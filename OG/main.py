import math
import numpy as np 
import matplotlib.pyplot as plt

class ListNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

    
class LinkedList:
    def __init__(self, array):
        self.start = None
        if array:
            _array = array[:]
            _array.reverse()
            while len(_array) > 0:
                x = _array.pop()
                node = ListNode(x)
                self.add(node)
    
    def add(self, node):
        if self.start:
            last = self.start.prev
            last.next = node
            node.prev = last
            node.next = self.start
            self.start.prev = node
        else:
            self.start = node
            self.start.next = node
            self.start.prev = node

    def remove(self, node):
        _node = None
        while _node != self.start:
            if _node is None:
                _node = self.start
            if _node == node:
                n = _node.next
                p = _node.prev
                n.prev = p
                p.next = n
                if node == self.start:
                    self.start = n
                break
            _node = _node.next

    def length(self):
        result = 0
        node = None
        while node != self.start:
            if node is None:
                node = self.start
            result += 1
            node = node.next
        return result

    def to_array(self):
        node = None
        arr = []
        while node != self.start:
            if node is None:
                node = self.start
            arr.append(node.value)
            node = node.next
        return arr


class Vec2:
    def __init__(self, x, y):
        if x is None:
            self.x = 0
        else:
            self.x = x
        if y is None:
            self.y = 0
        else:
            self.y = y

    def __str__(self):
        return "( " + str(self.x) + "; " + str(self.y) + " )" 
    
    def add(self, vec2):
        return Vec2(self.x + vec2.x, self.y + vec2.y)

    def sub(self, vec2):
        return Vec2(self.x - vec2.x, self.y - vec2.y)

    def mult(self, vec2):
        return Vec2(self.x * vec2.x, self.y * vec2.y)

    def div(self, vec2):
        return Vec2(self.x / vec2.x, self.y / vec2.y)

    def distance(self, vec2):
        temp = self.sub(vec2)
        return math.sqrt(temp.x * temp.x + temp.y * temp.y)

    def dot(self, vec2):
        return self.x * vec2.x + self.y * vec2.y

    def dup(self):
        return Vec2(self.x, self.y)


def calculate_angle(p1, p2, p3):
    return math.acos(p1.sub(p2).dot(p3.sub(p2)) / (p1.distance(p2) * p3.distance(p2)))

def is_right_turn(p1, p2, p3):
    delta = p1.x * p2.y - p1.x * p3.y - p2.x * p1.y + p3.x * p1.y + p2.x * p3.y - p3.x * p2.y
    return delta > 0

def is_left_turn(p1, p2, p3):
    delta = p1.x * p2.y - p1.x * p3.y - p2.x * p1.y + p3.x * p1.y + p2.x * p3.y - p3.x * p2.y
    return delta < 0

def find_inner_point(points):
    x = []
    y = []
    for point in points:
        x.append(point.x)
        y.append(point.y)
    center_x = (max(x) + min(x)) / 2
    center_y = (max(y) + min(y)) / 2
    return Vec2(center_x, center_y)

def prepare_points(points, center):
    helper = center.dup().add(Vec2(1, 0))
    result = []
    angles = []
    temp = {}

    for point in points:
        current_angle = calculate_angle(point, center, helper)
        if point.y < center.y:
            current_angle = 2 * math.pi - current_angle
        angles.append(current_angle)
        temp[current_angle] = point

    angles.sort()
    for angle in angles:
        result.append(temp[angle])

    return result

def build_convex_hull(points):
    pts = LinkedList(points)

    min_y = points[0].y
    min_point = points[0]
    for point in points:
        if point.y < min_y:
            min_y = point.y
            min_point = point
        elif point.y == min_y:
            if point.x < min_point.x:
                min_point = point

    start = None
    node = None
    while node != pts.start:
        if node is None:
            node = pts.start
        if node.value == min_point:
            start = node
            break
        node = node.next

    f = False
    v = start
    w = v.prev
    while v.next != start or not f:
        if v.next == w:
            f = True
        p1 = v.value
        p2 = v.next.value
        p3 = v.next.next.value
        if is_right_turn(p1, p2, p3):
            v = v.next
        else:
            pts.remove(v.next)
            v = v.prev
    pts.add(ListNode(pts.start.value))
    return pts.to_array()

def main():
    lines = open('input.txt', 'r')
    points = LinkedList([])
    for line in lines:
        values = line.split(' ')
        x = float(values[0])
        y = float(values[1])
        points.add(ListNode(Vec2(x, y)))

    q_point = find_inner_point(points.to_array())
    ordered = prepare_points(points.to_array(), q_point)

    convex_hull = build_convex_hull(ordered)
    print('\n\n\n')
    for point in convex_hull:
        print(point)

    x_points = []
    y_points = []
    x_convex_hull = []
    y_convex_hull = []
    for point in points.to_array():
        x_points.append(point.x)
        y_points.append(point.y)
    for point in convex_hull:
        x_convex_hull.append(point.x)
        y_convex_hull.append(point.y)

    x_points = np.array(x_points)
    y_points = np.array(y_points)
    x_convex_hull = np.array(x_convex_hull)
    y_convex_hull = np.array(y_convex_hull)

    plt.plot(x_points, y_points, 'o')
    plt.plot(x_convex_hull, y_convex_hull)
    plt.show()


if __name__ == '__main__':
    main()