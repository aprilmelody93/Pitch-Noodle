import dearpygui.dearpygui as dpg

with dpg.window():
    item = dpg.add_button(enabled=True, label="Press me")
    dpg.configure_item(item, enabled=False, label="New Label")

    dpg.get_item_configuration()
dpg.start_dearpygui()