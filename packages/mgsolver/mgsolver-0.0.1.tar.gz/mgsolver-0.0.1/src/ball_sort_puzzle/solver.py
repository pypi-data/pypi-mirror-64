from .color import Color
from typing import List


class BallSortPuzzle:

    def __init__(self, cells: List[List[int]], max_in_cell=4):
        self.cells = [cell[:] for cell in cells]
        self.cells_len = len(self.cells)
        self.max_in_cell = max_in_cell

    def finished(self) -> bool:
        for cell in self.cells:
            if len(cell) not in (0, self.max_in_cell):
                return False
            if len(cell) == self.max_in_cell and any(cell[0] != c for c in cell):
                return False
        return True

    def move(self, color: int, from_index: int, to_index: int):
        self.cells[to_index].append(color)  # append color here
        self.cells[from_index].pop(-1)  # pop from cell

    def solve(self, current_index=0) -> bool:
        if self.finished():
            return True

        if current_index > self.cells_len - 1:
            return False

        # empty, nothing to move from here
        if len(self.cells[current_index]) == 0:
            return self.solve(current_index + 1)

        current_color = self.cells[current_index][-1]
        alone = len(self.cells[current_index]) == 1

        def filter_f(i: int) -> bool:
            return 0 < len(self.cells[i]) < self.max_in_cell \
                   and i != current_index \
                   and self.cells[i][-1] == current_color

        # try non empty first
        for other_index in filter(filter_f, range(self.cells_len)):
            # last color in current cell or the colors are different under the top
            if alone or any(c != current_color for c in self.cells[current_index][:-1]) \
                    or all(c == current_color for c in self.cells[other_index]):
                # actual movement
                self.move(color=current_color, from_index=current_index, to_index=other_index)

                # start moving again
                if self.solve():
                    # if successful, then finished
                    print(f'Moved {Color.to_string(current_color)} from {current_index} to {other_index}')
                    return True
                else:
                    # if unsuccessful, then there is no other possible move and move on to the next one
                    self.move(color=current_color, from_index=other_index, to_index=current_index)

        if not alone:
            # moving to non empty did not work so place this into empty cell if exists
            empty_cell_indexes = list(filter(lambda i: len(self.cells[i]) == 0, range(self.cells_len)))
            if len(empty_cell_indexes) > 0:
                # move all possible colors to empty cell
                self.move(color=current_color, from_index=current_index, to_index=empty_cell_indexes[0])

                if self.solve():
                    # if successful, then finished
                    print(f'Moved {Color.to_string(current_color)} from {current_index} to {empty_cell_indexes[0]}')
                    return True
                else:
                    # if unsuccessful, then there is no other possible move and move on to the next one
                    self.move(color=current_color, from_index=empty_cell_indexes[0], to_index=current_index)

        # no successful movement to other indexes, continuing moving from next index
        return self.solve(current_index + 1)
