#!/usr/bin/python
# coding=utf-8

import unittest
import warnings

import elem
import message


class GigaSite(elem.Elem):
    id = 0

    def __init__(self, x, y):
        elem.Elem.__init__(self, x, y)

        self.__class__.id = self.__class__.id + 1
        self.slots = []
        self.slots_nb = 5
        self.waiting = []
        self.trace = False

    def run(self):
        getter = self.get_msg();
        for msg in getter:

            if (msg.type == message.Message.LANDING_REQUEST):
                if (len(self.slots) == self.slots_nb):
                    if(self.trace):
                        print("{} -> {} : plus de slots disponibles".format(
                            self.name, msg.sender.name))
                    msg.sender.post_msg(message.Message(
                        self, message.Message.LANDING_REFUSED))
                    continue

                if (msg.sender in self.slots ):
                    if self.trace:
                        print("{} -> {} : vaisseau déjà arrimé".format(
                        self.name, msg.sender.name))
                    continue

                msg.sender.post_msg(message.Message(self, message.Message.LANDING_ACCEPTED))
                self.slots.append(msg.sender)
            elif(msg.type == message.Message.LEAVING):
                self.slots.remove(msg.sender)
                print("occupied slots : {}, available slots : {}".format(len(self.slots),self.slots_nb - len(self.slots)))
import ship
import universe

class TestGigaSiteMethods(unittest.TestCase):

    site = None

    def setUp(self):

        self.site = GigaSite(100, 100)
        self.ship0 = ship.Ship(universe.Universe.get_universe().get_planet("Planet_0"))

    def tearDown(self):
        GigaSite.id = 0

    def test_message(self):

        self.site.post_msg("hello")
        msg = next(self.site.get_msg())
        self.assertEquals(msg, "hello")

        self.site.post_msg(message.Message(self.ship0, message.Message.LANDING_REQUEST))
        self.site.run()
        self.assertIs(self.site.slots[0], self.ship0)

        # We don't accept a same ship two times
        self.site.post_msg(message.Message(self.ship0, message.Message.LANDING_REQUEST))
        self.site.run()
        self.assertEquals(1, len(self.site.slots))

        # On surcharge l'arrivée
        for it in range(5):
            tmp_ship =  ship.Ship(universe.Universe.get_universe().get_planet("Planet_0"))
            self.site.post_msg(message.Message(tmp_ship, message.Message.LANDING_REQUEST))
            self.site.run()
            # 5 slots, one ship already present
            if(it < 4):
                self.assertEquals(message.Message.LANDING_ACCEPTED,next(tmp_ship.get_msg()).type)
            else:
                self.assertEquals(message.Message.LANDING_REFUSED,next(tmp_ship.get_msg()).type)

if __name__ == '__main__':
    unittest.main()
