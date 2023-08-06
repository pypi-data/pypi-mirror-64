from .color import Color
from typing import List


class BallSortPuzzle:

    def __init__(self, cells: List[List[int]], max_in_cell=4):
        self.cells = cells
        self.max_in_cell = max_in_cell
        self.validate()

    def validate(self):
        colors = {}
        for cell in self.cells:
            for color in cell:
                if color in colors.keys():
                    colors[color] += 1
                else:
                    colors[color] = 1

        color_amounts = colors.values()
        if self.cells_len < len(color_amounts) or any(amount != self.max_in_cell for amount in color_amounts):
            self.clear_cells()
            raise Exception('The ball sort level is not valid.')

    @property
    def cells(self):
        return self.__cells

    @cells.setter
    def cells(self, cells):
        self.__cells = [cell[:] for cell in cells]
        self.cells_len = len(self.cells)

    def clear_cells(self):
        self.cells = [[]]

    def finished(self) -> bool:
        for cell in self.cells:
            if len(cell) not in (0, self.max_in_cell):
                return False
            if len(cell) == self.max_in_cell and any(cell[0] != c for c in cell):
                return False
        return True

    def __move(self, color: int, from_index: int, to_index: int):
        self.cells[to_index].append(color)  # append color here
        self.cells[from_index].pop(-1)  # pop from cell

    def __not_empty_cells(self):
        return filter(lambda i: len(self.cells[i]) > 0, range(self.cells_len))

    def __top_color(self, index: int) -> int:
        return self.cells[index][-1]

    def solve(self) -> bool:
        if self.finished():
            return True

        # not empty cells
        for current_index in self.__not_empty_cells():

            current_color = self.__top_color(current_index)

            if any(c != current_color for c in self.cells[current_index]):
                # all other indexes
                for other_index in filter(lambda i: i != current_index, range(self.cells_len)):

                    other_cell_len = len(self.cells[other_index])

                    # other index not empty and not full
                    if 0 < other_cell_len < self.max_in_cell:
                        # same color at the top
                        if current_color == self.__top_color(other_index):
                            self.__move(current_color, from_index=current_index, to_index=other_index)
                            if self.solve():
                                print(f'Moved {Color.to_string(current_color)} from {current_index} to {other_index}')
                                return True
                            else:
                                self.__move(current_color, from_index=other_index, to_index=current_index)

                    # other index empty
                    elif other_cell_len == 0:
                        self.__move(current_color, from_index=current_index, to_index=other_index)
                        if self.solve():
                            print(f'Moved {Color.to_string(current_color)} from {current_index} to {other_index}')
                            return True
                        else:
                            self.__move(current_color, from_index=other_index, to_index=current_index)
            # same colors here but other cell can have the same colors as well
            else:
                for other_index in filter(lambda i: i != current_index and self.__top_color(i) == current_color,
                                          self.__not_empty_cells()):
                    if len(self.cells[current_index]) > len(self.cells[other_index]):
                        self.__move(current_color, from_index=other_index, to_index=current_index)
                        if self.solve():
                            print(f'Moved {Color.to_string(current_color)} from {other_index} to {current_index}')
                            return True
                        else:
                            self.__move(current_color, from_index=current_index, to_index=other_index)
        # no other movement possible
        return False
