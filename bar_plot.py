import dearpygui.dearpygui as dpg

class AlgorithmVisualizer():
    size = 50
    blue = [30, 144, 255]
    red = [238, 75, 43]
    yellow = [253, 218, 13]
    green = [50, 205, 50]
    gray = [169, 169, 169]
    white = [255, 250, 250]
    
    def __init__(self):
        self.plot = self._createPlot()

        self.start = ()
        self.end = ()
        self.obstacles = []
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
        
        self._createTheme()
        self._leftClickHandler()
        
        
    def _createPlot(self):
        plot = dpg.add_plot(label="Algorithm",width=self.size * 10, height=self.size * 10, 
                      no_title=True, no_menus=True, no_mouse_pos=False, no_box_select=True, equal_aspects=True)
        x_axis = dpg.add_plot_axis(dpg.mvXAxis, parent=plot, label="", no_tick_labels=True, no_tick_marks=True, lock_min=True, no_gridlines=False)
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, parent=plot, label="", no_tick_labels=True, no_tick_marks=True, lock_min=True, no_gridlines=False)

        dpg.set_axis_limits(axis=x_axis, ymin=0, ymax=self.size)
        dpg.set_axis_limits(axis=y_axis, ymin=0, ymax=self.size)
        return plot
    
    def setStartEnd(self, start: tuple = None, end: tuple = None):
        if start:
            self.start = start
        if end:
            self.end = end
    
    def setObstacle(self, mouse_pos):
        x = (int)(mouse_pos[0] / 5)
        y = (int)(mouse_pos[1] / 5) 
        self.drawSquare((x, y), self.gray)
        self.obstacles.append((x, y))
    
    def clickAddObstacle(self):
        """
        Callback of `_leftClickHandler` when `mvMouseButton_Left`.
        """
        if (dpg.is_item_clicked(self.plot)):
            mouse_pos = dpg.get_plot_mouse_pos()
            self.setObstacle(mouse_pos)
    
    def clearObstacleList(self):
        self.obstacles.clear()
    
    # Drawing in the plot
    
    def drawAllSquares(self):
        """ 
        Delete all drawn items in the plot and then draw the `start`, `end` and each `obstacle` in the obstacles list.
        """
        dpg.delete_item(self.plot, children_only=True, slot=2)
        self.drawSquare(self.start, self.green)
        self.drawSquare(self.end, self.white)
        for obstacle_xy in self.obstacles:
            self.drawSquare(obstacle_xy, self.gray)
    
    def drawSquare(self, xy: tuple, colorRGB: list = [0, 0, 0], thick = 0):
        x, y = xy
        dpg.draw_rectangle(parent=self.plot, pmin=[x*5, y*5], pmax=[(x*5)+5, (y*5)+5], color=colorRGB, fill=colorRGB, thickness=thick)
        
    def drawText(self, text: str, xy: tuple, size: int = 5):
        x, y = xy
        dpg.draw_text(parent=self.plot, text=text, pos=[x, y], size=size)

    # Themes and Handlers
    
    def _leftClickHandler(self):
        with dpg.handler_registry():
            dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Left, callback=self.clickAddObstacle)

    def _createTheme(self):
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
