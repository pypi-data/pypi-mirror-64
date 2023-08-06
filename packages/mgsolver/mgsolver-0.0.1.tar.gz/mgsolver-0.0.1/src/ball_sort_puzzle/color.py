class Color:
    orange = 0
    lightgreen = 1
    purple = 2
    gray = 3
    pink = 4
    red = 5
    green = 6
    lightblue = 7
    blue = 8

    @staticmethod
    def to_string(c: int) -> str:
        return ['orange', 'lightgreen', 'purple', 'gray', 'pink', 'red', 'green', 'lightblue', 'blue'][c]
