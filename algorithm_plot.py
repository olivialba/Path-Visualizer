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

        self.start = None
        self.start_drawing_alias = None
        self.start_text = None

        self.end = None
        self.end_drawing_alias = None
        self.end_text = None
        
        self.obstacles_list = []
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
        self._clickHandler()
        
        
    def _createPlot(self):
        plot = dpg.add_plot(label="Algorithm",width=self.size * 10, height=self.size * 10, 
                      no_title=True, no_menus=True, no_mouse_pos=False, no_box_select=True, equal_aspects=True)
        x_axis = dpg.add_plot_axis(dpg.mvXAxis, parent=plot, label="", no_tick_labels=True, no_tick_marks=True, lock_min=True, no_gridlines=False)
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, parent=plot, label="", no_tick_labels=True, no_tick_marks=True, lock_min=True, no_gridlines=False)

        dpg.set_axis_limits(axis=x_axis, ymin=0, ymax=self.size)
        dpg.set_axis_limits(axis=y_axis, ymin=0, ymax=self.size)
        return plot
    
    # Methods
    
    def setStart(self, start: tuple = None):
        if start is None:
            dpg.set_value(self.start_text, "None")
            dpg.delete_item(self.start_drawing_alias)
            self.start_drawing_alias = None
            self.start = None
        else:
            dpg.set_value(self.start_text, start)
            self.start_drawing_alias = self.drawSquare(start, self.green, need_return=True)
            self.start = start
        
    def setEnd(self, end: tuple = None):
        if end is None:
            dpg.set_value(self.end_text, "None")
            dpg.delete_item(self.end_drawing_alias)
            self.end_drawing_alias = None
            self.end = None
        else:
            dpg.set_value(self.end_text, end)
            self.end_drawing_alias = self.drawSquare(end, self.white, need_return=True)
            self.end = end
    
    def setObstacle(self, xy):
        self.drawSquare(xy, self.gray)
        self.obstacles_list.append(xy)
        
    def clearObstacleList(self):
        self.obstacles_list.clear()
    
    def mousePlotPosToXY(self, mouse_pos):
        """
        Returns a tuple `(x, y)` of the PLOT mouse position.
        """
        x = (int)(mouse_pos[0] / 5)
        y = (int)(mouse_pos[1] / 5) 
        return (x, y)
    
    # Drawing in the plot
    
    def drawAllSquares(self):
        """ 
        Delete all drawn items in the plot and then draw the `start`, `end` and each `obstacle` in the obstacles list.
        """
        dpg.delete_item(self.plot, children_only=True, slot=2)
        self.start_drawing_alias = self.drawSquare(self.start, self.green, need_return=True)
        self.end_drawing_alias = self.drawSquare(self.end, self.white, need_return=True)
        for obstacle_xy in self.obstacles_list:
            self.drawSquare(obstacle_xy, self.gray)
    
    def drawSquare(self, xy: tuple, colorRGB: list = [0, 0, 0], thick = 0, need_return: bool = None):
        x, y = xy
        x *= 5
        y *= 5
        square = dpg.draw_rectangle(parent=self.plot, pmin=[x, y], pmax=[x+5, y+5], color=colorRGB, fill=colorRGB, thickness=thick)
        if need_return:
            return square
        else:
            return None
        
    def drawText(self, text: str, xy: tuple, size: int = 5):
        dpg.draw_text(parent=self.plot, text=text, pos=xy, size=size)

    def errorMessage(self, text):
        dpg.set_value("error_message_plot", text)
        
    # Themes and Handlers
    
    def _setTextValues(self, start_text, end_text):
        self.start_text = start_text
        self.end_text = end_text
    
    def _clickAdd_Obstacle(self):
        """
        Callback of `_clickHandler` when `mvMouseButton_Left`.
        """
        if (dpg.is_item_clicked(self.plot)):
            mouse_pos = dpg.get_plot_mouse_pos()
            xy = self.mousePlotPosToXY(mouse_pos)
            self.setObstacle(xy)
            
    def _clickAdd_StartEnd(self):
        """
        Callback of `_clickHandler` when `mvMouseButton_Right`.
        """
        if (dpg.is_item_clicked(self.plot)):
            mouse_pos = dpg.get_plot_mouse_pos()
            xy = self.mousePlotPosToXY(mouse_pos)
            
            if xy == self.start:
                self.setStart(None)
            elif xy == self.end:
                self.setEnd(None)
                
            elif self.start is None:
                self.setStart(xy)
            elif self.end is None:
                self.setEnd(xy)
    
    def _clickHandler(self):
        with dpg.handler_registry():
            dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Left, callback=self._clickAdd_Obstacle)
            dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Right, callback=self._clickAdd_StartEnd)

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
