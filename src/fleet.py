#!/usr/bin/python
# coding=utf-8

import interactive
import universe
import player

import unittest


class Fleet(interactive.Interactive):

    def __init__(self, player, name):
        interactive.Interactive.__init__(self)
        self.name = name
        self.ships = []
        self.player = player


    def usage(self):
        return("add <planet_name> <number of ships> <ships type>")

    def do_status(self, param):
        print("name : {}, ships : {}".format(self.name, [it.__str__() for it in self.ships]))

    def do_trace(self,param):
        [it.do_trace(param) for it in self.ships]

    def do_go(self, param):
        for ship_it in self.ships:
            ship_it.do_go(param)

    # return the number of ship built
    def do_add(self, param):
        import ship

        params = param.split(" ")
        if len(params) != 3:
            print(self.usage())
            return

        (planet_name, ship_nb, ship_type) = params
        cur_universe = universe.Universe.get_universe()
        planet = cur_universe.get_planet(planet_name)
        if planet == None:
            print("Planet {} is unknown".format(planet_name))
            return 0
        if (not ship_nb.isdigit()) or int(ship_nb) < 1:
            print("{} is not a correct number".format(ship_nb))
            return 0

        try:
            ship_class  = getattr(ship, ship_type)
        except AttributeError:
            print("Ship class {} is unknown".format(ship_type))
            return 0
        it = 0
        for it in range(int(ship_nb)):
            ship_tmp = self.player.buy_ship(planet.__str__(), ship_type)
            if(ship_tmp != None):
                self.ships.append(ship_tmp)
            else:
                return it+1
        return it+1

import ship

class TestPlayerMethods(unittest.TestCase):

    def setUp(self):
        self.universe = universe.Universe.get_universe()
        self.player = player.Player("Thomas", self.universe)

        self.fleet = Fleet(self.player,"The Fleet")
        self.planet_0= self.universe.get_planet("Planet_0")

    def tearDown(self):
        self.planet_0.slots = []
        ship.Ship.id = 0
        ship.FastShip.id = 0

    def test_do__init__(self):
        self.assertEqual("The Fleet", self.fleet.name)

    def test_do_add(self):
        ship_nb = self.fleet.do_add("Planet_500 3 FastShip")
        self.assertEqual(0, ship_nb)

        ship_nb = self.fleet.do_add("Planet_0 Test FastShip")
        self.assertEqual(0, ship_nb)


        ship_nb = self.fleet.do_add("Planet_0 0 FastShip")
        self.assertEqual(0, ship_nb)

        ship_nb = self.fleet.do_add("Planet_0 Test UnknownShip")
        self.assertEqual(0, ship_nb)

        ship_nb = self.fleet.do_add("Planet_0 1 FastShip")
        self.assertEqual(1, ship_nb)

        ship_nb = self.fleet.do_add("Planet_0 1000 FastShip")
        self.assertEqual(100, ship_nb)
        self.assertEqual(100, len(self.fleet.ships))
        self.assertEqual(100,len(self.planet_0.slots))


    def test_do_add_10_ships(self):

        ship_nb = self.fleet.do_add("Planet_0 10 FastShip")
        self.assertEqual(10, ship_nb)
        self.assertEqual(10, len(self.planet_0.slots))