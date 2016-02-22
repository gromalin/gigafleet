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

    state_text = []

    STOPPED_SLOT = 0
    state_text.insert(STOPPED_SLOT, "ship stopped on a slot")

    STOPPED_WAITING = 1
    state_text.insert(STOPPED_WAITING, "ship waiting for a slot")

    RUNNING = 2
    state_text.insert(RUNNING, "ship running")


    def __init__(self, site):
        elem.Elem.__init__(self, site.x, site.y)
        self.name = "{}_{}".format(self.__class__.__name__, self.__class__.id)
        self.__class__.id = self.__class__.id + 1
        self.dst_site = site
        self.state = Ship.STOPPED_SLOT

    def do_go(self, dst_site_name):
        if(self.state == Ship.STOPPED_SLOT):
            self.state = Ship.RUNNING
            self.dst_site.post_msg(message.Message(self, message.Message.LEAVING))
        self.dst_site  =  universe.Universe.get_universe().get_planet(dst_site_name)

    def __str__(self):
        return self.name

    def status(self):
        return "{} (speed : {}, price : {}, dest site: {}, state : {})".format(
            super(Ship, self).status(), self.speed, self.price, self.dst_site, Ship.state_text[self.state])

    def do_status(self, param):
        print(self.status())

    def run(self):

        if (self.state == Ship.RUNNING):
            assert(self.dst_site is not None)
            (go_x, go_y) = self.dst_site.get_pos()
            distance = elem.Elem.distance(self, self.dst_site)
            if distance > 1:
                angle = math.atan((go_y - self.y) / (go_x - self.x))
                #print("angle : {}".format(angle * 360 / (2*3.14)))
                #print("cos {}, sin {}".format(math.cos(angle), math.sin(angle)))

                # right part of the quadrant
                if(go_x -self.x > 0):
                    self.x = self.x + math.cos(angle) * (self.speed if distance > self.speed else distance)
                    self.y = self.y + math.sin(angle) * (self.speed if distance > self.speed else distance)

                # left part of the quadrant
                else:
                    self.x = self.x - math.cos(angle) * (self.speed if distance > self.speed else distance)
                    self.y = self.y - math.sin(angle) * (self.speed if distance > self.speed else distance)


            else:
                self.dst_site.post_msg(message.Message(self, message.Message.LANDING_REQUEST))
                self.state = Ship.STOPPED_WAITING

        elif(self.state == Ship.STOPPED_WAITING):
            msg = self.get_msg()
            if(msg is not None and msg.type == message.Message.LANDING_ACCEPTED and msg.sender == self.dst_site ):
                self.state = Ship.STOPPED_SLOT


class SlowShip(Ship):
    speed = 1
    price = 10
    id = 0

    def __init__(self, site):
        Ship.__init__(self, site)


class FastShip(Ship):
    speed = 5
    price = 100
    id = 0

    def __init__(self, site):
        Ship.__init__(self, site)



class TestShipMethods(unittest.TestCase):

    ship = None

    def setUp(self):

        self.ship0 = Ship(universe.Universe.get_universe().get_planet("Planet_0") )
        self.ship1 = Ship(universe.Universe.get_universe().get_planet("Planet_0"))
        self.slow_ship0 = SlowShip(universe.Universe.get_universe().get_planet("Planet_0"))
        self.fast_ship0 = FastShip(universe.Universe.get_universe().get_planet("Planet_0"))
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
        self.assertEquals(Ship.STOPPED_SLOT, self.ship0.state)

        # check the ship number increase
        self.assertEquals("Ship_1", self.ship1.name)

        self.assertEquals("SlowShip_0", self.slow_ship0.name)
        self.assertEquals("FastShip_0", self.fast_ship0.name)

    def test___str__(self):
        self.assertEqual("Ship_0", self.ship0.__str__())

    def test_status(self):
        self.assertEqual("Ship_0 (100,100) (speed : 1, price : 0, dest site: Planet_0, state : ship stopped on a slot)", self.ship0.status())

    def test_do_go(self):
        self.ship0.do_go("Planet_1")
        self.assertEquals(self.ship0.x, 100)
        self.assertEquals(self.ship0.y, 100)

        self.ship0.run()
        self.assertAlmostEquals(100.71, self.ship0.x, 2)
        self.assertAlmostEquals(100.71, self.ship0.y, 2)

        self.fast_ship0.do_go("Planet_1")
        self.fast_ship0.run()
        self.assertAlmostEquals(self.fast_ship0.x, 103.54, 2)
        self.assertAlmostEquals(self.fast_ship0.y, 103.54, 2)

        self.fast_ship0.do_go("Planet_0")
        self.fast_ship0.run()
        self.assertAlmostEquals(100.00, self.fast_ship0.x, 2)
        self.assertAlmostEquals(100.00, self.fast_ship0.y, 2)

        self.fast_ship0.do_go("Planet_2")
        self.fast_ship0.run()
        self.assertAlmostEquals(103.54, self.fast_ship0.x, 2)
        self.assertAlmostEquals(96.46, self.fast_ship0.y, 2)

        self.fast_ship0.do_go("Planet_0")
        self.fast_ship0.run()
        self.assertAlmostEquals(100.00, self.fast_ship0.x, 2)
        self.assertAlmostEquals(100.00, self.fast_ship0.y, 2)

        # Test message planet lors de l'arrivée
        self.fast_ship0.do_go("Planet_1")
        (self.fast_ship0.x, self.fast_ship0.y) = (200,200)
        self.fast_ship0.run()
        self.assertEquals(Ship.STOPPED_WAITING, self.fast_ship0.state)
        msg = universe.Universe.get_universe().get_planet("Planet_1").get_msg()
        self.assertEquals("Message sent by FastShip_0 : landing request",
                          msg.__str__())

        # On remet le message et on runne
        universe.Universe.get_universe().get_planet("Planet_1").post_msg(msg)
        universe.Universe.get_universe().get_planet("Planet_1").run()

        msg = self.fast_ship0.get_msg()

        self.assertEquals("Message sent by Planet_1 : landing accepted",
                          msg.__str__())
        # On remet le message et on runne
        self.fast_ship0.post_msg(msg)
        self.fast_ship0.run()
        self.assertEquals(Ship.STOPPED_SLOT, self.fast_ship0.state)


        self.fast_ship0.do_go("Planet_0")
        self.fast_ship0.run()
        msg = universe.Universe.get_universe().get_planet("Planet_1").get_msg()

        self.assertEquals("Message sent by FastShip_0 : leaving",
                          msg.__str__())


if __name__ == '__main__':
    unittest.main()
