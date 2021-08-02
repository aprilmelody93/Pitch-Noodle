from dearpygui.dearpygui import *

def del_group(sender, app_data, user_data):
    # delete_item(Button1)
    print(group1)
    delete_item(group1)

with window(label="DearPyGui"):
    Button1 = add_button(label="Button1")
    add_button(label="Button2")

    add_same_line()
    add_button(label="Button3", callback=del_group)

    add_button(label="Button4")
    add_button(label="Button5")
    add_same_line()

    # group_name = generate_uuid()
    # print("group name: ", group_name)

    with group() as group1:
        add_button(label="Button6")
        add_button(label="Button7")

start_dearpygui()

# import dearpygui.dearpygui as dpg

# # pregenerate ids
# delete_button = dpg.generate_uuid()
# secondary_window = dpg.generate_uuid()

# # id's will be generated later
# new_button1 = 0
# new_button2 = 0

# def add_buttons():
#     global new_button1, new_button2
#     new_button1 = dpg.add_button(label="New Button", before=delete_button)
#     new_button2 = dpg.add_button(label="New Button 2", parent=secondary_window)

# def delete_buttons():
#     dpg.delete_item(new_button1)
#     dpg.delete_item(new_button2)


# with dpg.window(label="Tutorial", pos=(200, 200)):
#     dpg.add_button(label="Add Buttons", callback=add_buttons)
#     dpg.add_button(label="Delete Buttons", callback=delete_buttons, id=delete_button)

# with dpg.window(label="Secondary Window", id=secondary_window, pos=(100, 100)):
#     pass

# dpg.start_dearpygui()