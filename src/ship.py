#!/usr/bin/python
# coding=utf-8

import math
import unittest

import elem
import message
import planet
import interactive
import universe

class Ship(elem.Elem, interactive.Interactive):
    id = 0
    speed = 1
    price = 0

    def __init__(self, x, y):
        elem.Elem.__init__(self, x, y)
        self.name = "{}_{}".format(self.__class__.__name__, self.__class__.id)
        self.__class__.id = self.__class__.id + 1
        self.dst_site = None

    def do_go(self, dst_site_name):
        self.dst_site  =  universe.Universe.get_universe().get_planet(dst_site_name)

    def __str__(self):
        return self.name

    def status(self):
        return "{} (speed : {}, price : {}, dest site: {})".format(
            super(Ship, self).status(), self.speed, self.price, self.dst_site)

    def do_status(self, param):
        print(self.status())

    def run(self):

        if (self.dst_site is not None):
            (go_x, go_y) = self.dst_site.get_pos()
            distance = elem.Elem.distance(self, self.dst_site)
            if (distance > 1):
                angle = math.atan((go_y - self.y) / (go_x - self.x))
                #print("angle : {}".format(angle * 360 / (2*3.14)))
                #print("cos {}, sin {}".format(math.cos(angle), math.sin(angle)))

                if(go_x -self.x > 0):
                    self.x = self.x + math.cos(angle) * (self.speed if distance > self.speed else distance)
                else:
                    self.x = self.x - math.cos(angle) * (self.speed if distance > self.speed else distance)
                if(go_y -self.y > 0):
                    self.y = self.y + math.sin(angle) * (self.speed if distance > self.speed else distance)
                else:
                    self.y = self.y - math.sin(angle) * (self.speed if distance > self.speed else distance)


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
        #self.planet0 = planet.Planet(200, 200)
        #self.planet1 = planet.Planet(103.54, 103.54)

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

    def test_do_go(self):
        self.ship0.do_go("Planet_1")
        self.assertEquals(self.ship0.x, 100)
        self.assertEquals(self.ship0.y, 100)

        self.ship0.run()
        self.assertAlmostEquals(self.ship0.x, 100.71, 2)
        self.assertAlmostEquals(self.ship0.y, 100.71, 2)

        self.fast_ship0.do_go("Planet_1")
        self.fast_ship0.run()
        self.assertAlmostEquals(self.fast_ship0.x, 103.54, 2)
        self.assertAlmostEquals(self.fast_ship0.y, 103.54, 2)

        self.fast_ship0.do_go("Planet_0")
        self.fast_ship0.run()
        self.assertAlmostEquals(100.00, self.fast_ship0.x, 2)
        self.assertAlmostEquals(100.00, self.fast_ship0.y, 2)

        # Test message planet quand arrivé
        self.fast_ship0.do_go("Planet_1")
        (self.fast_ship0.x, self.fast_ship0.y) = (200,200)
        self.fast_ship0.run()
        self.assertEquals("Message envoyé par FastShip_0 : demande d'atterissage",
                          universe.Universe.get_universe().get_planet("Planet_1").get_msg().__str__())


if __name__ == '__main__':
    unittest.main()
