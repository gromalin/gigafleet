#!/usr/bin/python
#coding=utf-8

import time
import unittest

import planet
import ship


def worker(player):
    while(True):
        #print "worker"
        for planet in player.planets:
            planet.run()
        for ship in player.ships:
            ship.run()
        #print "worker 2"
        time.sleep(1)

class Player:

    def __init__(self, name):
        self.name = name
        self.money = 10000
        self.planets = []
        self.ships = []

    def __str__(self):
        return self.name

    def status(self):
        return "Money : {} | Nb Ships : {} | Nb Planets : {}".format(
            self.money, len(self.ships), len(self.planets))

    def add_planet(self, planet):
        self.planets.append(planet)

    def do_list(self, param):
        if(param == "planets"):
            print(self.list_planets())
        elif (param == "ships"):
            print(self.list_ships())

    def list_planets(self):
        return ", ".join([planet.__str__() for planet in self.planets])

    def list_ships(self):
        return "Liste des vaisseaux : "+", ".join([ship.__str__() for ship in self.ships])

    def detail_ship(self, ship_name):
        return ", ".join([ship.__str__() for ship in self.ships if ship.name == ship_name])

    def get_planet(self, name):
        return [planet for planet in self.planets if planet.name == name]

    def do_status(self,param):
        print(self.name)

    def do_in(self,param):
        result =  [ship for ship in self.ships if ship.name == param]
        if(result is not None):
            return result[0]

    def do_add(self,param):
        self.buy_ship(param.partition(" ")[0],param.partition(" ")[2])

    def buy_ship(self,planet_name, ship_class_name):
        planet = self.get_planet(planet_name)
        if(len(planet) != 1):
            print("Planete {} est inconnue !".format(planet_name))
            return None

        try:
            ship_class  = getattr(ship, ship_class_name)
        except AttributeError:
            print("Classe de vaisseau {} est inconnue !".format(ship_class_name))
            return None

        if(self.money < ship_class.price):
            print("Argent insuffisant, {} ne couvre pas {}".format(self.money, ship_class.price))
            return None

        planet = planet[0]
        self.money = self.money - ship_class.price
        ship_tmp = planet.build_ship(ship_class)
        self.ships.append(ship_tmp)
        print("Fabrication de {} sur {}".format(ship_tmp.name, planet.name))
        return ship_tmp


class TestPlayerMethods(unittest.TestCase):
    def test_status(self):
        player = Player("Thomas")
        self.assertEquals(player.status(),
                          "Money : 10000 | Nb Ships : 0 | Nb Planets : 0")

    def test_add_planet(self):
        player = Player("Thomas")
        planet1 = planet.Planet(100, 100)
        player.add_planet(planet1)
        planet2 = planet.Planet(200, 200)
        player.add_planet(planet2)
        self.assertEquals(len(player.planets), 2)
        self.assertEquals(1, len(player.get_planet("Planet_0")))
        self.assertEquals(1, len(player.get_planet("Planet_1")))
        self.assertEquals(0, len(player.get_planet("Planet_2")))

        # Achat OK
        ship = player.buy_ship("Planet_0", "FastShip")
        self.assertIsNotNone(ship)
        self.assertEquals(player.money, 9900)
        self.assertEquals(len(player.ships), 1)

        # Planete inexistante
        ship = player.buy_ship("Planet_2", "FastShip")
        self.assertIsNone(ship)
        self.assertEquals(player.money, 9900)

        # Type vaisseau inexistant
        ship = player.buy_ship("Planet_0", "NoShip")
        self.assertIsNone(ship)
        self.assertEquals(player.money, 9900)

        # Plus d'argent
        player.money = 0
        ship = player.buy_ship("Planet_0", "FastShip")
        self.assertIsNone(ship)
        self.assertEquals(player.money, 0)


if __name__ == '__main__':
    unittest.main()


