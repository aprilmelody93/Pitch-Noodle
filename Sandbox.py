import dearpygui.dearpygui as dpg
from math import sin

sindatax = []
sindatay = []
for i in range(0, 100):
    sindatax.append(i/100)
    sindatay.append(0.5 + 0.5*sin(50*i/100))

with dpg.window(label="Tutorial", width=400, height=400):

    # create plot
    dpg.add_text("Right click a series in the legend!")
    with dpg.plot(label="Line Series", height=-1, width=-1):

        dpg.add_plot_legend()

        dpg.add_plot_axis(dpg.mvXAxis, label="x")
        yaxis = dpg.add_plot_axis(dpg.mvYAxis, label="y")

        # series 1
        dpg.add_line_series(sindatax, sindatay, label="series 1", parent=yaxis)
        dpg.add_button(label="Delete Series 1", user_data = dpg.last_item(), parent=dpg.last_item(), callback=lambda s, a, u: dpg.delete_item(u))

        # series 2
        dpg.add_line_series(sindatax, sindatay, label="series 2", parent=yaxis)
        dpg.add_button(label="Delete Series 2", user_data = dpg.last_item(), parent=dpg.last_item(), callback=lambda s, a, u: dpg.delete_item(u))

dpg.start_dearpygui()