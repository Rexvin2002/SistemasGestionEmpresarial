#
# Kevin Gómez Valderas 2ºDAM
#
#
# MÉTODOS
#
def ejemplo1():

    a, b = 0, 1

    while a < 100:

        print(a, end=",")
        a, b = b, a + b


def ejemplo2():

    texto = "SGE es " + ("mi módulo " "favorito ")
    print(texto)
    print(texto[0:3])
    print(texto[-3:])

    texto = 3 * texto
    print(texto)

    texto = texto[17:]
    print(texto)
    #   texto[0:3]='FOL'


def frase(sujeto="SGE", verbo="es", predicado="mi modulo favorito"):

    print("{} {} {}".format(sujeto, verbo, predicado))
    print("{1} {0} {2}".format(sujeto, verbo, predicado))


def ejemplo3():

    frase()
    frase(predicado="muy divertido")


def ejemplo4():

    squares = [1, 4, 9]
    squares = squares + [16, 25]
    squares.append(36)
    print(squares)

    x = squares.pop()
    print(x)
    print(squares)

    squares1 = list(map(lambda x: x**2, range(6, 10)))
    squares += squares1
    squares += [x**2 for x in range(10, 13)]
    print(squares)

    cubes = [[x, x**3] for x in range(6)]
    print(cubes)

    for i, j in cubes:

        print(i, " ", j)


def ejemplo5():

    dic = {"uno": 1, "dos": 2, "tres": 3}
    print(dic["dos"] * dic["dos"])

    dic["cuatro"] = 4
    nombres = ["cinco", "seis", "siete", "ocho"]
    numeros = [5, 6, 7, 8]

    for no, nu in zip(nombres, numeros):

        dic[no] = nu

    print(dic)

    l = list(dic.keys())
    k = list(dic.values())
    l.sort()

    print(l)
    print(k)


def listalong(lista):

    return [len(x) for x in lista]


def ejemplo6():

    lista = ["a", "ab", "abc"]
    lisal = listalong(lista)

    print(lisal)


def soloimpar(n):

    if n % 2 == 0:

        raise Exception("Solo impares")


def ejemplo7():

    h = int(input("Dime un numero: "))

    try:

        soloimpar(h)
        print("El numero es impar")

    except:

        print("El numero es par")


def nfuncion(numero):

    return lambda x, y: (x - y) * 2 if x - y > numero else (x - y)


def ejemplo8():

    f = nfuncion(8)
    f1 = nfuncion(10)
    print(f(10, 1))
    print(f1(10, 1))


#
# USO
#
ejemplo8()
