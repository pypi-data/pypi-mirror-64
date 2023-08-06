import importlib.resources as importlib_resources


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        point = Point(self.x, self.y)
        point += other
        return point

    def __iadd__(self, other):
        self.x += other[0]
        self.y += other[1]
        return self


def asset_path(name):
    return importlib_resources.open_binary(
        "vimfected.assets",
        name,
    )
