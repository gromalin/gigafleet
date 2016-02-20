#!/usr/bin/python
#coding=utf-8

import unittest
import warnings

import elem
import message


class GigaSite(elem.Elem):

  id = 0
  def __init__(self,x,y):
    elem.Elem.__init__(self, x, y)
    self.__class__.id = self.__class__.id + 1
    self.slots = []
    self.slots_nb = 5
    self.waiting = []

  def run(self):
    msg = self.get_msg();
    if msg is not None:

      if(msg.type == message.Message.LANDING_REQUEST):
        if(len(self.slots) == self.slots_nb):
          warnings.warn("{} -> {} : plus de slots disponibles".format(
            self.name, msg.sender.name))
          msg.sender.post_msg(message.Message(
            self, message.Message.LANDING_REFUSED))
          return
    
        if(msg.sender in self.slots):
          warnings.warn("{} -> {} : vaisseau déjà arrimé".format(
            self.name, msg.sender.name))
          return
    
        self.slots.append(msg.sender)
          

class TestGigaSiteMethods(unittest.TestCase):
  def test_get_name(self):


    site = GigaSite(100,100)
    self.assertEquals(site.get_name(), 'GigaSite_0')
    site.post_msg("coucou")
    msg = site.get_msg()
    self.assertEquals(msg, "coucou")


    ship0 = ship.Ship(100, 100)
    site.post_msg(message.Message(ship0, message.Message.LANDING_REQUEST))
    site.run()
    self.assertIs(site.slots[0], ship0)
    site.post_msg(message.Message(ship0, message.Message.LANDING_REQUEST))

    # On ne prend pas 2 fois le meme vaisseau
    site.run()
    self.assertEquals(len(site.slots), 1)

    # On surcharge l'arrivée
    site.post_msg(message.Message(ship.Ship(100, 100), message.Message.LANDING_REQUEST))
    site.run()
    site.post_msg(message.Message(ship.Ship(100, 100), message.Message.LANDING_REQUEST))
    site.run()
    site.post_msg(message.Message(ship.Ship(100, 100), message.Message.LANDING_REQUEST))
    site.run()
    site.post_msg(message.Message(ship.Ship(100, 100), message.Message.LANDING_REQUEST))
    site.run()
    ship1 = ship.Ship(100, 100)
    site.post_msg(message.Message(ship1, message.Message.LANDING_REQUEST))
    site.run()
    print(ship1.get_msg())



if __name__ == '__main__':
    unittest.main()
