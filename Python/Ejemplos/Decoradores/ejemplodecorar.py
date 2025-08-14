#
# Kevin Gómez Valderas 2ºDAM
#
#
# MÉTODOS
#
def funcion_a(funcion_b):

    def funcion_c():

        print("Antes de la ejecución de la función a decorar")

        funcion_b()

        print("Después de la ejecución de la función a decorar")

    return funcion_c


#
# USO
#
@funcion_a
def saludar():

    print("Hola mundo!!")


saludar()
