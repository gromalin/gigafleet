from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import threading
from giga_fleet import app
import universe
import player

t = threading.Thread(target=universe.worker, args=(universe.Universe.get_universe(),))
daemon = True
player1 = player.Player("Thomas", universe.Universe.get_universe())
player1.add_fleet("Fleet_0")
fleet_0 = player1.get_fleet("Fleet_0")
fleet_0.do_add("Planet_0 30 FastShip")
fleet_0.do_go("Planet_1 Planet_0")

t.start()
print("Universe thread started")

print("Starting Tornado server ")
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)
IOLoop.instance().start()
