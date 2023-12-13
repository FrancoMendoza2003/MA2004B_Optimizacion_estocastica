import random
import matplotlib.pyplot as plt
try:
    def pi(n):
        puntos_dentro = 0
        puntos_cuadrado = 0
        x_dentro = []
        y_dentro = []
        x_cuadrado = []
        y_cuadrado = []
        for i in range(n):
            x = random.random()
            y= random.random()
            distancia = x**2+y**2
            if distancia <= 1:
                puntos_dentro+=1
                x_dentro.append(x)
                y_dentro.append(y)
            else:
                x_cuadrado.append(x)
                y_cuadrado.append(y)
            puntos_cuadrado+=1
        pi_estimado = (puntos_dentro/puntos_cuadrado)*4

        return pi_estimado,x_dentro,y_dentro,x_cuadrado,y_cuadrado
    n = int(input("Cantidad de puntos a generar: "))
    pi_estimado, x_dentro, y_dentro, x_cuadrado, y_cuadrado = pi(n)

    print("Estimacion de pi = ",pi_estimado)
    plt.figure(figsize=(6, 6))
    plt.scatter(x_dentro, y_dentro, color='blue', s=1, label='Dentro del círculo')
    plt.scatter(x_cuadrado, y_cuadrado, color='red', s=1, label='Fuera del círculo')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.title(f"Estimación de pi = {pi_estimado}")
    plt.show()
    print("X y Y dentro del circulo")
    for i in range(len(x_dentro)):
        print(f"({x_dentro[i]}, {y_dentro[i]})")
    print()
    print("X y Y fuera del circulo")
    for i in range(len(x_cuadrado)):
        print(f"({x_cuadrado[i]}, {y_cuadrado[i]})")
except:
    print("El input fue malo!")
