#!/usr/bin/python
# coding=utf-8

import math
import unittest

import elem
import message
import planet
import interactive
import universe

class Ship(elem.Elem):
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

    UNREACH_DST = 3
    state_text.insert(UNREACH_DST, "ship has an unreachable destination")


    def __init__(self, site):
        elem.Elem.__init__(self, site.x, site.y)
        self.name = "{}_{}".format(self.__class__.__name__, self.__class__.id)
        self.__class__.id = self.__class__.id + 1
        self.dst_site = site
        self.state = Ship.STOPPED_SLOT
        self.dst_list = [site.__str__()]
        self.trace = False

    def do_go(self, param):
        self.dst_list = param.split(" ")

    def __str__(self):
        return self.name

    def status(self):
        return "{} (speed : {}, price : {}, dest site: {}, state : {})".format(
            super(Ship, self).status(), self.speed, self.price, self.dst_site, Ship.state_text[self.state])

    @property
    def dict_status(self):
        result = {}
        result["name"] = self.name
        result["speed"] =  str(self.speed)
        result["price"] = str(self.price)
        result["dst_site"] = self.dst_site.__str__()
        result["state"] = Ship.state_text[self.state]
        result["x"] = str(self.x)
        result["y"] = str(self.y)
        return result

        return {"speed" : super(Ship, self).status(), }

    def do_status(self, param):
        print(self.status())

    def run(self):

        if self.trace:
            self.do_status("")

        if(self.state == Ship.UNREACH_DST):
            return

        if(self.state == Ship.STOPPED_SLOT):


            if len(self.dst_list) > 1 and \
                            self.dst_site.__str__() == self.dst_list[0] : # multiple destination, go to the next one
                old_dst = self.dst_list.pop(0) # pop current destination
                self.dst_list.append(old_dst)

            if self.dst_site.__str__() != self.dst_list[0]: # if destination has changed
                self.add_log("destination is now {}".format(self.dst_site))
                self.dst_site.post_msg(message.Message(self, message.Message.LEAVING))
                self.state = Ship.RUNNING

        if (self.state == Ship.RUNNING):
            assert(self.dst_site is not None)

            # New orders
            if(self.dst_site.__str__() != self.dst_list[0]):
                self.dst_site = universe.Universe.get_universe().get_planet(self.dst_list[0])
                if(self.dst_site == None):
                    self.state == Ship.UNREACH_DST
                    self.log("unreachable destination : {}".format(self.dst_site))

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
            #msg = self.get_msg()
            for msg in self.get_msg():
                if(msg is not None and msg.type == message.Message.LANDING_ACCEPTED and msg.sender == self.dst_site ):
                    self.state = Ship.STOPPED_SLOT
                    return

            if self.dst_site.__str__() != self.dst_list[0]: # if destination has changed
                self.dst_site.post_msg(message.Message(self, message.Message.LEAVING))
                self.state = Ship.RUNNING
                return

            self.dst_site.post_msg(message.Message(self, message.Message.LANDING_REQUEST))

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
        self.planet_0 = universe.Universe.get_universe().get_planet("Planet_0")
        self.planet_1 = universe.Universe.get_universe().get_planet("Planet_1")

        #self.planet0 = planet.Planet(200, 200)
        #self.planet1 = planet.Planet(103.54, 103.54)

    def tearDown(self):
        Ship.id = 0
        FastShip.id = 0
        SlowShip.id = 0
        planet.Planet.id = 0
        self.planet_0.ships = []
        self.planet_1.ships = []

    def test_init(self):
        self.assertEquals("Ship_0", self.ship0.name)
        self.assertEquals(100, self.ship0.x)
        self.assertEquals(100, self.ship0.y)
        self.assertEquals(Ship.STOPPED_SLOT, self.ship0.state)

        self.assertEquals(["Planet_0"], self.ship0.dst_list)

        self.ship0.run()
        self.assertEquals(Ship.STOPPED_SLOT, self.ship0.state)


        # check the ship number increase
        self.assertEquals("Ship_1", self.ship1.name)

        self.assertEquals("SlowShip_0", self.slow_ship0.name)
        self.assertEquals("FastShip_0", self.fast_ship0.name)

    def test___str__(self):
        self.assertEqual("Ship_0", self.ship0.__str__())

    def test_status(self):
        self.assertEqual("Ship_0 (100,100) (speed : 1, price : 0, dest site: Planet_0, state : ship stopped on a slot)", self.ship0.status())

    def test_log(self):
        self.ship0.do_go("Planet_1")
        self.ship0.run()
        #self.assertEqual("Destination is now", self.ship0.log[0])
        self.assertTrue(self.ship0.log[0].find("Ship_0 : destination is now Planet_0") != -1)



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
        msg = next(universe.Universe.get_universe().get_planet("Planet_1").get_msg())
        self.assertEquals("message from FastShip_0 : landing request",
                          msg.__str__())

        # On remet le message et on runne
        universe.Universe.get_universe().get_planet("Planet_1").post_msg(msg)
        universe.Universe.get_universe().get_planet("Planet_1").run()

        msg = next(self.fast_ship0.get_msg())

        self.assertEquals("message from Planet_1 : landing accepted",
                          msg.__str__())
        # On remet le message et on runne
        self.fast_ship0.post_msg(msg)
        self.fast_ship0.run()
        self.assertEquals(Ship.STOPPED_SLOT, self.fast_ship0.state)


        self.fast_ship0.do_go("Planet_0")
        self.fast_ship0.run()
        msg = next(universe.Universe.get_universe().get_planet("Planet_1").get_msg())

        self.assertEquals("message from FastShip_0 : leaving",
                          msg.__str__())

    def test_dict_status(self):
        result = self.ship0.dict_status
        self.assertEqual("Ship_0", result["name"])
        self.assertEqual("1", result["speed"])
        self.assertEqual("0", result["price"])
        self.assertEqual("Planet_0", result["dst_site"])
        self.assertEqual("ship stopped on a slot", result["state"])
        self.assertEqual("100", result["x"])
        self.assertEqual("100", result["y"])



    def test_do_go_mutiple_dst(self):
        self.ship0.do_go("Planet_1 Planet_0")
        self.assertEquals(["Planet_1", "Planet_0"], self.ship0.dst_list)
        self.ship0.run()
        self.assertEqual(self.planet_1, self.ship0.dst_site)

        (self.ship0.x, self.ship0.y) = (self.planet_1.x, self.planet_1.y) # Ship is placed on Planet_1
        self.ship0.run()        # Ask landing
        self.planet_1.run()          # landing accepted
        self.ship0.run()        # Process landing acceptance message
        self.assertEqual(Ship.STOPPED_SLOT, self.ship0.state)

        self.ship0.run()
        self.assertEqual(Ship.RUNNING, self.ship0.state)
        self.assertEqual(self.planet_0, self.ship0.dst_site)

if __name__ == '__main__':
    unittest.main()
