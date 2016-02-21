#!/usr/bin/python
# coding=utf-8

import unittest

import giga_site
import ship


class Planet(giga_site.GigaSite):
    id = 0

    def __init__(self, x, y):
        # giga_site.GigaSite.__init__(self, x, y)
        super(self.__class__, self).__init__(x, y)
        self.under_construction = []
        self.slots = []

    def __str__(self):
        return "{} ({},{})".format(
            self.name, self.x, self.y)

    def build_ship(self, ship_class):
        ship = ship_class(self.x, self.y)
        self.slots.append(ship)
        return ship


class TestPlanetMethods(unittest.TestCase):
    def setUp(self):
        self.planet = Planet(100, 100)

    def tearDown(self):
        ship.FastShip.id = 0
        Planet.id = 0

    def test_planet(self):
        self.assertEquals('Planet_0 (100,100)', self.planet.__str__())
        self.assertEquals(self.planet.x, 100)
        self.assertEquals(self.planet.y, 100)
        self.assertEquals(len(self.planet.slots), 0)
        self.assertEquals(len(self.planet.under_construction), 0)
        self.assertEquals(self.planet.__str__(),
                          "Planet_0 (100,100)")
        self.planet.build_ship(ship.FastShip)
        self.assertEquals(len(self.planet.slots), 1)
        self.assertEquals(self.planet.slots[0].name, "FastShip_0")


if __name__ == '__main__':
    unittest.main()
