#!/usr/bin/python
# coding=utf-8

import argparse
import cmd
import signal
import sys
import threading
import unittest
import re
from flask import Flask
app = Flask(__name__)


import planet
import player
import universe
import interactive

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)


class GigaFleetCmd(cmd.Cmd, interactive.Interactive):
    def __init__(self):
        cmd.Cmd.__init__(self)
        interactive.Interactive.__init__(self)
        self.focus = []
        self.cur_universe = universe.Universe.get_universe()

        self.cur_player = player.Player("Thomas", self.cur_universe)
        self.update_prompt()
        self.do_add("fleet Fleet_0")
        self.do_in("fleet Fleet_0")
        self.do_add("Planet_0 30 FastShip")
        self.do_go("Planet_1 Planet_0")
        self.do_exit("")


    def update_prompt(self):
        self.prompt = "{}@{}/".format(self.cur_player, self.cur_universe)
        for it in self.focus:
            self.prompt = self.prompt + it.__str__() + "/"
        self.prompt = self.prompt + ">"

    def usage(self):
        print("usage: : in planet <planet_name> or in ship <ship_name>")

    def do_in(self, param):

        regex = re.compile('^(planet|ship|fleet).*')
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
                ship = self.cur_universe.get_ship(params[2])
                if(ship is not None):
                    self.focus.append(ship)
            elif(params[0] == "fleet"):
                fleet = self.cur_player.get_fleet(params[2])
                if(fleet is not None):
                    self.focus.append(fleet)
        self.update_prompt()

    def do_exit(self, param):
        if (len(self.focus) != 0):
            self.focus.pop()
        self.update_prompt()

    def do_status(self, param):
        if len(self.focus) > 0 :
            self.focus[-1].do_status(param)
        else:
            super().do_status("")

    def do_go(self, param):
        if len(self.focus) > 0 :
            self.focus[-1].do_go(param)
        else:
            super().do_trace("")


    def do_list(self, param):
        if len(self.focus) > 0 :
            self.focus[-1].do_list(param)
        else:
            super().do_trace("")

    def do_trace(self, param):
        if len(self.focus) > 0 :
            self.focus[-1].do_trace(param)
        else:
            super().do_trace("")

    def do_log(self, param):
        if len(self.focus) > 0 :
            self.focus[-1].do_log(param)
        else:
            super().do_log("")

    #FIXME no recursivity, hard linked to cur_player
    def do_add(self, param):
        if len(self.focus) > 0 :
            self.focus[-1].do_add(param)
        else:
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

@app.route('/')
def hello_world():
    return 'Welcome to Giga Fleet'

@app.route('/planets')
def get_planets():
    return universe.Universe.get_universe().list_planets()

@app.route('/ship/<shipname>')
def get_ship(shipname):
    return universe.Universe.get_universe().get_ship(shipname).status()

if __name__ == '__main__':

    signal.signal(signal.SIGINT, signal_handler)

    cmd = GigaFleetCmd()
    t = threading.Thread(target=universe.worker, args=(cmd.cur_universe,))
    daemon = True
    t.start()
    #app.run(host='0.0.0.0')
    if sys.stdout.isatty():
        cmd.cmdloop()

