#!/usr/bin/python
#coding=utf-8

import math
import unittest

import elem
import message


class Ship(elem.Elem):

  id = 0
  speed = 1
  price = 0

  def __init__(self, x, y):
    elem.Elem.__init__(self, x, y)
    self.name = "{}_{}".format(self.__class__.__name__,self.__class__.id)
    self.__class__.id = self.__class__.id + 1
    self.dst_site = None

  def go(self, dst_site):
    self.dst_site = dst_site

  def __str__(self):
    return "{} (speed : {}, price : {})".format(
      self.id,self.speed, self.price)

  def run(self):

    if(self.dst_site is not None):
      (go_x,go_y) = self.dst_site.get_pos()
      if(abs(go_x -self.x) > 0.1 
        or abs(go_y - self.y) > 0.1): 
        angle = math.atan((go_y -self.y)/(go_x - self.x))
        self.x = self.x + math.cos(angle) * self.speed
        self.y = self.y + math.sin(angle) * self.speed
      else:
        self.dst_site.post_msg(message.Message(self, message.Message.LANDING_REQUEST))
      

class SlowShip(Ship):

  speed = 1
  price = 10
  id = 0

  def __init__(self, x, y):
    Ship.__init__(self, x, y)

class FastShip(Ship):

  speed = 5
  price = 100
  id = 0

  def __init__(self,  x, y):
    Ship.__init__(self, x, y)

class TestShipMethods(unittest.TestCase):

  def test_ship(self):
    from src import planet
    ship = Ship(100, 100)
    self.assertEquals("Ship_0", ship.name)
    self.assertEquals(100, ship.x)
    self.assertEquals(100, ship.y)

    #check the ship number inscrease
    ship = Ship(100, 100)
    self.assertEquals("Ship_1", ship.name)


    ship = SlowShip(100,100)
    self.assertEquals("SlowShip_0", ship.name)



    fast_ship = FastShip(100, 100)
    self.assertEquals("FastShip_0", fast_ship.name)

    planet0 = planet.Planet(200, 200)

    ship.go(planet0)
    self.assertEquals(ship.x,100)
    self.assertEquals(ship.y,100)


    ship.run()
    self.assertAlmostEquals(ship.x,100.71,2)
    self.assertAlmostEquals(ship.y,100.71,2)

    fast_ship.go(planet0)
    fast_ship.run()
    self.assertAlmostEquals(fast_ship.x,103.54,2)
    self.assertAlmostEquals(fast_ship.y,103.54,2)

    # Test message planet quand arrivé
    planet1 = planet.Planet(103.54, 103.54)
    fast_ship.go(planet1)
    fast_ship.run()
    self.assertEquals(planet1.get_msg().__str__(), "Message envoyé par FastShip_0 : demande d'atterissage")

if __name__ == '__main__':
    unittest.main()
