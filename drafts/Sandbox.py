from dearpygui.core import *
import dearpygui.dearpygui as dpg

def change_me (sender, user_data):
    configure_item(item, enabled=False, label="New Label")

with dpg.window(label="test"):  
    item = add_button(enabled=True, label="Press me", callback = change_me)

dpg.start_dearpygui()