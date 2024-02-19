import dearpygui.dearpygui as dpg
import DearPyGui_DragAndDrop as dpg_dnd
from bar_plot import AlgorithmVisualizer
from algorithms.a_star import a_star


dpg.create_context()
dpg_dnd.initialize()
dpg.create_viewport(title='Search Visualizer', height=560, width=800)

plot = object()
algorithms = {
    'A*' : 'A* Search',
}

def start_algorithm(send, app_data, user_data: AlgorithmVisualizer):    
    # start_XY = (dpg.get_value('startX'), dpg.get_value('startY'))
    # goal_XY = (dpg.get_value('endX'), dpg.get_value('endY'))
    # user_data.setStart(start=start_XY)
    # user_data.setEnd(end=goal_XY)

    
    combo_choice = dpg.get_value('algorithm_choice')
    if (combo_choice == algorithms['A*']):
        a_star(plot=user_data)
        
def reset_plot(send, app_data, user_data: AlgorithmVisualizer):
    user_data.setStart(None)
    user_data.setEnd(None)
    user_data.clearObstacleList()
    dpg.delete_item(user_data.plot, children_only=True, slot=2)

def start_end_positions():
    dpg.add_text("Start position:")
    with dpg.group(horizontal=True):
        dpg.add_text("X: ", indent=20)
        dpg.add_input_int(tag="startX", width=80, min_value=0, max_value=10, min_clamped=True, max_clamped=True)
    with dpg.group(horizontal=True):
        dpg.add_text("Y: ", indent=20)
        dpg.add_input_int(tag="startY", width=80, min_value=0, max_value=10, min_clamped=True, max_clamped=True)
    dpg.add_spacer(height=10)
    dpg.add_text("End position:")
    with dpg.group(horizontal=True):
        dpg.add_text("X: ", indent=20)
        dpg.add_input_int(tag="endX", width=80, min_value=0, max_value=10, min_clamped=True, max_clamped=True)
    with dpg.group(horizontal=True):
        dpg.add_text("Y: ", indent=20)
        dpg.add_input_int(tag="endY", width=80, min_value=0, max_value=10, min_clamped=True, max_clamped=True)

with dpg.window(tag="main_window"):
    with dpg.table(header_row=False, borders_innerH=True, borders_innerV=True, 
                   borders_outerH=True, borders_outerV=True):
        dpg.add_table_column(width_fixed=True, init_width_or_weight=250)
        dpg.add_table_column()
        with dpg.table_row():
            
            plot_canvas = AlgorithmVisualizer()
            plot_graph = plot_canvas.plot
            
            with dpg.group(before=plot_graph):
                # Algorithms ComboBox
                dpg.add_spacer(height=10)
                dpg.add_text("Algorithm: ")
                dpg.add_combo([text for key, text in algorithms.items()], tag='algorithm_choice')
                # Start & End XY Buttons
                dpg.add_spacer(height=10)
                start_end_positions()
                # Reset Walls & Start
                dpg.add_spacer(height=10)
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Reset Plot", callback=reset_plot, user_data=plot_canvas)
                    dpg.add_button(label="Start", callback=start_algorithm, user_data=plot_canvas)


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)
dpg.start_dearpygui()
dpg.destroy_context()