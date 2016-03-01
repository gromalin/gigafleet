#!/usr/bin/python
# coding=utf-8

import queue
import unittest
import math
from datetime import datetime, date, time


import interactive

class Elem(interactive.Interactive):
    id = 0

    def distance (e1, e2):
        return math.sqrt((e2.x-e1.x)**2 + (e2.y - e1.y)**2)

    def __init__(self, x, y):
        interactive.Interactive.__init__(self)
        self.name = "{}_{}".format(self.__class__.__name__, self.__class__.id)
        self.x = x
        self.y = y
        self.queue = queue.Queue()
        self.log = []

    def __str__(self):
        return self.name

    def add_log(self, line):
        self.log.append("{} {} : {}".format(datetime.now(), self.name, line))

    def do_log(self,param):
        for line in self.log:
            print("{}".format(line))

    def get_pos(self):
        return (self.x, self.y)

    def post_msg(self, msg):
        #print(msg)
        msg.sender.add_log("{} posted".format(msg.__str__()))
        self.queue.put(msg)

    def status(self):
        return "{} ({:.0f},{:.0f})".format(self.name, self.x, self.y)

    def get_msg(self):

        while True:
            try:
                msg = self.queue.get(False)
                self.add_log("{} accessed".format(msg.__str__()))
                yield msg
            except queue.Empty:
                #      print "Queue vide"
                return

import message
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

    def test_multiple_messages(self):
        for it in range(5):
            self.elem1.post_msg(message.Message(self.elem0,message.Message.LEAVING))
        iterator = self.elem1.get_msg()
        nb_msg = 0
        for msg in iterator:
            nb_msg = nb_msg + 1
        self.assertEqual(5, nb_msg)



if __name__ == '__main__':
    unittest.main()
