#!/usr/bin/python
#coding=utf-8


import unittest

import ship

class Message:


    msg_text = []

    LANDING_REQUEST = 0
    msg_text.insert(LANDING_REQUEST, "demande d'atterissage")

    LANDING_REFUSED = 1
    msg_text.insert(LANDING_REFUSED, "demande d'atterissage refusée")


    def __init__(self, sender, type, content = None):
        self.sender = sender
        self.type = type
        self.content = content

    def __str__(self):
        return "Message envoyé par {} : {}".format(self.sender.name, Message.msg_text[self.type])

class TestMessageMethods(unittest.TestCase):
    def test_msg(self):

        ship0 = ship.Ship(100, 100)

        msg = Message(ship0, Message.LANDING_REQUEST)
        self.assertEquals(msg.type, Message.LANDING_REQUEST)

    def tearDown(self):
            ship.Ship.id = 0


if __name__ == '__main__':
    unittest.main()
