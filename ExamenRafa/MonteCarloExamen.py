import numpy as np
try:
    def MonteCarlo(funcion, LimInf, LimSup, n):
        x_values = np.random.uniform(LimInf, LimSup, n)
        y_values = [eval(funcion.replace("x",str(x))) for x in x_values]
        area = [(LimSup - LimInf) / n * y for y in y_values]
        area_estimada =  sum(area)
        return x_values,y_values,area, area_estimada

    def MonteCarloNoInput(funcion, LimInf, LimSup, n):
        x_values = np.random.uniform(LimInf, LimSup, n)
        y_values = [funcion(x) for x in x_values]
        area = [(LimSup - LimInf) / n * y for y in y_values]
        area_estimada =  sum(area)
        return x_values,y_values,area, area_estimada

    decision = int(input("Si quieres ingresar tu propia funcion al prgorama, pon 1 si no pon 0: "))
    if decision == 1:
        funcion = input("Ingrese la función en terminos de x, si va a usar exponentes use **: ")

        a = int(input("Ingrese el Límite Inferior: "))
        b = int(input("Ingrese el Límite Superior: "))
        n = int(input("Ingrese el tamaño de la muestra: "))
        if a>b:
            print("El Limite inferior es mayor que el superior, no es valido!")
        elif n <=0:
            print("El numero de simulaciones no es valido")
        else:
            x_values, y_values, areas, area_estimate = MonteCarlo(funcion, a, b, n)
            ("----------------------------------------------------------------------------------------------")
            print("Usando la funcion: \n",funcion)
            print("Valores aleatorios generados:", np.round(x_values,3))
            print("Alturas correspondientes:", np.round(y_values,3))
            print("Áreas individuales debajo de la curva:", np.round(areas,3))
            print("Estimación del área bajo la curva:", np.round(area_estimate,3))
    else:
        def funcion(x):
            return x**2-2*x+1
        a = int(input("Ingrese el Límite Inferior: "))
        b = int(input("Ingrese el Límite Superior: "))
        n = int(input("Ingrese el tamaño de la muestra: "))
        if a>b:
            print("El Limite inferior es mayor que el superior, no es valido!")
        elif n <=0:
            print("El numero de simulaciones no es valido")
        else:
            x_values, y_values, areas, area_estimate = MonteCarloNoInput(funcion, a, b, n)
            print("----------------------------------------------------------------------------------------")
            print("Usando la funcion con polinomio grado 2:\nx**2-2*x+1")
            print("Valores aleatorios generados:", np.round(x_values,3))
            print("Alturas correspondientes:", np.round(y_values,3))
            print("Áreas individuales debajo de la curva:", np.round(areas,3))
            print("Estimación del área bajo la curva:", np.round(area_estimate,3))
            print()

        def funcion2(x):
            return 3**(x)
        a = int(input("Ingrese el Límite Inferior: "))
        b = int(input("Ingrese el Límite Superior: "))
        n = int(input("Ingrese el tamaño de la muestra: "))
        if a>b:
            print("El Limite inferior es mayor que el superior, no es valido!")
        elif n <=0:
            print("El numero de simulaciones no es valido")
        else:

            x_values, y_values, areas, area_estimate = MonteCarloNoInput(funcion2, a, b, n)
            print("------------------------------------------------------------------------------------------")
            print("Usando la funcion exponencial:\n3**(x)")
            print("Valores aleatorios generados:", np.round(x_values,3))
            print("Alturas correspondientes:", np.round(y_values,3))
            print("Áreas individuales debajo de la curva:", np.round(areas,3))
            print("Estimación del área bajo la curva:", np.round(area_estimate,3))
            print()
except:
    print("Algun input fue malo!")
