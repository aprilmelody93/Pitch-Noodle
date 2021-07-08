import dearpygui.dearpygui as dpg

xaxis = dpg.generate_uuid()
yaxis = dpg.generate_uuid()

with dpg.window(label="Tutorial", width=400, height=400):

    with dpg.group(horizontal=True):
        dpg.add_button(label="fit y", callback=lambda:dpg.fit_axis_data(yaxis))
        dpg.add_button(label="unlock x limits", callback=lambda:dpg.set_axis_limits_auto(xaxis))
        dpg.add_button(label="unlock y limits", callback=lambda:dpg.set_axis_limits_auto(yaxis))
        dpg.add_button(label="print limits x", callback=lambda:print(dpg.get_axis_limits(xaxis)))
        dpg.add_button(label="print limits y", callback=lambda:print(dpg.get_axis_limits(yaxis)))

    with dpg.plot(label="Bar Series", height=-1, width=-1):
        dpg.add_plot_legend()

        # create x axis
        dpg.add_plot_axis(dpg.mvXAxis, label="Student", no_gridlines=True, id=xaxis)
        dpg.set_axis_limits(dpg.last_item(), 9, 33)
        dpg.set_axis_ticks(dpg.last_item(), (("S1", 11), ("S2", 21), ("S3", 31)))
                
        # create y axis
        dpg.add_plot_axis(dpg.mvYAxis, label="Score", id=yaxis)      
        dpg.set_axis_limits(yaxis, 0, 110)

        # add series to y axis
        dpg.add_bar_series([10, 20, 30], [100, 75, 90], label="Final Exam", weight=1, parent=yaxis)
        dpg.add_bar_series([11, 21, 31], [83, 75, 72], label="Midterm Exam", weight=1, parent=yaxis)
        dpg.add_bar_series([12, 22, 32], [42, 68, 23], label="Course Grade", weight=1, parent=yaxis)

dpg.start_dearpygui()