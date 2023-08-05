"""A module defining all objects used to visualise model result data extracts"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from abc import ABC, abstractmethod
from tfv.misc import get_date_time, Expression
from matplotlib.animation import FFMpegWriter
from matplotlib.colorbar import ColorbarBase
from matplotlib.text import Text
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
from matplotlib.quiver import Quiver
from matplotlib.tri import Triangulation, TriContourSet
from matplotlib.cbook import silent_list
from matplotlib._tri import TriContourGenerator
from matplotlib.collections import PolyCollection, TriMesh, PathCollection
# Non-essential imports
from matplotlib import cm
from matplotlib.dates import DateFormatter
from matplotlib.colors import Normalize, BoundaryNorm


mpl.use('Qt5Agg')
plt.interactive(True)

__axes__ = list()


# --------------------------------------------------- Interactive Objects ----------------------------------------------
class Slider:

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, values):
        self._values = np.array(values)
        self._index = np.argmin(np.abs(self.values - self.value))
        self._value = self.values[self.index]

        self.update()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.index = np.argmin(np.abs(self.values - value))

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        in_range = 0 <= index and index <= self.values.size - 1
        is_new = index != self.index
        if in_range and is_new:
            self._index = index
            self._value = self._values[index]

            self.update()

    def __init__(self, figure, values, callbacks=[], init_value=None, inc=1):
        self.figure = figure
        self._init_patches()
        self._init_events()

        self.inc = inc
        self._playing = False
        self._dragging = False

        self._index = None
        if init_value is None:
            self._value = values[0]
        else:
            self._value = init_value
        self.callbacks = callbacks
        self.values = values

        # Provide figure update method, depends on backend
        back_end = mpl.get_backend()
        if back_end == 'TkAgg':  # TkAgg
            self.fig_draw = self.figure.canvas.draw
        elif back_end == 'Qt5Agg':  # PyQt5
            self.fig_draw = self.figure.canvas.update

    def _init_patches(self):
        self.bbox = [0.02, 0.02, 0.3, 0.06]
        self.axes = self.figure.add_axes(self.bbox)
        self.axes.xaxis.set_visible(False)
        self.axes.yaxis.set_visible(False)
        self.axes.set_navigate(False)

        __axes__.append(self.axes)

        def make_rectangle(w, h):
            return np.array([[0, 0], [0, h], [w, h], [w, 0]]) - [w/2, h/2]

        def make_triangle(w, h, sign):
            return np.array( [[0, 0], [sign*w, h / 2], [0, h]]) - [sign*w/2, h/2]

        xy = make_rectangle(0.90, 0.10) + [0.50, 0.7]
        self.bar = Polygon(xy, edgecolor='black', facecolor='black')
        self.axes.add_patch(self.bar)

        xy = make_rectangle(0.025, 0.40) + [0.05, 0.7]
        self.ball = Polygon(xy, edgecolor='black', facecolor='white')
        self.axes.add_patch(self.ball)

        xy = make_triangle(0.05, 0.40, -1) + [0.40, 0.25]
        self.bwd = Polygon(xy, edgecolor='black', facecolor='green')
        self.axes.add_patch(self.bwd)

        xy = make_rectangle(0.05, 0.40) + [0.50, 0.25]
        self.stp = Polygon(xy, edgecolor='black', facecolor='red')
        self.axes.add_patch(self.stp)

        xy = make_triangle(0.05, 0.40, 1) + [0.60, 0.25]
        self.fwd = Polygon(xy, edgecolor='black', facecolor='green')
        self.axes.add_patch(self.fwd)

    def _init_events(self):
        callback_map = dict(button_press_event=self._on_press, motion_notify_event=self._on_motion,
                            button_release_event=self._on_release, key_press_event=self._on_key_press)
        self._cid = [self.figure.canvas.mpl_connect(event, callback) for event, callback in callback_map.items()]

    def _on_press(self, event):
        if event.inaxes != self.axes:
            return

        in_ball, _ = self.ball.contains(event)
        in_bar, _ = self.bar.contains(event)
        in_fwd, _ = self.fwd.contains(event)
        in_stop, _ = self.stp.contains(event)
        in_bwd, _ = self.bwd.contains(event)

        if in_ball:
            self._dragging = True
        elif in_bar:
            self.value = self._pos2val(event.xdata)
        elif in_fwd:
            self.play_fwd()
        elif in_bwd:
            self.play_bwd()
        elif in_stop:
            self.stop()

    def _on_motion(self, event):
        in_axes = event.inaxes == self.axes
        if not self._dragging or not in_axes:
            return
        self.value = self._pos2val(event.xdata)
        # self.figure.canvas.draw()

    def _on_release(self, event):
        self._dragging = False
        # self.figure.canvas.draw()

    def _on_key_press(self, event):
        if event.key == 'left':
            plt.ioff()
            self.prev()
            self.quick_draw()
            plt.ion()
        elif event.key == 'right':
            plt.interactive(False)
            self.next()
            self.quick_draw()
            plt.interactive(True)

    def _scale(self):
        return (self.values[-1] - self.values[0])/0.9

    def _x0(self):
        return self.bar.xy[0, 0]

    def _val2pos(self, value):
        return (value - self.values[0])/self._scale()+self._x0()

    def _pos2val(self, x):
        return (x-self._x0())*self._scale() + self.values[0]

    def subscribe(self, callback):
        self.callbacks.append(callback)
        self.update()

    def unsubscribe(self, callback):
        self.callbacks.remove(callback)

    def update(self):
        x = self._val2pos(self.value)
        dx = x - np.mean(self.ball.xy[:,0])
        self.ball.set_xy(self.ball.xy + [dx, 0])

        for callback in self.callbacks:
            callback(self.value)

    def next(self):
        self.index += self.inc

    def prev(self):
        self.index -= self.inc

    def play_fwd(self):
        self._playing = True
        plt.interactive(False)
        while self._playing:
            self.next()
            self.quick_draw()

    def play_bwd(self):
        self._playing = True
        plt.interactive(False)
        while self._playing:
            self.prev()
            self.quick_draw()

    def stop(self):
        self._playing = False
        plt.interactive(True)

    def quick_draw(self):
        for axes in __axes__:
            # Redraw the only items in frame
            axes.redraw_in_frame()

            # Draw x grid-lines
            x_grid = axes.get_xgridlines()
            for line in x_grid:
                axes.draw_artist(line)

            # Draw y grid-lines
            y_grid = axes.get_ygridlines()
            for line in y_grid:
                axes.draw_artist(line)

        # self.figure.canvas.update()
        self.fig_draw()
        self.figure.canvas.flush_events()


class _Cursor:
    """
    To be added to set of interactive objects
    """
    pass


class _Line:

    highlight = \
        {
            'marker': 'o',
            'markersize': '3',
            'markerfacecolor': 'r',

            'linestyle': '-',
            'linewidth': 1.2,
            'color': 'r'
        }

    @property
    def editing(self):
        return self._editing

    @property
    def adding(self):
        return self._adding

    @property
    def moving(self):
        return self._moving

    @property
    def index(self):
        return self._index

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        x = self.data[:, 0]
        y = self.data[:, 1]
        self.line.set_data((x, y))

    def __init__(self, *args, **kwargs):
        # Set default status attributes
        self._editing = False
        self._adding = False
        self._moving = False
        self._index = None

        # Set default data attribute
        self._data = np.array([[np.nan, np.nan]])

        # Set default line attribute
        self.line = plt.plot(np.nan, np.nan, **kwargs)[0]
        self.style = {key: plt.get(self.line, key) for key in self.highlight.keys()}
        self.line.set_pickradius(10)

        # Update data attribute based on input arguments
        if len(args) > 2:
            self.data = np.column_stack((args[0], args[1]))
        else:
            self._index = 0
            self._editing = True
            self._adding = True

        # Connect event handlers (call backs) to events
        self._cid_click = self.line.axes.figure.canvas.mpl_connect('button_press_event', self._on_click)
        self._cid_move = self.line.axes.figure.canvas.mpl_connect('motion_notify_event', self._on_hover)

    def __repr__(self):
        return repr(self.data)

    def _insert(self):
        # Insert vertex
        self.data = np.insert(self.data, self._index, [np.nan, np.nan], axis=0)

    def _delete(self):
        # Delete vertex
        self.data = np.delete(self.data, self._index, axis=0)

    def _on_click(self, event):
        if (event.inaxes is None) or (not self.editing):
            return

        if event.button.name == 'LEFT':
            # Left click to add\move
            if self.adding:
                # If adding, render current point
                self._index += 1
                self._insert()
            elif self.moving:
                # If moving, render current point
                self._moving = False
                self._index = None
            else:
                # Move node which was clicked
                hit, dic = self.line.contains(event)

                node = self.data[dic['ind']]
                pixel = self.line.axes.transData.transform(node)

                dx = event.x - pixel[0, 0]
                dy = event.y - pixel[0, 1]
                dist = (dx ** 2 + dy ** 2) ** 0.5

                if hit & (dist < self.line.get_pickradius()):
                    self._index = dic['ind']
                    self._moving = True

        elif event.button.name == 'RIGHT':
            # Right click to finish adding
            if self.adding:
                self._adding = False
                self._index = None

    def _on_hover(self, event):
        if (event.inaxes is None) or (not self.editing):
            return

        if self.editing:
            # Change line style
            if self.line.contains(event)[0]:
                plt.setp(self.line, **self.highlight)
            else:
                plt.setp(self.line, **self.style)

        if self.adding or self.moving:
            # Update current node position
            self._data[self.index, :] = np.array([event.xdata, event.ydata])
            self.line.set_data((self.data[:, 0], self.data[:, 1]))

    def toggle(self):
        self._editing = not self.editing

    def reset(self):
        self.data = np.array([[np.nan, np.nan]])
        self._editing = True
        self._adding = True


class Viewer:
    """
    Class to explore/view time varying model result data

    Parameters
    ----------
    size : tuple
        Size of underlying figure as (width, height) in specified units
    units : {'mm', 'cm' or 'm'}
        Figure units
    time_fmt : string
        Time format of title based on python datetime string formatting

    Attributes
    ----------
    figure : matplotlib.pyplot.Figure
        Underlying matplotlib figure object
    time_vector : np.ndarray
        Time vector associated with display
    time_current : np.float64
        Current time of display
    slider_bar: tfv.visual.Slider
        Slider widget for updating display
    title_axes : matplotlib.pyplot.Axes
        Axes which contains time title
    title : matplotlib.text.Text
        Text object of time title
    """

    __register__ = list()

    @property
    def time_current(self):
        return self.slider_bar.value

    @time_current.setter
    def time_current(self, time_current):
        self.slider_bar.value = time_current

    @property
    def time_vector(self):
        return self.slider_bar.values

    @time_vector.setter
    def time_vector(self, time_vector):
        if np.all(self.time_vector == np.arange(100)):
            self.slider_bar.values = time_vector
        else:
            t1 = np.hstack((self.time_vector, time_vector)).min()
            t2 = np.hstack((self.time_vector, time_vector)).max()
            dt = np.min((np.mean(np.diff(self.time_vector)), np.mean(np.diff(time_vector))))
            self.slider_bar.values = np.arange(t1, t2, dt)

    def __init__(self, size=(240, 120), units='mm', time_fmt='%d/%m/%Y %H:%M:%S'):
        """Initializes Viewer object with figure size, figure units & title time format"""

        self.size = size
        self.units = units
        self.time_fmt = time_fmt

        self.__prep_figure__()
        self.__prep_slider__()
        self.__prep_title__()

        self.__register__.append(self)

    def __prep_figure__(self):
        """Prepares underlying figure"""

        sf_map = {'mm': 12 / 300, 'cm': 12 / 30, 'm': 12 / 0.3}

        sf = sf_map[self.units]
        w = self.size[0]*sf
        h = self.size[1]*sf

        self.figure = plt.figure(figsize=(w, h))

    def __prep_slider__(self):
        """Initializes the Slider object"""

        self.slider_bar = Slider(self.figure, np.arange(100), callbacks=[])

    def __prep_title__(self):
        rec = [0.30, 0.96, 0.40, 0.04]
        self.title_axes = self.figure.add_axes(rec)
        self.title_axes.xaxis.set_visible(False)
        self.title_axes.yaxis.set_visible(False)
        self.title_axes.set_navigate(False)

        for spine in self.title_axes.spines.values():
            spine.set_color('white')

        self.title_axes.set_xlim(0, 2)
        self.title_axes.set_ylim(0, 2)
        __axes__.append(self.title_axes)

        self.title = Text(1, 1, '', fontsize=12, horizontalalignment='center', verticalalignment='center')
        self.title_axes._add_text(self.title)

        if self.time_fmt is not None:
            self.slider_bar.subscribe(self.__set_title_time__)

    def __set_title_time__(self, time_stamp):
        date_time = get_date_time(time_stamp)
        string = date_time[0].strftime(self.time_fmt)
        self.title.set_text(string)

    def subscribe(self, callback):
        """Subscribes callback to slider"""
        self.slider_bar.subscribe(callback)

    def unsubscribe(self, callback):
        """Removes callback subscription"""
        self.slider_bar.unsubscribe(callback)

    def print(self, file_path, fmt='png', dpi=300):
        """
        Prints Viewer objects figure to image file.

        Parameters
        ---------
        file_path : string
            File path to output image file
        fmt : string
            File format i.e 'png', 'pdf', 'jpg'
        dpi : integer
            Resolution in dots per inch (dpi)
        """

        self.slider_bar.axes.set_visible(False)
        self.figure.savefig(file_path, format=fmt, dpi=dpi)
        self.slider_bar.axes.set_visible(True)

    def animate(self, file_path, ts, te, dt,  fps=10, dpi=150):
        """
        Writes animation file for specified time interval.

        Parameters
        ----------
        file_path : string
            File path to output animation
        ts : float
            Start time as python time stamp
        te : float
            End time as python time stamp
        dt : float
            Time increment at which to save frame

        Other Parameters
        ----------------
        fps : integer
            Frames per second
        dpi : integer
            Resolution in dots per inch (dpi)
        """

        # Hide slider bar
        self.slider_bar.axes.set_visible(False)

        # Loop through time
        nt = int((te - ts) / dt)+1
        writer = FFMpegWriter(fps=fps)
        with writer.saving(self.figure, file_path, dpi):
            for ii in range(nt):
                self.time_current = (ts + ii*dt)
                writer.grab_frame()

        # Show slider bar
        self.slider_bar.axes.set_visible(True)


class ColourBar(ColorbarBase):

    def __init__(self, patch, location='bottom', offset=0.075, thickness=0.010, label=''):
        # Get target axes handle
        if type(patch).__name__ == 'TriContourSet':
            target = patch.ax
        else:
            target = patch.axes

        if offset > 0:
            offset_1 = offset
            offset_2 = 0
        else:
            offset_1 = 0
            offset_2 = offset

        # Determine rectangles for target axes & colour bar axes
        rec = target.get_position().extents
        if location == 'bottom':
            rec1 = [rec[0], rec[1] + offset_1, rec[2] - rec[0], rec[3] - rec[1] - offset_1]
            rec2 = [rec[0], rec[1] + offset_2, rec[2] - rec[0], thickness]
        elif location == 'top':
            rec1 = [rec[0], rec[1], rec[2] - rec[0], rec[3] - rec[1] - offset_1]
            rec2 = [rec[0], rec[3] - offset_2, rec[2] - rec[0], thickness]
        elif location == 'left':
            rec1 = [rec[0] + offset_1, rec[1], rec[2] - rec[0] - offset_1, rec[3] - rec[1]]
            rec2 = [rec[0] + offset_2, rec[1], thickness, rec[3] - rec[1]]
        elif location == 'right':
            rec1 = [rec[0], rec[1], rec[2] - rec[0] - offset_1, rec[3] - rec[1]]
            rec2 = [rec[2] - offset_2, rec[1], thickness, rec[3] - rec[1]]

        target.set_position(rec1)
        axes = target.figure.add_axes(rec2)

        # Set orientation
        if location == 'bottom' or location == 'top':
            orientation = 'horizontal'
        elif location == 'left' or location == 'right':
            orientation = 'vertical'

        # Initialize ColorbarBase
        super(ColourBar, self).__init__(axes, patch.cmap, patch.norm, orientation=orientation)

        # Finish formatting
        if orientation == 'horizontal':
            axes.xaxis.set_ticks_position(location)
            axes.xaxis.set_label_position(location)
            axes.set_xlabel(label)
        elif orientation == 'vertical':
            axes.yaxis.set_ticks_position(location)
            axes.yaxis.set_label_position(location)
            axes.set_ylabel(label)


# --------------------------------------------------- Visual Objects ---------------------------------------------------
class Visual(ABC):
    """
    An abstract base class for an object which visualizes a variable. The main purpose of a Visual sub-class is to
    initialize and store a plotting library specific graphics object for a given extract type i.e SheetPatch.

    The Visual object works by subscribing its set_time_current method to the Slider object. When self.set_time_current
    is called by the Slider, the Visual object selects a valid time based on the Extractor objects time_vector and updates itself.
    """

    @property
    def time_vector(self):
        return self.extractor.time_vector

    def __init__(self, axes, extractor, expression, **kwargs):
        # Set target axes
        self.axes = axes
        __axes__.append(self.axes)

        # Set extractor
        self.extractor = extractor
        self._time_current = self.time_vector[0]
        self._time_index = 0

        # Set expression
        if type(expression) is str:
            self.expression = Expression(expression)
        elif type(expression) is list:
            self.expression = [Expression(exp) for exp in expression]
        else:
            self.expression = None

        # Connect with viewer
        viewer = kwargs.pop('viewer', None)
        if viewer is None:
            viewer = Viewer.__register__[0]
        self.viewer = viewer
        self.viewer.time_vector = self.time_vector
        self.viewer.subscribe(self.set_time_current)

        # Initialize the graphics object
        self.__prep_graphics_obj__(**kwargs)

        # Zoom to the graphics object
        self.zoom()

    def get_time_current(self):
        return self._time_current

    def set_time_current(self, time):
        ii = np.argmin(np.abs(self.time_vector - time))

        if ii != self._time_index:
            self._time_index = ii
            self._time_current = self.time_vector[ii]
            self.__dynamic_update__()

    @abstractmethod
    def __get_data__(self):
        """Abstract method which returns object data based on the expression"""

    @abstractmethod
    def __prep_graphics_obj__(self, **kwargs):
        """Abstract method to initialize the graphics object which will be used to visualize the result"""

    @abstractmethod
    def __static_update__(self):
        """Abstract method which updates static components of graphics object"""

    @abstractmethod
    def __dynamic_update__(self):
        """Abstract method which updates dynamic components graphics object"""

    @abstractmethod
    def zoom(self):
        """Abstract method which zooms axis to extent of graphics object"""


class SheetPatch(Visual):
    """
    Class for dynamic visualization of model result sheet extracts as collection of patches


    Parameters
    ----------
    axes : matplotlib.pyplot.Axes
        Axes object to display/render the graphics object
    extractor : tfv.extractor.Extractor
        Extractor object which is extracting data
    expression : string
        Expression that defines a variable
    datum : {'sigma', 'depth', 'height', 'elevation'}
        Vertical depth-averaging datum i.e sigma, depth, height, elevation, top, bottom.
    limits : tuple
        Vertical depth-averaging limits (z1, z2) relative to vertical datum.


    Other Parameters
    ----------------
    shading : {'flat', 'interp'}
        Sets the shading to be flat or interpolated (gourad)
    zorder : integer
        Layer order in which graphics object will be rendered (0 is bottom/first)
    cmap : matplotlib.colors.LinearSegmentedColormap
        Colormap object for mapping normalized data (0 - 1) to rgb colors
    norm : matplotlib.colors.BoundaryNorm
        Normalization object for normalizing raw data to (0 - 1) based on (min, max)
    clim : tuple
        Colour limits of the underlying matplotlib.collections.PatchCollection object (min, max)
    edgecolor : string
        Sets the mesh edge colouring of the underlying matplotlib.collections object
    antialiased : bool
        Sets the antialiasing state for rendering the underlying matplotlib.collections object
    alpha : float
        Sets the transparencies of the underlying matplotlib.collections object

    """

    def __init__(self, axes, extractor, expression, datum='sigma', limits=(0, 1), **kwargs):
        self.datum = datum
        self.limits = limits

        # Call initialize method of super class
        super(SheetPatch, self).__init__(axes, extractor, expression, **kwargs)

    def __get_data__(self):
        args = (self.expression, self._time_index, self.datum, self.limits)
        if self.shading is 'flat':
            return self.extractor.get_sheet_cell(*args)
        elif self.shading is 'interp':
            return self.extractor.get_sheet_node(*args)

    def __prep_graphics_obj__(self, **kwargs):
        # Pop key word arguments which are not used by the graphics object
        self.shading = kwargs.pop('shading', 'flat')

        # Get handles on sheet geometry
        node_x = self.extractor.node_x
        node_y = self.extractor.node_y
        cell_node = self.extractor.cell_node
        tri_cell_node = self.extractor.tri_cell_node

        # Instantiate graphics object based on shading type
        data = self.__get_data__()
        if self.shading is 'flat':
            xy = np.dstack((node_x[cell_node], node_y[cell_node]))
            self.patch = PolyCollection(xy, array=data, **kwargs)
        elif self.shading is 'interp':
            self.tri = Triangulation(node_x, node_y, triangles=tri_cell_node)
            self.patch = TriMesh(self.tri, array=data, antialiased=True, **kwargs)

            # Mask invalid triangles
            mask = np.any(data.mask[self.extractor.tri_cell_node], axis=1)
            self.tri.set_mask(mask)

        # Add the graphics object to axes
        self.axes.add_collection(self.patch)

    def __static_update__(self):
        pass

    def __dynamic_update__(self):
        data = self.__get_data__()
        self.patch.set_array(data)

        # Mask invalid triangles
        if self.shading is 'interp':
            mask = np.any(data.mask[self.extractor.tri_cell_node], axis=1)
            self.tri.set_mask(mask)

    def zoom(self):
        self.axes.set_xlim([np.min(self.extractor.node_x), np.max(self.extractor.node_x)])
        self.axes.set_ylim([np.min(self.extractor.node_y), np.max(self.extractor.node_y)])


class SheetContour(Visual):
    """
    Class for dynamic visualization of model result sheet extracts as contours

    Parameters
    ----------
    axes : matplotlib.pyplot.Axes
        Axes object to display/render the graphics object
    extractor : tfv.extractor.Extractor
        Extractor object which is extracting data
    expression : string
        Expression that defines a variable
    datum : {'sigma', 'depth', 'height', 'elevation'}
        Vertical depth-averaging datum i.e sigma, depth, height, elevation, top, bottom.
    limits : tuple
        Vertical depth-averaging limits (z1, z2) relative to vertical datum.

    Other Parameters
    ----------------
    zorder : integer
        Layer order in which graphics object will be rendered (0 is bottom/first)
    cmap : matplotlib.colors.LinearSegmentedColormap
        Colormap object for mapping normalized data (0 - 1) to rgb colors
    norm : matplotlib.colors.BoundaryNorm
        Normalization object for normalizing raw data to (0 - 1) based on (min, max)
    clim : tuple
        Colour limits of the underlying matplotlib.collections.PatchCollection object (min, max)
    edgecolor : string
        Sets the mesh edge colouring of the underlying matplotlib.collections object
    antialiased : bool
        Sets the antialiasing state for rendering the underlying matplotlib.collections object
    alpha : float
        Sets the transparencies of the underlying matplotlib.collections object
    """

    def __init__(self, axes, extractor, expression, datum='sigma', limits=(0, 1), **kwargs):
        self.datum = datum
        self.limits = limits

        # Call initialize method of super class
        super(SheetContour, self).__init__(axes, extractor, expression, **kwargs)

    def __get_data__(self):
        args = (self.expression, self._time_index, self.datum, self.limits)
        return self.extractor.get_sheet_node(*args)

    def __prep_graphics_obj__(self, **kwargs):
        # Get handles on sheet geometry
        node_x = self.extractor.node_x
        node_y = self.extractor.node_y
        tri_cell_node = self.extractor.tri_cell_node

        # Get triangular mesh and initialize cpp triangulation
        tri = Triangulation(node_x, node_y, triangles=tri_cell_node)
        self.cpp_tri = tri.get_cpp_triangulation()

        # Get data
        data = self.__get_data__()

        # Mask bad triangles
        mask = np.any(data.mask[self.extractor.tri_cell_node], axis=1)
        self.cpp_tri.set_mask(mask)

        # Set contour limits/levels
        zlim = [data.min(), data.max()]

        clim = kwargs.pop('clim', [zlim[0], zlim[1]])
        self.levels = kwargs.pop('levels', 50)

        if type(self.levels) is int:
            levels = np.linspace(clim[0], clim[1], self.levels)
        else:
            levels = self.levels

        self.cont = TriContourSet(self.axes, tri, data.data, levels, filled=True, extend='both', **kwargs)

        if clim is not None:
            self.cont.set_clim(clim)

    def __static_update__(self):
        pass

    def __dynamic_update__(self):
        # Get data
        data = self.__get_data__()

        # Mask bad triangles
        mask = np.any(data.mask[self.extractor.tri_cell_node], axis=1)
        self.cpp_tri.set_mask(mask)

        # Set contour limits/levels
        zlim = [data.min(), data.max()]
        clim = self.cont.get_clim()

        if type(self.levels) is int:
            levels = np.linspace(clim[0], clim[1], self.levels)
        else:
            levels = self.levels

        # self._contour_args(self, args, kwargs)
        self.cont.zmin = zlim[0]
        self.cont.zmax = zlim[1]

        # self._contour_level_args
        self.cont.levels = levels

        # self.__init__
        self.cont._process_levels()

        # Update cpp generator
        self.cont.cppContourGenerator = TriContourGenerator(self.cpp_tri, data)

        # Update Paths
        lowers, uppers = self.cont._get_lowers_and_uppers()
        segs, kinds = self.cont._get_allsegs_and_allkinds()

        zorder = self.cont.collections[0].zorder
        for collection in self.cont.collections:
            self.cont.ax.collections.remove(collection)
        self.cont.collections = silent_list('PathCollection')

        for level, level_upper, segs, kinds in \
                zip(lowers, uppers, segs, kinds):
            paths = self.cont._make_paths(segs, kinds)

            col = \
                PathCollection(
                    paths,
                    antialiaseds=(self.cont.antialiased,),
                    edgecolors=None,
                    alpha=self.cont.alpha,
                    transform=self.cont.get_transform(),
                    zorder=zorder
                )

            self.cont.ax.add_collection(col, autolim=False)
            self.cont.collections.append(col)
        self.cont.changed()

    def zoom(self):
        self.axes.set_xlim([np.min(self.extractor.node_x), np.max(self.extractor.node_x)])
        self.axes.set_ylim([np.min(self.extractor.node_y), np.max(self.extractor.node_y)])


class SheetVector(Visual):
    """
    Class for dynamic visualization of model result sheet extracts as gridded vector field

    Parameters
    ----------
    axes : matplotlib.pyplot.Axes
        Axes object to display/render the graphics object
    extractor : tfv.extractor.Extractor
        Extractor object which is extracting data
    expression : tuple
        Tuple of string expressions that defines vector (vec_x, vec_y)
    datum : {'sigma', 'depth', 'height', 'elevation'}
        Vertical depth-averaging datum i.e sigma, depth, height, elevation, top, bottom.
    limits : tuple
        Vertical depth-averaging limits (z1, z2) relative to vertical datum.
    """

    def __init__(self, axes, extractor, expression, datum, limits, **kwargs):
        self.datum = datum
        self.limits = limits

        self.xg = None
        self.yg = None
        self.grid_index = None

        # Call initialize method of super class
        super(SheetVector, self).__init__(axes, extractor, expression, **kwargs)

    def __get_data__(self):
        args = (self._time_index, self.xg, self.yg, self.datum, self.limits)
        u = self.extractor.get_sheet_grid(self.expression[0], *args, grid_index=self.grid_index)
        v = self.extractor.get_sheet_grid(self.expression[1], *args, grid_index=self.grid_index)

        return u, v

    def __prep_graphics_obj__(self, **kwargs):
        # Pop key word arguments which are not used by the graphics object
        self.resolution = kwargs.pop('resolution', 40)

        # Instantiate graphics object with no data, data will be added on draw event automatically
        self.quiver = Quiver(self.axes, np.mean(self.extractor.node_x), np.mean(self.extractor.node_y), 0, 0, **kwargs)

        # Add the graphics object to axes
        self.axes.add_collection(self.quiver)

        # Connect the regrid method to the draw event of the figure object.
        self._x_cid = self.axes.callbacks.connect('xlim_changed', self.__static_update__)
        self._y_cid = self.axes.callbacks.connect('ylim_changed', self.__static_update__)

    def __static_update__(self, event=None):
        xlim = self.axes.get_xlim()
        ylim = self.axes.get_ylim()

        self.xg = np.linspace(xlim[0], xlim[1], self.resolution)
        self.yg = np.linspace(ylim[0], ylim[1], self.resolution)
        self.grid_index = self.extractor.get_grid_index(self.xg, self.yg)

        u, v = self.__get_data__()

        x, y = [arr.flatten() for arr in np.meshgrid(self.xg, self.yg)]
        xy = np.hstack((x[:, np.newaxis], y[:, np.newaxis]))

        self.quiver.set_offsets(xy)
        self.quiver.set_UVC(u, v)

    def __dynamic_update__(self):
        u, v = self.__get_data__()
        self.quiver.set_UVC(u, v)

    def zoom(self):
        self.axes.set_xlim([np.min(self.extractor.node_x), np.max(self.extractor.node_x)])
        self.axes.set_ylim([np.min(self.extractor.node_y), np.max(self.extractor.node_y)])


class CurtainPatch(Visual):
    """
    Class for dynamic visualization of model result curtain extracts as collection of patches.

    Arguments
    ---------
    :param axes -- object | Axes object.
    :param extractor -- object | Extractor object.
    :param expression -- string | String expression that defines variable.
    :param polyline -- 2D array | Polyline as [x, y] used to slice 3D data.

    Returns
    -------
    :param curtain -- object | CurtainPatch instance.

    Examples
    --------
    >> xtr = FvExtractor('my_file_3D.nc')
    >> curtain = SheetContour(axes, xtr, polyline, 'SAL')
    """

    def __init__(self, axes, extractor, expression, polyline, **kwargs):
        self.polyline = polyline
        self.x_data = extractor.get_intersection_data(polyline)
        self.index = extractor.get_curtain_cell_index(polyline)

        # Call initialize method of super class
        super(CurtainPatch, self).__init__(axes, extractor, expression, **kwargs)

    def __get_data__(self):
        self.geo = self.extractor.get_curtain_cell_geo(self._time_index, self.polyline, self.x_data, self.index)

        args = (self.expression, self._time_index, self.polyline, self.x_data, self.index)
        return self.extractor.get_curtain_cell(*args)

    def __prep_graphics_obj__(self, **kwargs):
        data = self.__get_data__()
        node_x, node_y, cell_node = self.geo

        xy = np.dstack((node_x[cell_node], node_y[cell_node]))
        self.patch = PolyCollection(xy, array=data, **kwargs)

        # Add the graphics object to axes
        self.axes.add_collection(self.patch)

    def __static_update__(self):
        pass

    def __dynamic_update__(self):
        data = self.__get_data__()
        node_x, node_y, cell_node = self.geo

        xy = np.dstack((node_x[cell_node], node_y[cell_node]))

        self.patch.set_verts(xy)
        self.patch.set_array(data)

    def zoom(self):
        self.axes.set_xlim([np.min(self.geo[0]), np.max(self.geo[0])])
        self.axes.set_ylim([np.min(self.geo[1]), np.max(self.geo[1])])


class CurtainVector(Visual):
    """
    Class for dynamic visualization of model result curtain extracts as gridded vector field

    Arguments
    ---------
    :param axes -- object | Axes object.
    :param extractor -- object | Extractor object.
    :param expression -- string | String expression that defines variable.
    :param polyline -- 2D array | Polyline as [x, y] used to slice 3D data.

    Returns
    -------
    :param curtain -- object | CurtainPatch instance.

    Examples
    --------
    >> xtr = FvExtractor('my_file_3D.nc')
    >> curtain = SheetContour(axes, xtr, polyline, ['hyp(V_x, V_y)', 'W'])
    """

    def __init__(self, axes, extractor, expression, polyline, **kwargs):
        self.polyline = polyline
        self.x_data = extractor.get_intersection_data(polyline)
        self.index = extractor.get_curtain_cell_index(polyline)

        self.xg = np.array([0, 1])
        self.yg = np.array([0, 1])

        # Call initialize method of super class
        super(CurtainVector, self).__init__(axes, extractor, expression, **kwargs)

    def __get_data__(self):
        self.geo = self.extractor.get_curtain_cell_geo(self._time_index, self.polyline, self.x_data, self.index)

        args = (self._time_index, self.polyline, self.xg, self.yg, self.x_data, self.index)
        u = self.extractor.get_curtain_grid(self.expression[0], *args)
        v = self.extractor.get_curtain_grid(self.expression[1], *args)

        return u, v

    def __prep_graphics_obj__(self, **kwargs):
        # Pop key word arguments which are not used by the graphics object
        self.resolution = kwargs.pop('resolution', 40)

        # Update geometry
        self.__get_data__()

        # Instantiate graphics object with no data, data will be added on draw event automatically
        self.quiver = Quiver(self.axes, np.mean(self.geo[0]), np.mean(self.geo[1]), 0, 0, **kwargs)

        # Add the graphics object to axes
        self.axes.add_collection(self.quiver)

        # Connect the regrid method to the draw event of the figure object.
        self._cid = self.axes.figure.canvas.mpl_connect('draw_event', lambda event: self.__dynamic_update__())

    def __static_update__(self):
        pass

    def __dynamic_update__(self):
        xlim = self.axes.get_xlim()
        ylim = self.axes.get_ylim()

        self.xg = np.linspace(xlim[0], xlim[1], self.resolution)
        self.yg = np.linspace(ylim[0], ylim[1], self.resolution)

        u, v = self.__get_data__()

        x, y = [arr.flatten() for arr in np.meshgrid(self.xg, self.yg)]
        xy = np.hstack((x[:, np.newaxis], y[:, np.newaxis]))

        self.quiver.set_offsets(xy)
        self.quiver.set_UVC(u, v)

    def zoom(self):
        self.axes.set_xlim([np.min(self.geo[0]), np.max(self.geo[0])])
        self.axes.set_ylim([np.min(self.geo[1]), np.max(self.geo[1])])


class ProfileCell(Visual):
    """
    Class for dynamic visualization of model result profile extracts as vertical line

    Arguments
    ---------
    :param axes -- object | Axes object.
    :param extractor -- object | Extractor object.
    :param expression -- string | String expression that defines variable.
    :param point -- tuple | Point (x, y) of profile location.

    Returns
    -------
    :param profile -- object | ProfileCell instance.

    Examples
    --------
    >> xtr = FvExtractor('my_file_3D.nc')
    >> profile = ProfileCell(axes, xtr, point, 'SAL')
    """

    def __init__(self, axes, extractor, expression, point, **kwargs):
        self.point = point

        super(ProfileCell, self).__init__(axes, extractor, expression, **kwargs)

    def __get_data__(self):
        self.elevation = self.extractor.get_profile_cell_geo(self._time_index, self.point)

        args = (self.expression, self._time_index, self.point)
        return self.extractor.get_profile_cell(*args)

    def __prep_graphics_obj__(self, **kwargs):
        data = self.__get_data__()
        self.line = Line2D(data, self.elevation, **kwargs)

        self.axes.add_line(self.line)

    def __static_update__(self):
        pass

    def __dynamic_update__(self):
        data = self.__get_data__()
        self.line.set_data(data, self.elevation)

    def zoom(self):
        data = self.__get_data__()
        if data.min() != 0 and data.max() != 0:
            self.axes.set_xlim([data.min()*0.95, data.max()*1.05])
        self.axes.set_ylim([self.elevation.min()*0.95, self.elevation.max()*1.05])


class SeriesGlider(Visual):
    """
    Class for dynamic visualization of model result time series extracts with current time marked

    Arguments
    ---------
    :param axes -- object | Axes object.
    :param extractor -- object | Extractor object.
    :param expression -- string | String expression that defines variable.
    :param location -- tuple | Point (x, y) of profile location.

    Keyword Arguments
    -----------------
    :param datum -- string | Vertical depth-averaging datum i.e sigma, depth, height, elevation, top, bottom.
    :param limits -- tuple | Vertical depth-averaging limits relative to vertical datum.

    Returns
    -------
    :param profile -- object | ProfileCell instance.

    Examples
    --------
    >> xtr = FvExtractor('my_file_3D.nc')
    >> profile = ProfileCell(axes, xtr, point, 'SAL')
    """

    def __init__(self, axes, extractor, expression, location, datum='sigma', limits=(0, 1), **kwargs):
        self.location = location
        self.datum = datum
        self.limits = limits

        super(SeriesGlider, self).__init__(axes, extractor, expression, **kwargs)

    def __get_data__(self):
        args = (self.expression, self.location, self.datum, self.limits)
        return self.extractor.get_data(*args)

    def __prep_graphics_obj__(self, **kwargs):
        self.date_fmt = kwargs.pop('date_fmt', '%d/%m/%Y')

        x = self.extractor.time_vector
        x = get_date_time(x)
        y = self.__get_data__()

        self.time_series = Line2D(x, y, **kwargs)
        self.axes.add_line(self.time_series)

        glider_spec = dict(linewidth=0.8, linestyle='--', color='black')
        self.glider = Line2D([x[0], x[0]], [-10**20, 10**20], **glider_spec)
        self.axes.add_line(self.glider)

    def __static_update__(self):
        pass

    def __dynamic_update__(self):
        tc = self.get_time_current()
        x = np.array([tc, tc])
        x = get_date_time(x)
        self.glider.set_xdata(x)

    def zoom(self):
        x, y = self.time_series.get_data()
        xlim = [x.min(), x.max()]
        ylim = [y.min(), y.max()]
        self.axes.set_xlim(xlim)
        self.axes.set_ylim(ylim)


class HovmollerGlider(Visual):

    def __init__(self, axes, extractor, expression, location, **kwargs):
        self.location = location

        super(HovmollerGlider, self).__init__(axes, extractor, expression, **kwargs)

    def __get_data__(self):
        args = (self.expression, self.location)
        return self.extractor.get_raw_data(*args).ravel('F')

    def __prep_graphics_obj__(self, **kwargs):
        self.mesh = self.extractor.get_geometry(self.location)
        self.mesh.node_x = get_date_time(self.mesh.node_x)
        self.mesh.node_x = mdates.date2num(self.mesh.node_x)

        node_x = self.mesh.node_x[self.mesh.cell_node]
        node_y = self.mesh.node_y[self.mesh.cell_node]
        verts = np.dstack((node_x, node_y))

        self.patch = PolyCollection(verts, array=self.__get_data__(), **kwargs)
        self.axes.add_collection(self.patch)

        glider_spec = dict(linewidth=0.8, linestyle='--', color='black')
        self.glider = Line2D(self.time_vector[[0, 0]], [-10 ** 20, 10 ** 20], **glider_spec)
        self.axes.add_line(self.glider)

    def __static_update__(self):
        pass

    def __dynamic_update__(self):
        tc = self.get_time_current()
        x = np.array([tc, tc])
        x = get_date_time(x)
        self.glider.set_xdata(x)

    def zoom(self):
        xlim = [self.mesh.node_x.min(), self.mesh.node_x.max()]
        ylim = [self.mesh.node_y.min(), self.mesh.node_y.max()]
        self.axes.set_xlim(xlim)
        self.axes.set_ylim(ylim)


# --------------------------------------------- Particle Tracking Objects ----------------------------------------------
class ParticlesScatter(Visual):
    """
    Class for dynamic visualization of particle tracking model results as collection of patches

    Parameters
    ----------
    axes : matplotlib.pyplot.Axes
        Axes object to display/render the graphics object
    extractor : tfv.particles.FvParticles
        Extractor object which is extracting data
    expression : string
        Expression used to color the particles
    datum : {'sigma', 'depth', 'height', 'elevation'}
        Vertical datum applied for particle selection
    limits : tuple
        Vertical limits (z1, z2) applied for particle selection.
    show : string
        Expression used to select particles for display (works on top of vertical selection)
    highlight : string
        Expression used to highlight particles
    scale : float
        Number used to scale marker size (this is in map units i.e metres or degrees)
    shape : {'tri','square','o','star','diamond'}
        Shape of marker

    Other Parameters
    ----------------
    zorder : integer
        Layer order in which graphics object will be rendered (0 is bottom/first)
    cmap : matplotlib.colors.LinearSegmentedColormap
        Colormap object for mapping normalized data (0 - 1) to rgb colors
    norm : matplotlib.colors.BoundaryNorm
        Normalization object for normalizing raw data to (0 - 1) based on (min, max)
    clim : tuple
        Colour limits of the underlying matplotlib.collections.PatchCollection object (min, max)
    edgecolor : string
        Sets the edge colouring of the underlying matplotlib.collections object
    facecolor : string
        Sets the face colouring of the underlying matplotlib.collections object
    antialiased : bool
        Sets the antialiasing state for rendering the underlying matplotlib.collections object
    alpha : float
        Sets the transparencies of the underlying matplotlib.collections object
    """

    def __init__(self, axes, extractor, expression=None, datum=None, limits=None, show=None,
                 highlight=None, track=0, scale=0.001, shape='tri', **kwargs):

        self.datum = datum
        self.limits = limits
        self.track = track
        self.scale = scale
        self.shape = shape

        if show is not None:
            self.show = Expression(show)
        else:
            self.show = show
        if highlight is not None:
            self.highlight = Expression(highlight)
        else:
            self.highlight = highlight

        # Call initialize method of super class
        super(ParticlesScatter, self).__init__(axes, extractor, expression, **kwargs)

    def __get_data__(self):
        return self.extractor.get_raw_data(self.expression, self._time_index)

    def __prep_graphics_obj__(self, **kwargs):
        # Initialize dimensionless shape
        pi = np.pi
        n = None
        r = pi/2

        shape = self.shape.lower()
        if shape in ['triangle', 'tri']:
            n = 3
        elif shape == 'square':
            n = 4
        elif shape in ['circle', 'o']:
            n = 50
        elif shape in ['diamond', 'd']:
            n = 4
            r = 0
        elif shape == 'star':
            rad = np.linspace(0, 2 * pi, 6) - pi / 5 - r
            rad = rad[1, 3, 5, 2, 4, 1]
            self.shape_x = np.cos(rad)
            self.shape_y = np.sin(rad)
        else:
            pass

        if n is not None:
            rad = np.linspace(0, 2 * pi, n + 1) - pi / n - r
            self.shape_x = np.cos(rad)
            self.shape_y = np.sin(rad)

        node_x = 0 + self.scale*self.shape_x
        node_y = 0 + self.scale*self.shape_y

        xy = np.dstack((node_x, node_y))
        self.patch = PolyCollection(xy, **kwargs)

        # Add the graphics object to axes
        self.axes.add_collection(self.patch)

    def __static_update__(self):
        pass

    def __dynamic_update__(self):
        # Get logical index of particles to show based on self.show expression
        if self.show is None:
            show_lgi = np.ones((self.extractor.np,), dtype=np.bool)
        else:
            show_lgi = self.extractor.get_raw_data(self.show, self._time_index)

        # Apply additional elevation & inactivity filters
        if self.datum is None and self.limits is None:
            # Get valid particles based on mask only
            valid_lgi = np.invert(self.extractor.get_mask_vector(self._time_index))
        else:
            # Get valid particles based elevation filter (mask applied in get_vertical selection)
            valid_lgi = self.extractor.get_vertical_selection(self._time_index, self.datum, self.limits)

        # Update the 'show' logical index
        show_lgi = (show_lgi & valid_lgi)

        # Count number to show
        ns = np.sum(show_lgi)

        # Plot the particles
        if ns != 0:
            # Get logical index of particles to highlight
            if self.highlight is None:
                # Default to highlighting none of the shown particles
                highlight_lgi = np.zeros((ns,), dtype=np.bool)
            else:
                # Get highlight logical index (sub setting with the 'show' lgi)
                highlight_lgi = self.extractor.get_raw_data(self.highlight, self._time_index)[show_lgi]
            highlight_lgi[0] = False  # Stops from highlighting all particles (bug)
            nh = np.sum(highlight_lgi)  # Count number to highlight

            # Update patch faces (sub setting with the 'show' lgi)
            x = self.extractor.get_raw_data('x', self._time_index)[show_lgi]
            y = self.extractor.get_raw_data('y', self._time_index)[show_lgi]

            node_x = x.reshape(x.size, 1) + self.scale*self.shape_x
            node_y = y.reshape(y.size, 1) + self.scale*self.shape_y

            xy = np.dstack((node_x, node_y))
            self.patch.set_verts(xy)

            # Update colours
            if self.expression is None:
                # Get face colours
                c = self.patch.get_facecolor()[0]
                face_colours = np.tile(c, (ns, 1))

                # Finish highlighting with yellow
                y = np.array([255, 255, 0., 255.]) / 255
                face_colours[highlight_lgi, :] = np.tile(y, (nh, 1))

                # Set face colours
                self.patch.set_facecolor(face_colours)

                # Get edge colours & set edge colors
                c = self.patch.get_edgecolor()
                if c.size > 0:
                    # Set edge colours
                    edge_colours = np.tile(c[0], (ns, 1))
                    self.patch.set_edgecolor(edge_colours)
            else:
                # Get data relating to self.expression (sub setting with the 'show' lgi)
                data = self.extractor.get_raw_data(self.expression, self._time_index)[show_lgi]

                # Get face colours
                norm = self.patch.norm(data)
                face_colours = self.patch.cmap(norm)

                # Finish highlighting
                y = np.array([255, 255, 0., 255]) / 255
                face_colours[highlight_lgi, :] = np.tile(y, (nh, 1))

                # Set face colours
                self.patch.set_facecolor(face_colours)

                # Get & set edge colours
                c = self.patch.get_edgecolor()
                if c.size > 0:
                    # Set edge colours
                    edge_colours = np.tile(c[0], (ns, 1))
                    self.patch.set_edgecolor(edge_colours)
        else:
            node_x = np.nan + self.scale * self.shape_x
            node_y = np.nan + self.scale * self.shape_y

            xy = np.dstack((node_x, node_y))
            self.patch.set_verts(xy)

    def zoom(self):
        pass


class ParticlesHeat(Visual):

    def __init__(self, axes, extractor, expression, datum='sigma', limits=(0, 1), **kwargs):
        self.datum = datum
        self.limits = limits

        # Call initialize method of super class
        super(ParticlesHeat, self).__init__(axes, extractor, expression, **kwargs)

    def __get_data__(self):
        args = (self._time_index, self.datum, self.limits, self.count)

        return self.extractor.get_particle_density(*args)

    def __prep_graphics_obj__(self, **kwargs):
        # Pop key word arguments which are not used by the graphics object
        self.count = kwargs.pop('count', 10000)
        self.index = np.arange(0, self.extractor.np, np.ceil(self.extractor.np/self.count)).astype(dtype=np.int32)

        x = self.extractor.get_particle_data('x', self._time_index)[self.index]
        y = self.extractor.get_particle_data('y', self._time_index)[self.index]

        # Instantiate graphics object with no data, data will be added on draw event automatically
        self.sca = self.axes.scatter(x, y, **kwargs)

    def __static_update__(self):
        pass

    def __dynamic_update__(self):
        x = self.extractor.get_particle_data('x', self._time_index)[self.index]
        y = self.extractor.get_particle_data('y', self._time_index)[self.index]
        data = self.__get_data__()

        self.sca.set_offsets(np.column_stack((x, y)))
        self.sca.set_array(data)

    def zoom(self):
        pass


# ------------------------------------------------ Delta Visual Objects ------------------------------------------------
class DeltaSheetPatch(SheetPatch):
    """
    Class for dynamic visualization of model result sheet extract differences as collection of patches

    Arguments
    ---------
    :param axes -- object | Axes object
    :param extractor -- tuple | Extractor objects (base, developed)
    :param expression -- string | Expression that defines variable

    Keyword Arguments
    -----------------
    :param datum -- string | Vertical depth-averaging datum i.e sigma, depth, height, elevation, top, bottom.
    :param limits -- tuple | Vertical depth-averaging limits relative to vertical datum.

    Returns
    -------
    :param sheet -- object | DeltaSheetPatch instance

    Examples
    --------
    >> base_xtr = FvExtractor('my_file_base.nc')
    >> dev_xtr = FvExtractor('my_file_developed.nc')
    >> diff_sheet = DeltaSheetPatch(axes, (base_xtr, dev_xtr), 'H')
    """

    def __init__(self, axes, extractors, expression, datum='sigma', limits=(0, 1), **kwargs):
        # Store multiple extractor objects
        self.extractors = extractors

        # Initialize as super class
        super(DeltaSheetPatch, self).__init__(axes, self.extractors[0], expression, datum, limits, **kwargs)

    def __get_data__(self):
        self.extractor = self.extractors[0]
        data_1 = super(DeltaSheetPatch, self).__get_data__()

        self.extractor = self.extractors[1]
        data_2 = super(DeltaSheetPatch, self).__get_data__()

        return data_2 - data_1


class DeltaSheetContour(SheetContour):
    """
    Class for dynamic visualization of model result sheet extract differences as contours

    Arguments
    ---------
    :param axes -- object | Axes object
    :param extractor -- tuple | Extractor objects (base, developed)
    :param expression -- string | Expression that defines variable

    Keyword Arguments
    -----------------
    :param datum -- string | Vertical depth-averaging datum i.e sigma, depth, height, elevation, top, bottom.
    :param limits -- tuple | Vertical depth-averaging limits relative to vertical datum.

    Returns
    -------
    :param sheet -- object | DeltaSheetContour instance

    Examples
    --------
    >> base_xtr = FvExtractor('my_file_base.nc')
    >> dev_xtr = FvExtractor('my_file_developed.nc')
    >> diff_sheet = DeltaSheetContour(axes, (base_xtr, dev_xtr), 'H')
    """

    def __init__(self, axes, extractors, expression, datum='sigma', limits=(0, 1), **kwargs):
        # Store multiple extractor objects
        self.extractors = extractors

        # Initialize as super class
        super(DeltaSheetContour, self).__init__(axes, self.extractors[0], expression, datum, limits, **kwargs)

    def __get_data__(self):
        self.extractor = self.extractors[0]
        data_1 = super(DeltaSheetContour, self).__get_data__()

        self.extractor = self.extractors[1]
        data_2 = super(DeltaSheetContour, self).__get_data__()

        return data_2 - data_1


class DeltaSheetVector(SheetVector):
    """
    Class for dynamic visualization of model result sheet extract differences as gridded vector field

    Arguments
    ---------
    :param axes -- object | Axes object
    :param extractor -- tuple | Extractor objects (base, developed)
    :param expression -- string | Expression that defines variable

    Keyword Arguments
    -----------------
    :param datum -- string | Vertical depth-averaging datum i.e sigma, depth, height, elevation, top, bottom.
    :param limits -- tuple | Vertical depth-averaging limits relative to vertical datum.

    Returns
    -------
    :param vector -- object | DeltaSheetVector instance

    Examples
    --------
    >> base_xtr = FvExtractor('my_file_base.nc')
    >> dev_xtr = FvExtractor('my_file_developed.nc')
    >> diff_sheet = DeltaSheetVector(axes, (base_xtr, dev_xtr), ['V_x', 'V_y'])
    """

    def __init__(self, axes, extractors, expression, datum='sigma', limits=(0, 1), **kwargs):
        # Store multiple extractor objects
        self.extractors = extractors

        # Initialize as super class
        super(DeltaSheetVector, self).__init__(axes, self.extractors[0], expression, datum, limits, **kwargs)

    def __get_data__(self):
        self.extractor = self.extractors[0]
        data_1 = super(DeltaSheetVector, self).__get_data__()

        self.extractor = self.extractors[1]
        data_2 = super(DeltaSheetVector, self).__get_data__()

        return data_2[0] - data_1[0], data_2[1] - data_1[1]