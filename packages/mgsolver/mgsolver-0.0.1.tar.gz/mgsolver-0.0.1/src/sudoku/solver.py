import numpy as np
import pandas as pd


def __next__(x, y):
    return (0, y + 1) if x + 1 > 8 else (x + 1, y)


def __previous__(x, y):
    return (8, y - 1) if x - 1 < 0 else (x - 1, y)


def solve(sudoku):
    fixed_nums = sudoku > 0
    x = y = 0
    num = 1
    
    while x < 9 and y < 9:
        if fixed_nums.iloc[y, x]:
            x, y = __next__(x, y)
            num = 1
            continue

        if num > 9:
            sudoku.iloc[y, x] = 0
            x, y = __previous__(x, y)
            while fixed_nums.iloc[y, x]:
                x, y = __previous__(x, y)
            if y < 0:
                print("Sudoku has no solution!")
                return None
            num = sudoku.iloc[y, x] + 1
            continue

        row = np.array(sudoku.iloc[y, :])
        col = np.array(sudoku.iloc[:, x])
        square = np.array(sudoku.iloc[(y // 3) * 3:(y // 3) * 3 + 3, (x // 3) * 3:(x // 3) * 3 + 3])
        
        if num in row or num in col or num in square:
            num += 1
            continue
        else:
            sudoku.iloc[y, x] = num
            x, y = __next__(x, y)
            num = 1
            continue


def solve_recursively(sudoku):
    fixed_nums = sudoku > 0

    def putnumber(x, y, num):
        if num > 9:
            sudoku.iloc[y, x] = 0
            x, y = __previous__(x, y)
            while fixed_nums.iloc[y, x]:
                x, y = __previous__(x, y)
                if y < 0:
                    print("Sudoku has no solution!")
                    return None
            return putnumber(x - 1, y, sudoku.iloc[y, x - 1] + 1)

        if y + 1 > 8 and x + 1 > 8:
            return True

        if fixed_nums.iloc[y, x]:
            x, y = __next__(x, y)
            return putnumber(x, y, 1)

        row = np.array(sudoku.iloc[y, :])
        col = np.array(sudoku.iloc[:, x])
        square = np.array(sudoku.iloc[(y // 3)*3:(y // 3)*3 + 3, (x // 3)*3:(x // 3)*3 + 3])
        
        if num in row or num in col or num in square:
            return putnumber(x, y, num + 1)
        else:
            sudoku.iloc[y, x] = num
            x, y = __next__(x, y)
            return putnumber(x, y, 1)

    putnumber(0, 0, 1)


def main():
    print("Reading file...")
    sudoku = pd.read_csv("sudoku.csv", dtype=int, header=None)
    print(sudoku)
    print("Solving sudoku...")
    solve(sudoku)
    print(sudoku)
    

if __name__ == "__main__":
    main()