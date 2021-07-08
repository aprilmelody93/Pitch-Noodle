import dearpygui.dearpygui as dpg
from dearpygui.demo import *
from dearpygui.core import *



# add a font registry
with dpg.font_registry():
    
    # add font (set as default for entire app)
    dpg.add_font("Arial.ttf", 20, default_font=True)

    # add second font
    secondary_font = dpg.add_font("CAMBRIAZ.TTF", 13)

with dpg.window(label="Font Example"):
    dpg.add_button(label="Default font")
    dpg.add_button(label="Secondary font")
    
    # set font of specific widget
    dpg.set_item_font(dpg.last_item(), secondary_font)

show_demo()

dpg.start_dearpygui()

