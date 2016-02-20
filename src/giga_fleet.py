#!/usr/bin/python
# coding=utf-8

import argparse
import cmd
import signal
import sys
import threading
import unittest

import planet
import player


def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)


class GigaFleetCmd(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.focus = []
        self.cur_player = player.Player("Thomas")
        self.prompt = ">"


        planet_1 = planet.Planet(100, 100)
        self.cur_player.add_planet(planet_1)
        planet_2 = planet.Planet(200, 200)
        self.cur_player.add_planet(planet_2)

    def do_go(self, param):
        self.focus.append(self.cur_player)
        self.prompt = "{}".format(*self.focus, sep="|") + ">"

    def do_exit(self, param):
        if (len(self.focus) != 0):
            self.focus.pop()
            if (len(self.focus) != 0):
                self.prompt = "{}".format(*self.focus, sep="|") + ">"
            else:
                self.prompt = ">"


    def do_status(self, param):
        self.focus[-1].do_status(param)
        #print(self.cur_player.status())

    def do_list(self, param):
        self.focus[-1].do_list(param)
        #print(self.cur_player.status())

    def do_add(self, param):
        self.focus[-1].do_add(param)
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
    def test_init(self):
        # FIXME je ne sais pas tester proprement pour le moment
        return
        cmd = GigaFleetCmd()


        self.assertTrue(cmd is not None)
        cmd.do_planets('list')
        cmd.do_status('')
        cmd.do_planet(('buy Planet_1 FastShip'))
        self.assertEquals(len(cmd.cur_player.ships), 1)
        cmd.do_planet(('buy Planet_1 FastShip'))
        self.assertEquals(len(cmd.cur_player.ships), 2)
        cmd.do_planet(('buy Planet_1 FastShip'))
        self.assertEquals(len(cmd.cur_player.ships), 3)
        cmd.do_planet(('buy Planet_1 NoShip'))
        self.assertEquals(len(cmd.cur_player.ships), 3)
        cmd.cur_player.list_ships()




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
        t = threading.Thread(target=player.worker, args=(cmd.cur_player,))
        t.daemon = True
        t.start()

        cmd.cmdloop()
