import dearpygui.dearpygui as dpg
import DearPyGui_DragAndDrop as dpg_dnd
import dearpygui.demo as demo
from bar_plot import AlgorithmVisualizer
from algorithms.a_star import a_star
import os


dpg.create_context()
dpg_dnd.initialize()
dpg.create_viewport(title='Search Visualizer', height=560, width=800)

plot = object()
algorithms = {
    'A*' : 'A* Search',
}

def start_algorithm(send, app_data, user_data):
    
    choice = dpg.get_value('algorithm_choice')
    startX = dpg.get_value('startX')
    startY = dpg.get_value('startY')
    endX = dpg.get_value('endX')
    endY = dpg.get_value('endY')
    
    start_node = (startX, startY)
    goal_node = (endX, endY)
    user_data.setSquares(start=start_node, end=goal_node)
    
    if (choice == algorithms['A*']):
        a_star(plot=user_data, start_xy=start_node, goal_xy=goal_node)
        
def start_end_positions():
    dpg.add_text("Start position:")
    with dpg.group(horizontal=True):
        dpg.add_text("X: ", indent=20)
        startx = dpg.add_input_int(tag="startX", width=80, min_value=0, max_value=10, min_clamped=True, max_clamped=True)
    with dpg.group(horizontal=True):
        dpg.add_text("Y: ", indent=20)
        starty = dpg.add_input_int(tag="startY", width=80, min_value=0, max_value=10, min_clamped=True, max_clamped=True)
    dpg.add_spacer(height=10)
    dpg.add_text("End position:")
    with dpg.group(horizontal=True):
        dpg.add_text("X: ", indent=20)
        endx = dpg.add_input_int(tag="endX", width=80, min_value=0, max_value=10, min_clamped=True, max_clamped=True)
    with dpg.group(horizontal=True):
        dpg.add_text("Y: ", indent=20)
        endy = dpg.add_input_int(tag="endY", width=80, min_value=0, max_value=10, min_clamped=True, max_clamped=True)

def clearWalls(send, app_data, user_data):
    user_data.resetWalls()
    dpg.delete_item(user_data.plot, children_only=True, slot=2)

with dpg.window(tag="main_window"):
    with dpg.table(header_row=False, borders_innerH=True, borders_innerV=True, borders_outerH=True, borders_outerV=True):
        dpg.add_table_column(width_fixed=True, init_width_or_weight=250)
        dpg.add_table_column()
        with dpg.table_row():
            plot = AlgorithmVisualizer()
            plot_graph = plot.plot
            with dpg.group(before=plot_graph):
                dpg.add_spacer(height=10)
                dpg.add_text("Algorithm: ")
                dpg.add_combo([text for key, text in algorithms.items()], tag='algorithm_choice')
                dpg.add_spacer(height=10)
                start_end_positions()
                dpg.add_spacer(height=10)
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Reset Walls", callback=clearWalls, user_data=plot)
                    dpg.add_button(label="Start", callback=start_algorithm, user_data=plot)

#demo.show_demo()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)
dpg.start_dearpygui()
dpg.destroy_context()