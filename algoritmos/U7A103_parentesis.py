class MatrixParenthesis:
    def __init__(self) -> None:
        pass

    def print_parenthesis(self, s: list, i: int, j: int) -> str:
        # Si la matriz es de tamaño 1, la cadena se devuelve en forma de A1
        if i == j:
            return f"A{i+1}"
        # Si la matriz es de tamaño mayor a 1, se realiza la llamada recursiva de la función
        else:
            # Se incluyen los paréntesis según la solución óptima
            return f"({self.print_parenthesis(s, i, s[i][j])} {self.print_parenthesis(s, s[i][j]+1, j)})"

    def matrix_parenthesis(self, p: list) -> tuple:
        # Se calcula el número de matrices a multiplicar
        n = len(p) - 1

        # Inicialización de la tabla de valores mínimos y de la tabla de la solución óptima
        # m[i][j] guarda el número mínimo de multiplicaciones escalares necesarias
        # para multiplicar la sucesión de matrices desde la matriz i hasta la matriz j
        m = [[float("inf") for j in range(n)] for i in range(n)]

        # s[i][j] guarda el índice del último paréntesis abierto en la solución óptima
        s = [[0 for j in range(n)] for i in range(n)]

        # Los valores de la diagonal de la tabla de valores mínimos se inicializan en cero
        for i in range(n):
            m[i][i] = 0

        # Llenado de la tabla de valores mínimos y de la tabla de la solución óptima
        # _len representa la longitud de la cadena de matrices a considerar
        for _len in range(2, n + 1):
            # Se consideran todas las posibles subcadenas de longitud _len
            for i in range(n - _len + 1):
                j = i + _len - 1
                # Se calcula la solución óptima para cada subcadena considerada

                for k in range(i, j):
                    # Se calcula el número de multiplicaciones escalares necesarias
                    # para multiplicar la sucesión de matrices desde la matriz i hasta la matriz j
                    q = m[i][k] + m[k + 1][j] + p[i] * p[k + 1] * p[j + 1]

                    # Si el número de multiplicaciones escalares calculado es menor
                    # que el número mínimo anterior, se actualiza el valor mínimo y
                    # se guarda el índice del último paréntesis abierto
                    if q < m[i][j]:
                        m[i][j] = q
                        s[i][j] = k

        # Se devuelve el número mínimo de multiplicaciones escalares necesarias y
        # la solución óptima en forma de cadena de paréntesis
        return m[0][n - 1], self.print_parenthesis(s, 0, n - 1)


P = [5, 10, 3, 12, 5, 50, 6]

mp = MatrixParenthesis()
print(mp.matrix_parenthesis(P))
