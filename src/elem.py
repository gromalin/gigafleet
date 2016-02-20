#!/usr/bin/python
#coding=utf-8

import queue
import unittest


class Elem:


  id = 0
  def __init__(self,x,y):
    self.name = "{}_{}".format(self.__class__.__name__,self.__class__.id)
    self.x = x 
    self.y = y
    self.queue = queue.Queue()
  def get_name(self):
    return self.name

  def get_pos(self):
    return (self.x, self.y)

  def post_msg(self, msg):
    self.queue.put(msg)

  def __str__(self):
    return "{} ({},{})".format(self.name, self.x, self.y)

  def get_msg(self):
    try:
      return self.queue.get(False)
    except queue.Empty:
#      print "Queue vide"
      return None

class TestElemMethods(unittest.TestCase):
  def test_elem(self):
    elem = Elem(100,100)
    self.assertEquals(elem.__str__(), "Elem_0 (100,100)")

if __name__ == '__main__':
    unittest.main()
