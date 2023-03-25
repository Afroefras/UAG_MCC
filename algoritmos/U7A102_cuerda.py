def cut_rod(lengths, prices, n):
    # Obtenemos la longitud de las listas de precios y longitudes
    m = len(lengths)
    # Inicializamos una matriz de tamaño (m+1) x (n+1) para almacenar los valores óptimos
    # de los subproblemas
    dp = [[0 for j in range(n + 1)] for i in range(m + 1)]
    # Inicializamos una lista de tamaño (n+1) para almacenar la lista de longitudes óptimas
    # para cada subproblema
    cuts = [[] for i in range(n + 1)]

    # Iteramos sobre todas las longitudes de las subcuerdas posibles
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Si la longitud de la subcuerda es menor o igual a la longitud del problema actual,
            # entonces podemos considerar cortar la cuerda y actualizar el valor óptimo
            if lengths[i - 1] <= j:
                # Si cortamos la cuerda en esta posición, entonces podemos obtener un valor
                # de beneficio igual al precio de esta longitud más el valor óptimo para el
                # resto de la cuerda
                if prices[i - 1] + dp[i][j - lengths[i - 1]] > dp[i - 1][j]:
                    # Actualizamos el valor óptimo y la lista de cortes óptimos para la longitud actual
                    dp[i][j] = prices[i - 1] + dp[i][j - lengths[i - 1]]
                    cuts[j] = cuts[j - lengths[i - 1]] + [lengths[i - 1]]

                # Si no cortamos la cuerda en esta posición, entonces simplemente usamos el valor óptimo
                # del subproblema anterior
                else:
                    dp[i][j] = dp[i - 1][j]
                    
            # Si la longitud de la subcuerda es mayor a la longitud del problema actual,
            # entonces no podemos cortar la cuerda y simplemente usamos el valor óptimo
            # del subproblema anterior
            else:
                dp[i][j] = dp[i - 1][j]

        # Hacemos una copia de la lista de cortes óptimos para la longitud actual
        # antes de actualizar la lista de cortes óptimos para la siguiente longitud
        cuts[j] = cuts[j][:]

    # Retornamos el valor óptimo para el problema completo y la lista de cortes óptimos para la longitud n
    return dp[m][n], cuts[n]


LENGTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
PRICES = [1, 4, 10, 12, 15, 20, 21, 32, 31, 41, 51]
ROD_LENGHT = 11


result = cut_rod(LENGTHS, PRICES, ROD_LENGHT)
print(result)
