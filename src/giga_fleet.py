#!/usr/bin/python
# coding=utf-8

import argparse
import cmd
import signal
import sys
import threading
import unittest
import re

import planet
import player
import universe

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)


class GigaFleetCmd(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.focus = []
        self.cur_universe = universe.Universe.get_universe()

        self.cur_player = player.Player("Thomas", self.cur_universe)
        self.update_prompt()


    def update_prompt(self):
        self.prompt = "{}@{}/".format(self.cur_player, self.cur_universe)
        for it in self.focus:
            self.prompt = self.prompt + it.__str__() + "/"
        self.prompt = self.prompt + ">"

    def usage(self):
        print("usage: : in planet <planet_name> or in ship <ship_name>")

    def do_in(self, param):

        regex = re.compile('^(planet|ship).*')
        if not regex.match(param):
            return self.usage()

        params = param.partition(" ")

        # recursive
        if(len(self.focus) != 0):
            result = self.focus[-1].do_in(param)
            if(result is not None):
                self.focus.append(result)
        else:
            if(params[0] == "planet"):
                planet = self.cur_universe.get_planet(params[2])
                if(planet is not None):
                    self.focus.append(planet)
            elif(params[0] == "ship"):
                ship = self.cur_player.get_ship(params[2])
                if(ship is not None):
                    self.focus.append(ship)
        self.update_prompt()

    def do_exit(self, param):
        if (len(self.focus) != 0):
            self.focus.pop()
        self.update_prompt()

    def do_status(self, param):
        self.focus[-1].do_status(param)
        #print(self.cur_player.status())

    def do_go(self, param):
        self.focus[-1].do_go(param)
        #print(self.cur_player.status())

    def do_list(self, param):
        self.focus[-1].do_list(param)
        #print(self.cur_player.status())

    #FIXME no recursivity, hard linked to cur_player
    def do_add(self, param):
        self.cur_player.do_add(param)
        #print(self.cur_player.status())

    def do_ships(self, param):
        print(self.cur_player.detail_ship(param))

    def do_ship(self, param):
        if param == "list":
            print(self.cur_player.list_ships())

    def do_planets(self, param):
        if param == "list":
            print(self.cur_player.list_planets())

    def do_planet(self, param):
        param = param.split()
        if param[0] == "buy":
            ship = self.cur_player.buy_ship(param[1], param[2])
        else:
            print("Parametres inconnus : {}".format(",".join(param)))


class TestGigaFleetCmdMethods(unittest.TestCase):

    giga_cmd = None

    def setUp(self):
        self.giga_cmd = GigaFleetCmd()
    def tearDown(self):
        self.giga_cmd = None
        planet.Planet.id = 0

    def test_update_prompt(self):
        self.assertEqual("Thomas@VoieLactée/>", self.giga_cmd.prompt)

    def test_do_in_planet(self):
        self.assertEqual("Thomas@VoieLactée/>",self.giga_cmd.prompt)

        self.giga_cmd.do_add("Planet_0 FastShip")
        self.giga_cmd.do_in("ship FastShip_0")
        self.assertEqual("Thomas@VoieLactée/FastShip_0/>",self.giga_cmd.prompt)

        self.giga_cmd.do_in("sh_ip FastShip_0")


    def test_do_in_ship(self):
        self.assertEqual("Thomas@VoieLactée/>",self.giga_cmd.prompt)

        self.giga_cmd.do_in("planet Planet_0")
        self.assertEqual("Thomas@VoieLactée/Planet_0/>",self.giga_cmd.prompt)


    def test_do_exit(self):
        self.giga_cmd.do_exit("")
        self.assertEqual("Thomas@VoieLactée/>",self.giga_cmd.prompt)
        self.assertEqual([],self.giga_cmd.focus)

        self.giga_cmd.do_in("planet Planet_0")
        self.giga_cmd.do_exit("")
        self.assertEqual("Thomas@VoieLactée/>",self.giga_cmd.prompt)
        self.assertEqual([],self.giga_cmd.focus)

if __name__ == '__main__':

    signal.signal(signal.SIGINT, signal_handler)
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", help="tests unitaires")
    args = parser.parse_args()

    if args.unit:
        runner = unittest.TextTestRunner()
        itersuite = unittest.TestLoader().loadTestsFromTestCase(TestGigaFleetCmdMethods)
        runner.run(itersuite)
    else:

        cmd = GigaFleetCmd()
        t = threading.Thread(target=universe.worker, args=(cmd.cur_universe,))
        t.daemon = True
        t.start()

        cmd.cmdloop()
