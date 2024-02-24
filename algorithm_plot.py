import dearpygui.dearpygui as dpg
from algorithms.maze_gen import maze_gen

class AlgorithmVisualizer():
    blue = (30, 144, 255)
    red = (238, 75, 43)
    yellow = (253, 218, 13)
    green = (50, 205, 50)
    gray = (169, 169, 169)
    white = (255, 250, 250)
    
    def __init__(self):
        self.size = 20
        self.square = 1
        self.plot = self._createPlot()

        self.start = None
        self.start_drawing_alias = None
        self.start_text = None

        self.end = None
        self.end_drawing_alias = None
        self.end_text = None
        
        self.obstacles_list = []
        self.gridlines = []
        self.array = []
        
        self._createArray()
        self.drawGridlines()
        self._createTheme()
        self._clickHandler()        
        
    def _createPlot(self):
        plot = dpg.add_plot(label="Algorithm",width=500, height=500, 
                      no_title=True, no_menus=True, no_mouse_pos=False, no_box_select=True, equal_aspects=True)
        self.x_axis = dpg.add_plot_axis(dpg.mvXAxis, parent=plot, label="", no_tick_labels=True, no_tick_marks=True, lock_min=True, no_gridlines=True)
        self.y_axis = dpg.add_plot_axis(dpg.mvYAxis, parent=plot, label="", no_tick_labels=True, no_tick_marks=True, lock_min=True, no_gridlines=True)

        dpg.set_axis_limits(axis=self.x_axis, ymin=0, ymax=self.size)
        dpg.set_axis_limits(axis=self.y_axis, ymin=0, ymax=self.size)
        return plot
    
    def _createArray(self):
        self.array.clear()
        for y in range(self.size):
            self.array.append([])
            for x in range(self.size):
                self.array[y].append(0)
    
    # Methods
    
    def setStart(self, start: tuple = None):
        if start is None:
            dpg.set_value(self.start_text, "None")
            dpg.delete_item(self.start_drawing_alias)
            self.start_drawing_alias = None
            self.start = None
        else:
            if self.array[self.getReverseY(start[1])][start[0]] == 1:
                return
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
            if self.array[self.getReverseY(end[1])][end[0]] == 1:
                return
            dpg.set_value(self.end_text, end)
            self.end_drawing_alias = self.drawSquare(end, self.white, need_return=True)
            self.end = end
    
    def setObstacle(self, xy: tuple):
        if (xy == self.start or xy == self.end):
            return
        self.drawSquare(xy, self.gray)
        x, y = xy
        new_y = (y + (self.size - 1) - (2 * y))
        self.array[new_y][x] = 1
        
    def setSizeArray(self, size: int):
        self.size = size
        self._createArray()
    
    def setSquareSide(self, size: int):
        self.square = size
                
    def setMaze(self):
        self.resetPlot()
        maze = maze_gen(self)
        if maze:
            self.array = maze
            for num_y, y in enumerate(self.array):
                for num_x, x in enumerate(y):
                    if x == 1:
                        self.drawSquare((num_x, self.getReverseY(num_y)), self.gray)
        else:
            self.errorMessage("* Error Maze: Plot size < 6")
    
    def getReverseY(self, y: int):
        return (y + (self.size - 1) - (2 * y))
    
    def resetPlot(self):
        self.setStart(None)
        self.setEnd(None)
        dpg.delete_item(self.plot, children_only=True, slot=2)
        dpg.set_axis_limits(axis=self.x_axis, ymin=0, ymax=self.size)
        dpg.set_axis_limits(axis=self.y_axis, ymin=0, ymax=self.size)
        self.drawGridlines(delete=False)
        self._createArray()
    
    def mousePlotPosToXY(self, mouse_pos):
        """
        Returns a tuple `(x, y)` of the PLOT mouse position.
        """
        x = (int)(mouse_pos[0] / self.square)
        y = (int)(mouse_pos[1] / self.square) 
        return (x, y)
        
    # Drawing in the plot
    
    def drawAllSquares(self):
        """ 
        Delete all drawn items in the plot and then draw the `start`, `end` and each `obstacle` in the obstacles list.
        """
        dpg.delete_item(self.plot, children_only=True, slot=2)
        self.drawGridlines(delete=False)
        if self.start:
            self.start_drawing_alias = self.drawSquare(self.start, self.green, need_return=True)
        if self.end:
            self.end_drawing_alias = self.drawSquare(self.end, self.white, need_return=True)
    
    def drawWall(self, xy: tuple):
        self.drawSquare(xy, self.gray)
    
    def drawSquare(self, xy: tuple, colorRGB: list = [0, 0, 0], thick = 0, need_return: bool = False):
        x, y = xy
        x *= self.square
        y *= self.square
        square = dpg.draw_rectangle(parent=self.plot, pmin=[x, y], pmax=[x+self.square, y+self.square], color=(0, 0, 0, -255), fill=colorRGB, thickness=thick)
        if need_return:
            return square
        else:
            return None
        
    def drawText(self, text: str, xy: tuple, size: int = 5):
        dpg.draw_text(parent=self.plot, text=text, pos=xy, size=size)

    def drawGridlines(self, delete: bool=True):
        if delete:
            for gridline in self.gridlines:
                dpg.delete_item(gridline)
        self.gridlines.clear()
        
        new_gridlines = []
        for x in range(1, self.size):
            new_line = dpg.draw_line(parent=self.plot, p1=(x, 0), p2=(x, self.size), color=(169, 169, 169, 90), thickness=0)
            new_gridlines.append(new_line)
        for y in range(1, self.size):
            new_line = dpg.draw_line(parent=self.plot, p1=(0, y), p2=(self.size, y), color=(169, 169, 169, 90), thickness=0)
            new_gridlines.append(new_line)
        self.gridlines = new_gridlines
    
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
                dpg.add_theme_style(dpg.mvPlotStyleVar_MinorAlpha, 0.6, category=dpg.mvThemeCat_Plots)
        dpg.bind_item_theme(self.plot, plot_style)
