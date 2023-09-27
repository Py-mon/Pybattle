from copy import copy
from os import system
from random import randint, random
from textwrap import dedent
from time import sleep
from typing import Optional

from pybattle.screen.colors import Color, Colors
from pybattle.screen.frames.frame import Frame
from pybattle.screen.frames.map import Map
from pybattle.screen.frames.menu import Menu, Selection, SwitchSelection, VoidSelection
from pybattle.screen.frames.weather import Rain, Weather
from pybattle.screen.grid.matrix import Cell, Grid
from pybattle.screen.grid.point import Coord, Size
from pybattle.screen.window import Event, EventExit, EventQueue, Window, keys_pressing
from pybattle.types_ import CardinalDirection

# 7x24


r"""                                        




  
                                  
                                                                              
SQUIRREL                                    __/\       _─────_                                            
|||||||||||||..... 90/102                  / ,  \____ /       \                                                              
                                           \_____    \|    /   |                                       
    __/\       _─────_                     _|____/ ____ \   |  /                                                             
   / ,  \____ /       \                   |   |___/    \ \  |_/                                                              
   \_____    \|    /  |                    \_/ ___|      | /                                                                
  _|____/ ____ \   |  /                      /____\_____//                                                                          
 |   |___/    \ \  |_/                                                                                
  \_/ ___|      | /                                                                                    
     /____\_____//                                                                                  
                                                                              
"""


r"""
    __/\       _─────_  
   / ,  \____ /       \ 
   \_____    \|    /  | 
  _|____/ ____ \   |  / 
 |   |___/    \ \  |_/  
  \_/ ___|      | /      
     /____\_____//    
 ```
    __╱╲       _⎽⎼⎼⎼⎼⎽_  
   ╱ ,  ╲____ ╱       ╲ 
   ╲_____    ╲│    ╷  │ 
  _╷____/ ____ ╲   │  ╱ 
 │   │___╱    ╲ ╲  │_╱  
  ╲_╱ ___|      │ ╱     
     ╱____╲_____╱╱   
 ```
   _    _        
  ( \  / )       
   \ \/ /        
   |, , \        
   |     \       
   /     \       
  |  \ /  \ _\/_ 
  \     /    /   
 __\_ __\___/    
 ```
 ```
   _---_               
 << ,   \_____         
   \   /      \__       
    |  \________/=====- 
     \________/         
         __|_     
 ```
"""
