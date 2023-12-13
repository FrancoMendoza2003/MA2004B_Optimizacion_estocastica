import numpy as np
from scipy.stats import chi2

def generacion_pseudoaleatorios(semilla, m, a, c, total, intervalos):
    lista_pseudoaleatorios = []

    # Paso 1: Guardamos la semilla
    lista_pseudoaleatorios.append(semilla)
    valor_generado = semilla

    # Paso 2: Inicia ciclo de total de números pseudoaleatorios
    for i in range(total):
        valor_anterior = valor_generado

        # Paso 2.1: Generar el siguiente valor pseudoaleatorio
        valor_generado = (a * valor_anterior + c) % m

        # Paso 2.2: Añadir elemento a la lista de retorno
        lista_pseudoaleatorios.append(valor_generado)

        # Paso 2.3: Criterio de paro
        if valor_generado == valor_anterior:
            break

    frecuencias, _ = np.histogram(lista_pseudoaleatorios, bins=intervalos)
    esperadas = [total / intervalos] * intervalos
    estadistico_chi2 = sum((frecuencias - esperadas) ** 2 / esperadas)
    grados_de_libertad = intervalos - 1
    valor_p = 1 - chi2.cdf(estadistico_chi2, df=grados_de_libertad)

    return lista_pseudoaleatorios, estadistico_chi2, valor_p

semilla = 5
m = 13
a = 7
c = 3
total = 1000
intervalos = 10

resultados, chi2, p_value = generacion_pseudoaleatorios(semilla, m, a, c, total, intervalos)
print("Números Pseudoaleatorios:", resultados)
print("Estadístico Chi-Cuadrado:", chi2)
print("Valor p:", p_value)

if p_value > 0.05:
    print("La distribución es uniforme (no se rechaza la hipótesis nula)")
else:
    print("La distribución no es uniforme (se rechaza la hipótesis nula)")
