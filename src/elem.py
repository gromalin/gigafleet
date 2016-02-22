#!/usr/bin/python
# coding=utf-8

import queue
import unittest
import math

class Elem:
    id = 0

    def distance (e1, e2):
        return math.sqrt((e2.x-e1.x)**2 + (e2.y - e1.y)**2)

    def __init__(self, x, y):
        self.name = "{}_{}".format(self.__class__.__name__, self.__class__.id)
        self.x = x
        self.y = y
        self.queue = queue.Queue()

    def __str__(self):
        return self.name

    def get_pos(self):
        return (self.x, self.y)

    def post_msg(self, msg):
        print(msg)
        self.queue.put(msg)

    def status(self):
        return "{} ({:.0f},{:.0f})".format(self.name, self.x, self.y)

    def get_msg(self):
        try:
            return self.queue.get(False)
        except queue.Empty:
            #      print "Queue vide"
            return None


class TestElemMethods(unittest.TestCase):
    elem0 = None
    elem1 = None

    def setUp(self):
        self.elem0 = Elem(100.01, 100.01)
        self.elem1 = Elem(200.01, 200.01)

    def tearDown(self):
        Elem.id = 0

    def test_elem(self):
        self.assertEquals("Elem_0", self.elem0.__str__())
        self.assertEquals("Elem_0 (100,100)", self.elem0.status())

    def test_distance(self):
        self.assertAlmostEqual(141, Elem.distance(self.elem0, self.elem1),0)

if __name__ == '__main__':
    unittest.main()
