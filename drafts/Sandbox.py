import dearpygui.dearpygui as dpg

dpg.setup_registries()

with dpg.window(label="tutorial"):
    dpg.add_button(label="Press me")
    dpg.draw_line((10, 10), (100, 100), color=(255, 0, 0, 255), thickness=1)

# print children    
print("Last root: ", dpg.get_item_children(dpg.last_root()))

# print children in slot 1
print("Last root slot 1: ", dpg.get_item_children(dpg.last_root(), 1))

# check draw_line's slot
print("Last item: ", dpg.get_item_slot(dpg.last_item()))


dpg.start_dearpygui()