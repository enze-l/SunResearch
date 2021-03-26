from networking import Networking
from light_sensor import LightSensor

print("Starting Lightmodule...")
lightsensor = LightSensor()
print("Lightmodule started")

print("Starting Server...")
networking = Networking(lightsensor)
print("Networking started")
