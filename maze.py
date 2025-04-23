from cell import Cell
import random
import time


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_columns,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_columns = num_columns
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed: 
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_columns):
            row = []
            for j in range(self._num_rows):
                row.append(Cell(self._win))
            self._cells.append(row)
        for i in range(self._num_columns):
            for j in range(self._num_rows):
                self._draw_cell(i,j)


    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()
        

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        entrance = self._cells[0][0]
        exit = self._cells[self._num_columns - 1][self._num_rows - 1]

        entrance.has_top_wall = False
        self._draw_cell(0,0)

        exit.has_bottom_wall = False
        self._draw_cell(self._num_columns - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []

            # find cells to visit
            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                to_visit.append((i - 1, j))

            # right
            if i < self._num_columns - 1 and not self._cells[i + 1][j].visited:
                to_visit.append((i+1, j))

            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                to_visit.append((i, j - 1))

            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                to_visit.append((i, j + 1))
            
            # break if nowhere else to go
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return

            # choose direction
            next_cell_index = random.randrange(len(to_visit))
            next_cell = to_visit[next_cell_index]

            # break walls between current and next cell
            # right
            if next_cell[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False

            # left
            if next_cell[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            
            # up
            if next_cell[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            # down
            if next_cell[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j - 1].has_top_wall = False

            # visit the next cell
            self._break_walls_r(next_cell[0], next_cell[1])

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r(i=0, j=0)

    def _solve_r(self, i, j):
        self._animate()

        # visit current cell
        self._cells[i][j].visited = True

        if i == self._num_columns - 1 and j == self._num_rows -1:
            return True

        # move left if possible
        if (
            i > 0
            and not self._cells[i][j].has_left_wall
            and not self._cells[i - 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else: 
                self._cells[i][j].draw_move(self._cells[i - 1][j], undo=True)

        # move right if possible
        if (
            i < self._num_columns - 1
            and not self._cells[i][j].has_right_wall
            and not self._cells[i + 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else: 
                self._cells[i][j].draw_move(self._cells[i + 1][j], undo=True)

        # move up if possible
        if (
            j > 0
            and not self._cells[i][j].has_top_wall
            and not self._cells[i][j - 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else: 
                self._cells[i][j].draw_move(self._cells[i][j - 1], undo=True)

        # move down if possible
        if (
            j < self._num_rows - 1
            and not self._cells[i][j].has_bottom_wall
            and not self._cells[i][j + 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else: 
                self._cells[i][j].draw_move(self._cells[i][j + 1], undo=True)

        return False
