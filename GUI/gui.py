import sys
from PyQt4 import QtGui, QtCore
import importlib.machinery
from pycella.automaton.automaton import CA

# TODO
# default colors from conf_file
# name of the rules from conf_file

class CaGui(QtGui.QMainWindow):
    def __init__(self, rules_path):
        super(CaGui, self).__init__()

        self._rules_path = rules_path
        self.init_toolbar()
        self._grid = Grid(self)
        self._timer = QtCore.QBasicTimer()
        self._interval = 1000

        self.setCentralWidget(self._grid)
        self.statusBar()
        self.setWindowTitle('Pycella')
        self.setGeometry(50, 200, 900, 900)
        #TODO choose show method
        self.showMaximized()
        #self.show()

    def init_toolbar(self):
        self._toolbar = self.addToolBar('Actions')


        step_action = QtGui.QAction(QtGui.QIcon('Step.png'),
                                    '&Step', self)
        step_action.setShortcut('Enter')
        step_action.triggered.connect(self.step)
        self._toolbar.addAction(step_action)

        play_action = QtGui.QAction(QtGui.QIcon('Play.png'),
                                    '&Play', self)
        play_action.triggered.connect(self.play)
        self._toolbar.addAction(play_action)

        pause_action = QtGui.QAction(QtGui.QIcon('Pause.png'),
                                     '&Pause', self)
        pause_action.triggered.connect(self.pause)
        self._toolbar.addAction(pause_action)

        toggle_action = QtGui.QAction('&Toggle Play/Pause', self)
        toggle_action.setShortcut('Space')
        toggle_action.triggered.connect(self.toggle)

        reset_action = QtGui.QAction(QtGui.QIcon('Reset.png'),
                                     '&Reset', self)
        reset_action.setShortcut('Backspace')
        reset_action.triggered.connect(self.reset)
        self._toolbar.addAction(reset_action)

        speed_down_action = QtGui.QAction(QtGui.QIcon('SpeedDown.png'),
                                          '&Speed Down', self)
        speed_down_action.setShortcut('Down')
        speed_down_action.triggered.connect(self.speed_down)
        self._toolbar.addAction(speed_down_action)

        speed_up_action = QtGui.QAction(QtGui.QIcon('SpeedUp.png'),
                                        '&Speed Up', self)
        speed_up_action.setShortcut('Up')
        speed_up_action.triggered.connect(self.speed_up)
        self._toolbar.addAction(speed_up_action)

        control_menu = self.menuBar().addMenu('&Control')
        control_menu.addAction(step_action)
        control_menu.addAction(play_action)
        control_menu.addAction(pause_action)
        control_menu.addAction(toggle_action)
        control_menu.addAction(reset_action)
        control_menu.addAction(speed_down_action)
        control_menu.addAction(speed_up_action)


    def step(self):
        self._grid.step()

    def play(self):
        if not self._timer.isActive():
            self._timer.start(self._interval, self)

    def pause(self):
        if self._timer.isActive():
            self._timer.stop()

    def toggle(self):
        if self._timer.isActive():
            self._timer.stop()
        else:
            self._timer.start(self._interval, self)

    def reset(self):
        pass

    def speed_up(self):
        if self._interval / CaGui.FACTOR > 1:
            self._interval /= CaGui.FACTOR
        self._timer.start(self._interval, self)

    def speed_down(self):
        self._interval *= CaGui.FACTOR
        self._timer.start(self._interval, self)

    def timerEvent(self, event):
        if event.timerId() == self._timer.timerId():
            self._grid._automaton.step()
            self.repaint()

    FACTOR = 1.5

class Grid(QtGui.QFrame):

    def __init__(self, window):
        super(Grid, self).__init__()
        self._window = window
        self._horizontal_count = 15
        self._vertical_count = 10
        self._color = QtCore.Qt.darkGray
        self.create_automaton()
        self.MIN_BOX_HEIGHT = 20
        self.MIN_BOX_WIDTH = 20

    def create_automaton(self):
        rules_path = self._window._rules_path
        rules_name = rules_path.split(r'/')[-1]
        loader = importlib.machinery.SourceFileLoader(rules_name, rules_path)
        module = loader.load_module()

        self._empty_cell = module.empty_cell
        rules = module.rules
        initial_buff = [[self._empty_cell()
                        for _ in range(self._horizontal_count)]
                        for i in range(self._vertical_count)]
        self._automaton = CA(initial_buff, rules, self._empty_cell,
                             bounded=False)
        self._automaton._expand_callback = self._box_limit
        self._default_cell = module.default_cell

    def _box_limit(self):
        rect = self.contentsRect()
        box_width = rect.width() // self._horizontal_count
        box_height = rect.height() // self._vertical_count
        if box_width < self.MIN_BOX_WIDTH or box_height < self.MIN_BOX_HEIGHT:
            return False
        else:
            return True

    def paintEvent(self, e):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.draw_grid(painter)
        painter.end()
        self._window.statusBar().clearMessage()
        generation = self._automaton.generation
        self._window.statusBar().showMessage("generation={}".format(generation))

    def draw_grid(self, painter):
        # TODO get configured in file color
        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
        painter.setPen(pen)

        rect = self.contentsRect()
        left = rect.left()
        right = rect.right()
        top = rect.top()
        bottom = rect.bottom()
        self._horizontal_count = self._automaton.width
        self._vertical_count = self._automaton.height
        box_width = rect.width() // self._horizontal_count
        box_height = rect.height() // self._vertical_count
        # TODO remove
        print(box_width, box_height)
        y = top
        right_max = self._horizontal_count * box_width
        for i in range(self._vertical_count+1):
            painter.drawLine(left, y, right_max, y)
            y += box_height
        y -= box_height

        x = left
        bottom_max = y
        for i in range(self._horizontal_count+1):
            painter.drawLine(x, top, x, bottom_max)
            x += box_width

        # TODO get configured in file color
        pen = QtGui.QPen(QtCore.Qt.darkGray, 1, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        #fill living cells
        coordinates = ((i, j) for i in range(self._vertical_count)
                       for j in range(self._horizontal_count))
        for cell in self._automaton:
            y, x = next(coordinates)
            # TODO remove
            #print('({}, {})'.format(x, y), end=' ')
            # starting from inside the box
            x = x * box_width + 1
            y = y * box_height + 1
            # TODO remove
            # print(x, y)
            if cell:
                painter.fillRect(x, y, box_width-1, box_height-1, self._color)
        # TODO remove
        #print(self._automaton)

    def pix_to_row_col(self, event):
        rect = self.contentsRect()
        box_width = int(rect.width() / self._horizontal_count) - 1
        box_height = int(rect.height() / self._vertical_count) - 1
        col = event.x() // box_width
        row = event.y() // box_height
        # this is to account for the border width
        col = (event.x() - col) // box_width
        row = (event.y() - row) // box_height
        # TODO remove
        #print("row={}, col={}".format(row, col))
        # accounting that the automaton indices start from 1
        return row + 1, col + 1

    def mouseReleaseEvent(self, event):
        if self._window._timer.isActive():
            return
        row, col = self.pix_to_row_col(event)
        if self._automaton[row, col]:
            self._automaton[row, col] = self._empty_cell()
        else:
            self._automaton[row, col] = self._default_cell()
        self.repaint()

    def step(self):
        self._automaton.step()
        self.repaint()

if __name__ == '__main__':
    app = QtGui.QApplication([])
    ca_gui = CaGui('/home/bozhidar/schoolcode/Python/pycella/GUI/rules.py')
    sys.exit(app.exec_())
