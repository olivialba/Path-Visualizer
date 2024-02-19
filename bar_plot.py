import dearpygui.dearpygui as dpg
import DearPyGui_DragAndDrop as dpg_dnd


class AlgorithmVisualizer():
    size = 50
    blue = [30, 144, 255]
    red = [238, 75, 43]
    yellow = [253, 218, 13]
    green = [50, 205, 50]
    gray = [169, 169, 169]
    white = [255, 250, 250]
    
    def __init__(self):
        self._CreatePlot()
        self.array = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.obstacles = []
        self.start = ()
        self.end = ()
        
    def _CreatePlot(self):
        self.plot = dpg.add_plot(label="Algorithm",width=self.size * 10, height=self.size * 10, 
                      no_title=True, no_menus=True, no_mouse_pos=False, no_box_select=True, equal_aspects=True)
        x_axis = dpg.add_plot_axis(dpg.mvXAxis, parent=self.plot, label="", no_tick_labels=True, no_tick_marks=True, lock_min=True, no_gridlines=False)
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, parent=self.plot, label="", no_tick_labels=True, no_tick_marks=True, lock_min=True, no_gridlines=False)

        dpg.set_axis_limits(axis=x_axis, ymin=0, ymax=self.size)
        dpg.set_axis_limits(axis=y_axis, ymin=0, ymax=self.size)
        self._CreateTheme()
        self.leftClick()
    
    def setSquares(self, start: tuple = None, end: tuple = None):
        if start:
            self.start = start
        if end:
            self.end = end
    
    def leftClick(self):
        with dpg.handler_registry() as mouse_handler:
            m_click_left = dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Left, callback=self.clickPlot, )
            
    def clickPlot(self):
        if (dpg.is_item_clicked(self.plot)):
            mouse_pos = dpg.get_plot_mouse_pos()
            self.setObstacle(mouse_pos)
    
    def setObstacle(self, mouse_pos):
        x = (int)(mouse_pos[0] / 5)
        y = (int)(mouse_pos[1] / 5) 
        self.graySquare((x, y))
        self.obstacles.append((x, y))
    
    def resetWalls(self):
        self.obstacles.clear()
    
    def paintAllSquares(self):
        dpg.delete_item(self.plot, children_only=True, slot=2)
        self.greenSquare(self.start)
        self.whiteSquare(self.end)
        for obstacle_xy in self.obstacles:
            self.graySquare(obstacle_xy)
    
    def blueSquare(self, xy: tuple):
        self.colorSquare(xy, colorRGB=self.blue)

    def redSquare(self, xy: tuple):
        self.colorSquare(xy, colorRGB=self.red)
    
    def yellowSquare(self, xy: tuple):
        self.colorSquare(xy, colorRGB=self.yellow)
        
    def greenSquare(self, xy: tuple):
        self.colorSquare(xy, colorRGB=self.green)
        
    def graySquare(self, xy: tuple):
        self.colorSquare(xy, colorRGB=self.gray)
        
    def whiteSquare(self, xy: tuple):
        self.colorSquare(xy, colorRGB=self.white)

    def colorSquare(self, xy: tuple, colorRGB: list = [0, 0, 0], thick = 0):
        x, y = xy
        dpg.draw_rectangle(parent=self.plot, pmin=[x*5, y*5], pmax=[(x*5)+5, (y*5)+5], color=colorRGB, fill=colorRGB, thickness=thick)
        
    def drawText(self, text: str, xy: tuple, size: int = 5):
        x, y = xy
        dpg.draw_text(parent=self.plot, text=text, pos=[x, y], size=size)
                
    def _CreateTheme(self):
        with dpg.theme() as plot_style:
            with dpg.theme_component(dpg.mvPlot):
                dpg.add_theme_style(dpg.mvPlotStyleVar_PlotPadding, 0, 0, category=dpg.mvThemeCat_Plots)
                dpg.add_theme_style(dpg.mvPlotStyleVar_LineWeight, 0, category=dpg.mvThemeCat_Plots)
                dpg.add_theme_style(dpg.mvPlotStyleVar_MajorTickSize, 0, 0, category=dpg.mvThemeCat_Plots)
        with dpg.theme() as plot_color_red:
            with dpg.theme_component(dpg.mvPlot):
                dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 0, 0, 255), category=dpg.mvThemeCat_Plots)
                dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 0, 0, 255), category=dpg.mvThemeCat_Plots)
        dpg.bind_item_theme(self.plot, plot_style)
