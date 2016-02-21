#!/usr/bin/python
# coding=utf-8

import math
import unittest

import elem
import message
import planet

class Ship(elem.Elem):
    id = 0
    speed = 1
    price = 0

    def __init__(self, x, y):
        elem.Elem.__init__(self, x, y)
        self.name = "{}_{}".format(self.__class__.__name__, self.__class__.id)
        self.__class__.id = self.__class__.id + 1
        self.dst_site = None

    def go(self, dst_site):
        self.dst_site = dst_site

    def __str__(self):
        return self.name

    def status(self):
        return "{} (speed : {}, price : {}, dest site: {})".format(
            super(Ship, self).status(), self.speed, self.price, self.dst_site)

    def run(self):

        if (self.dst_site is not None):
            (go_x, go_y) = self.dst_site.get_pos()
            if (abs(go_x - self.x) > 0.1
                or abs(go_y - self.y) > 0.1):
                angle = math.atan((go_y - self.y) / (go_x - self.x))
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

    def __init__(self, x, y):
        Ship.__init__(self, x, y)



class TestShipMethods(unittest.TestCase):

    ship = None

    def setUp(self):
        self.ship0 = Ship(100, 100)
        self.ship1 = Ship(100,00)
        self.slow_ship0 = SlowShip(100, 100)
        self.fast_ship0 = FastShip(100, 100)
        self.planet0 = planet.Planet(200, 200)
        self.planet1 = planet.Planet(103.54, 103.54)

    def tearDown(self):
        Ship.id = 0
        FastShip.id = 0
        SlowShip.id = 0
        planet.Planet.id = 0

    def test_init(self):
        self.assertEquals("Ship_0", self.ship0.name)
        self.assertEquals(100, self.ship0.x)
        self.assertEquals(100, self.ship0.y)

        # check the ship number increase
        self.assertEquals("Ship_1", self.ship1.name)

        self.assertEquals("SlowShip_0", self.slow_ship0.name)
        self.assertEquals("FastShip_0", self.fast_ship0.name)

    def test___str__(self):
        self.assertEqual("Ship_0", self.ship0.__str__())

    def test_status(self):
        self.assertEqual("Ship_0 (100,100) (speed : 1, price : 0, dest site: None)", self.ship0.status())

    def test_go(self):
        self.ship0.go(self.planet0)
        self.assertEquals(self.ship0.x, 100)
        self.assertEquals(self.ship0.y, 100)

        self.ship0.run()
        self.assertAlmostEquals(self.ship0.x, 100.71, 2)
        self.assertAlmostEquals(self.ship0.y, 100.71, 2)

        self.fast_ship0.go(self.planet0)
        self.fast_ship0.run()
        self.assertAlmostEquals(self.fast_ship0.x, 103.54, 2)
        self.assertAlmostEquals(self.fast_ship0.y, 103.54, 2)

        # Test message planet quand arrivé
        self.fast_ship0.go(self.planet1)
        self.fast_ship0.run()
        self.assertEquals(self.planet1.get_msg().__str__(), "Message envoyé par FastShip_0 : demande d'atterissage")

if __name__ == '__main__':
    unittest.main()
