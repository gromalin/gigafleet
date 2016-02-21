#!/usr/bin/python
#coding=utf-8


import unittest

import elem

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

    elem = None

    def setUp(self):
        self.elem = elem.Elem(100, 100)

    def tearDown(self):
        elem.Elem.id = 0

    def test_msg(self):

        msg = Message(self.elem, Message.LANDING_REQUEST)
        self.assertEquals(msg.type, Message.LANDING_REQUEST)

if __name__ == '__main__':
    unittest.main()
