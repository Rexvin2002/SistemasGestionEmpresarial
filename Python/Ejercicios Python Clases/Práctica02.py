#
# Kevin Gómez Valderas 2ºDAM
#
#
# CLASES
#
class GeometricFigure:

    def surface_area(self):

        return 0


class RightTriangle(GeometricFigure):

    def __init__(self, leg1, leg2):

        self.leg1 = leg1
        self.leg2 = leg2

    def hypotenuse(self):

        return (self.leg1**2 + self.leg2**2) ** 0.5

    def surface_area(self):

        return 0.5 * self.leg1 * self.leg2


class Rectangle(GeometricFigure):

    def __init__(self, base, height):

        self.base = base
        self.height = height

    def surface_area(self):

        return self.base * self.height


class FigureList:

    def __init__(self):

        self.figures = []

    def add_triangle(self, triangle):

        self.figures.append(triangle)

    def add_square(self, square):

        self.figures.append(square)

    def total_surface_area(self):

        return sum(figure.surface_area() for figure in self.figures)

    def count_triangles(self):

        return sum(1 for figure in self.figures if isinstance(figure, RightTriangle))
