import dearpygui.dearpygui as dpg

def button_callback(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")

with dpg.window(label="Tutorial"):

    dpg.add_button(label="Apply", callback=button_callback, user_data="Some Data")

dpg.start_dearpygui() 