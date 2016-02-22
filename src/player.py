#!/usr/bin/python
#coding=utf-8

import time
import unittest

import planet
import universe
import ship
import interactive


class Player (interactive.Interactive):

    def __init__(self, name, universe):
        self.name = name
        self.money = 10000
        self.ships = []
        self.universe = universe

    def __str__(self):
        return self.name

    def status(self):
        return "Money : {} | Nb Ships : {}".format(
            self.money, len(self.ships))


    def do_list(self, param):
        print(self.list_ships())

    def list_ships(self):
        return "Liste des vaisseaux : "+", ".join([ship.__str__() for ship in self.ships])

    def detail_ship(self, ship_name):
        return ", ".join([ship.__str__() for ship in self.ships if ship.name == ship_name])

    def get_ship(self, ship_name):
        ships = [ship for ship in self.ships if ship.name == ship_name]
        if(len(ships) == 1):
            return ships[0]
        else:
            return None


    def do_in(self,param):
        result =  [ship for ship in self.ships if ship.name == param]
        if(len(result) == 1):
            return result[0]
        else:
            print("Ship {} not found".format(param))

    def do_add(self,param):
        self.buy_ship(param.partition(" ")[0],param.partition(" ")[2])

    def buy_ship(self,planet_name, ship_class_name):
        planet = self.universe.get_planet(planet_name)
        if(planet == None):
            return None

        try:
            ship_class  = getattr(ship, ship_class_name)
        except AttributeError:
            print("Classe de vaisseau {} est inconnue !".format(ship_class_name))
            return None

        if(self.money < ship_class.price):
            print("Argent insuffisant, {} ne couvre pas {}".format(self.money, ship_class.price))
            return None

        self.money = self.money - ship_class.price
        ship_tmp = planet.build_ship(ship_class)
        self.ships.append(ship_tmp)
        universe.Universe.get_universe().ships.append(ship_tmp)
        print("Fabrication de {} sur {}".format(ship_tmp.name, planet.name))
        return ship_tmp


class TestPlayerMethods(unittest.TestCase):

    def setUp(self):
        cur_universe = universe.Universe("Voie lactée")

        self.player = Player("Thomas", cur_universe)

    def test_status(self):
        self.assertEquals(self.player.status(),
                          "Money : 10000 | Nb Ships : 0")

    def test_buy_ship(self):

        # Achat OK
        ship = self.player.buy_ship("Planet_0", "FastShip")
        self.assertIsNotNone(ship)
        self.assertEquals(self.player.money, 9900)
        self.assertEquals(len(self.player.ships), 1)

        # Planete inexistante
        ship = self.player.buy_ship("Planet_2", "FastShip")
        self.assertIsNone(ship)
        self.assertEquals(self.player.money, 9900)

        # Type vaisseau inexistant
        ship = self.player.buy_ship("Planet_0", "NoShip")
        self.assertIsNone(ship)
        self.assertEquals(self.player.money, 9900)

        # Plus d'argent
        self.player.money = 0
        ship = self.player.buy_ship("Planet_0", "FastShip")
        self.assertIsNone(ship)
        self.assertEquals(self.player.money, 0)


if __name__ == '__main__':
    unittest.main()


