# from pathlib import Path

# from pybattle.window.map.sound import Sound


# class Weather:
#     active = []
    
#     def __init__(self, particle: str, sound: Path, heaviness: int = 10):
#         self.particle = particle
#         self.sound = Sound(sound)
#         self.heaviness = heaviness
        
#         type(self).active.append(self)
        
# weather = Weather('|', Path('light_rain.mp3'))

# print(weather.sound.fade_in(3).play())