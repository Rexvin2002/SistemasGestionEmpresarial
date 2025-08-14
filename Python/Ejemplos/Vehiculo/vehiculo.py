#
# Kevin Gómez Valderas 2ºDAM
#
#
# CLASES
#
class Vehiculo:

    #
    # MÉTODOS
    #
    def __init__(self, nruedas):

        self.numeroruedas = nruedas

    def mostrar(self):

        print("Vehiculo con ", self.numeroruedas, " ruedas")


class Coche(Vehiculo):

    #
    # MÉTODOS
    #
    def __init__(self):

        super().__init__(4)
        self._matricula = "??????"

    def matricular(self, nmatricula):

        self._matricula = nmatricula


class Bicicleta(Vehiculo):

    #
    # MÉTODOS
    #
    def __init__(self):

        super().__init__(2)
        self.ruedashinchadas = False

    def hincharrueda(self):

        self.ruedashinchadas = True

    def mostrar(self):

        if self.ruedashinchadas:

            mensaje = " hinchadas"

        else:

            mensaje = "deshinchadas"

        print("Bicicleta con las ruedas ", mensaje)


class Taller:

    #
    # MÉTODOS
    #
    def __init__(self):

        self.vehiculos = []

    def nuevocoche(self, matricula):

        c = Coche()
        c.matricular(matricula)
        self.vehiculos.append(c)

    def nuevabici(self):

        b = Bicicleta()
        self.vehiculos.append(b)

    def hincharruedas(self):

        for v in self.vehiculos:

            if isinstance(v, Bicicleta):

                v.hincharrueda()

    def mostrartaller(self):

        for v in self.vehiculos:

            v.mostrar()

    def metodotonto(self):

        print("Vaya Tonteria")


#
# USO
#
t = Taller()
t.nuevocoche("AAAAA")
t.nuevabici()
t.nuevabici()
t.nuevocoche("BBBB")
t.mostrartaller()
t.hincharruedas()
t.mostrartaller()
t.metodotonto()
