import dearpygui.dearpygui as dpg
import DearPyGui_DragAndDrop as dpg_dnd
from algorithm_plot import AlgorithmVisualizer
from algorithms.a_star import A_star


dpg.create_context()
dpg_dnd.initialize()
dpg.create_viewport(title='Search Visualizer', height=560, width=815)

show_euristic = False
algorithms = {
    'A*' : 'A* Search',
}

# Events

def startAlgorithm(send, app_data, user_data: AlgorithmVisualizer):    
    combo_choice = dpg.get_value('algorithm_choice')
    if (combo_choice == algorithms['A*']):
        A_star(plot=user_data, show_heuristic=show_euristic)
        
def resetPlot(send, app_data, user_data: AlgorithmVisualizer):
    user_data.resetPlot()
    
def changePlotSize(send, app_data, user_data: AlgorithmVisualizer):
    user_data.setSizeArray(dpg.get_value("plot_size"))
    user_data.resetPlot()

def generateMaze(send, app_data, user_data: AlgorithmVisualizer):
    user_data.setMaze()
    
def showEuristic(send, app_data, user_data: AlgorithmVisualizer):
    global show_euristic
    show_euristic = dpg.get_value("show_euristic")

# GUI Elements

def plot_size(plot: AlgorithmVisualizer):
    dpg.add_text("Plot size:")
    with dpg.group(horizontal=True):
        dpg.add_slider_int(tag="plot_size", min_value=2, max_value=50, clamped=True, default_value=15)
        dpg.add_button(label="Change", callback=changePlotSize, user_data=plot)

def start_end_coordinates(plot: AlgorithmVisualizer):
    dpg.add_text("Start Coordinate:", indent=10)
    start_pos_text = dpg.add_text("None", indent=20)
    dpg.add_spacer()
    dpg.add_text("End Coordinate:", indent=10)
    end_pos_text = dpg.add_text("None", indent=20)
    
    plot._setTextValues(start_pos_text, end_pos_text)

with dpg.window(tag="main_window"):
    with dpg.table(header_row=False, borders_innerH=True, borders_innerV=True, 
                   borders_outerH=True, borders_outerV=True):
        dpg.add_table_column(width_fixed=True, init_width_or_weight=250)
        dpg.add_table_column()
        with dpg.table_row():
            
            plot_canvas = AlgorithmVisualizer()
            plot_graph = plot_canvas.plot
            
            with dpg.group(before=plot_graph, indent=10):
                # Algorithms ComboBox
                dpg.add_spacer(height=10)
                dpg.add_text("Algorithm: ")
                dpg.add_combo([text for key, text in algorithms.items()], tag='algorithm_choice', default_value=list(algorithms.values())[0])
                # Generate Maze
                dpg.add_spacer()
                with dpg.group():
                    dpg.add_text("Maze:")
                    dpg.add_button(label="Generate Maze", callback=generateMaze, user_data=plot_canvas)
                    
                # Start & End XY Buttons
                dpg.add_spacer(height=30)
                plot_size(plot_canvas)
                dpg.add_spacer(height=5)
                dpg.add_checkbox(label="Show Heuristic", tag="show_euristic", callback=showEuristic)
                dpg.add_spacer(height=25)
                start_end_coordinates(plot_canvas)
                # Reset Walls & Start
                dpg.add_spacer(height=10)
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Reset Plot", callback=resetPlot, user_data=plot_canvas)
                    dpg.add_button(label="Start", callback=startAlgorithm, user_data=plot_canvas)
                dpg.add_spacer(height=10)
                dpg.add_text("", tag="error_message_plot", wrap=400)
                dpg.add_spacer(height=10)


# Setup

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)
dpg.start_dearpygui()
dpg.destroy_context()