#!/usr/bin/python
# coding=utf-8

import unittest
import warnings

import elem
import message
import ship


class GigaSite(elem.Elem):
    id = 0

    def __init__(self, x, y):
        elem.Elem.__init__(self, x, y)
        self.__class__.id = self.__class__.id + 1
        self.slots = []
        self.slots_nb = 5
        self.waiting = []

    def run(self):
        msg = self.get_msg();
        if msg is not None:

            if (msg.type == message.Message.LANDING_REQUEST):
                if (len(self.slots) == self.slots_nb):
                    warnings.warn("{} -> {} : plus de slots disponibles".format(
                        self.name, msg.sender.name))
                    msg.sender.post_msg(message.Message(
                        self, message.Message.LANDING_REFUSED))
                    return

                if (msg.sender in self.slots):
                    warnings.warn("{} -> {} : vaisseau déjà arrimé".format(
                        self.name, msg.sender.name))
                    return

                self.slots.append(msg.sender)


class TestGigaSiteMethods(unittest.TestCase):
    site = None

    def setUp(self):
        self.site = GigaSite(100, 100)
        self.ship0 = ship.Ship(100, 100)

    def tearDown(self):
        GigaSite.id = 0

    def test_message(self):
        self.site.post_msg("coucou")
        msg = self.site.get_msg()
        self.assertEquals(msg, "coucou")

        self.site.post_msg(message.Message(self.ship0, message.Message.LANDING_REQUEST))
        self.site.run()
        self.assertIs(self.site.slots[0], self.ship0)
        self.site.post_msg(message.Message(self.ship0, message.Message.LANDING_REQUEST))

        # On ne prend pas 2 fois le meme vaisseau
        self.site.run()
        self.assertEquals(len(self.site.slots), 1)

        # On surcharge l'arrivée
        self.site.post_msg(message.Message(ship.Ship(100, 100), message.Message.LANDING_REQUEST))
        self.site.run()
        self.site.post_msg(message.Message(ship.Ship(100, 100), message.Message.LANDING_REQUEST))
        self.site.run()
        self.site.post_msg(message.Message(ship.Ship(100, 100), message.Message.LANDING_REQUEST))
        self.site.run()
        self.site.post_msg(message.Message(ship.Ship(100, 100), message.Message.LANDING_REQUEST))
        self.site.run()
        ship1 = ship.Ship(100, 100)
        self.site.post_msg(message.Message(ship1, message.Message.LANDING_REQUEST))
        self.site.run()
        print(ship1.get_msg())


if __name__ == '__main__':
    unittest.main()
