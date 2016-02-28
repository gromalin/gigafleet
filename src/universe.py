import time
import unittest
import planet


def worker(universe):
    while (True):
        # print "worker"
        for planet in universe.planets:
            planet.run()
        for ship in universe.ships:
            ship.run()
        # print "worker 2"
        time.sleep(1)


class Universe():

    instance = None
    def __init__(self, name):
        self.name = name
        self.planets = [planet.Planet(100,100), planet.Planet(200,200), planet.Planet(200,0)]
        self.ships = []

    @staticmethod
    def get_universe():
        if(Universe.instance == None):
            Universe.instance = Universe("VoieLactée")
        return Universe.instance

    def add_planet(self, planet):
        self.planets.append(planet)

    def do_list(self, param):
        if (param == "planets"):
            print(self.list_planets())
        elif (param == "ships"):
            print(self.list_ships())

    def list_planets(self):
        return ", ".join([planet.__str__() for planet in self.planets])

    def get_planet(self, name):
        result = [planet for planet in self.planets if planet.name == name]
        if(result == []):
            print("planet {} unknown".format(name))
            return None
        return result[0]

    def get_ship(self, name):
        result = [ship for ship in self.ships if ship.name == name]
        if(result == []):
            print("ship {} unknown".format(name))
            return None
        return result[0]

    def __str__(self):
            return self.name


class TestUniverseMethods(unittest.TestCase):
    def setUp(self):
        self.universe = Universe("Voie lactée")

    def doCleanups(self):
        planet.Planet.id = 0

    def test___str__(self):
        self.assertEqual("Voie lactée", self.universe.__str__())

    def test___init__(self):
        self.assertEquals(len(self.universe.planets), 3)
        self.assertIsNotNone(self.universe.get_planet("Planet_0"))
        self.assertIsNotNone(self.universe.get_planet("Planet_1"))
        self.assertIsNone(self.universe.get_planet("Planet_10000"))

if __name__ == '__main__':
    unittest.main()
