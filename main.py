import math


class Matrice:
    # Constructor for matrix class
    def __init__(self, rows: list, column: list, contents):
        self.rows, self.columns = rows, column
        self.contents = contents
        self.matr_display = Matrice.seq_to_matrice(self.contents)
        # Check if the matrix is
        # well-formed i.e.
        # the rows have the same number of elements
        for x in contents:
            if len(x) != self.columns:
                print("ERROR")
                exit()

    # Sum method
    def matrix_sums(self, matr):
        # Check if the matrices to be added have the same dimensions
        # and sum them
        if matr.rows == self.rows and matr.columns == self.columns:
            sum_of_element = []
            for x in range(self.rows):
                row = [self.contents[x][y] + matr.contents[x][y] for y in range(self.columns)]
                sum_of_element.append(row)
            Matrice.result_print(Matrice.seq_to_matrice(sum_of_element))
        else:
            print("The operation cannot be performed")

    # Constant multiplication method
    def mul_by_constant(self, constant):
        product_matrice = []
        for x in range(self.rows):
            row = [self.contents[x][y] * constant for y in range(self.columns)]
            product_matrice.append(row)
        Matrice.result_print(Matrice.seq_to_matrice(product_matrice))

    # Matrix multiplication method
    def matrix_multiply(self, matr):
        # Checks if the number of columns of the first matrix
        # is equal to the number of rows of the second
        # matrix then performs the calculation
        if self.columns == matr.rows:
            product_of_element = []
            for x in range(self.rows):
                row = []
                for y in range(matr.columns):
                    product = sum(
                        self.contents[x][z] * matr.contents[z][y]
                        for z in range(self.columns)
                    )

                    row.append(product)
                product_of_element.append(row)
            Matrice.result_print(Matrice.seq_to_matrice(product_of_element))
        else:
            print("The operation cannot be performed")

    # This function looks for the sub-matrices obtained by removing the lines i and j
    @staticmethod
    def sub_mat(contents, row, column, i, j):
        minor_matrice = []
        for a in range(row):
            row = [contents[a][b] for b in range(column) if a != i and b != j]
            if row:
                minor_matrice.append(row)
        return minor_matrice

    @staticmethod
    def determinant(matrice):
        if matrice.rows != matrice.columns:
            print('Impossible to determinate the determinant of a non-square matrix')
            return
        det = 0
        # Return the number if the matrix's dimension is 1
        if matrice.rows == 1:
            mat = matrice.contents
            return mat[0][0]
        # Return ab - cd if the dimension is 2
        if matrice.rows == 2:
            mat = matrice.contents
            return (mat[0][0] * mat[1][1]) - (mat[0][1] * mat[1][0])
        # For dimension > 2
        for y in range(matrice.columns):
            n = matrice.rows
            m = matrice.columns
            # We are looking for the n-1 miner associated with the cofactor
            content = Matrice.sub_mat(matrice.contents, n, m, 0, y)
            sub_matrice = Matrice(n - 1, m - 1, content)
            det += math.pow(-1, y) * matrice.contents[0][y] * Matrice.determinant(sub_matrice)
        return det

    @staticmethod
    def inverse(matrice):
        inverse_mat = []
        det = Matrice.determinant(matrice)
        if det == 0:
            return None
        n = matrice.rows
        m = matrice.columns
        for x in range(matrice.rows):
            row = []
            for y in range(matrice.columns):
                # We are looking for the n-1 miner associated with the cofactor
                content = Matrice.sub_mat(matrice.contents, n, m, x, y)
                sub_matrice = Matrice(n - 1, m - 1, content)
                cofactor = (pow(-1, x + y) * Matrice.determinant(sub_matrice)) * (det ** -1)
                row.append(cofactor)
            inverse_mat.append(row)
        inverse_mat = Matrice.matrix_transposition(Matrice(n, m, inverse_mat))
        return inverse_mat

    @staticmethod
    def matrix_transposition(matrice, transposition_type='main'):
        matrix_transpose = []
        if transposition_type == 'main':
            for x in range(matrice.rows):
                row: list = [matrice.contents[y][x] for y in range(matrice.columns)]
                matrix_transpose.append(row)
        elif transposition_type == 'side':
            matrix_transpose = Matrice.matrix_transposition(matrice, 'main')
            matrice.contents = matrix_transpose
            matrix_transpose = Matrice.matrix_transposition(matrice, 'vertical')
            matrice.contents = matrix_transpose
            matrix_transpose = Matrice.matrix_transposition(matrice, 'horizontal')
        elif transposition_type == 'vertical':
            matrix_transpose = [x[::-1] for x in matrice.contents]
        elif transposition_type == 'horizontal':
            matrix_transpose = list(matrice.contents[::-1])
        return matrix_transpose

    # This method allows the entry of
    # the matrix then returns the content in the form of a list
    @staticmethod
    def matrice_former(n, m):
        return [[float(y) for y in input().split()[:m]] for _ in range(n)]

    # This method allows you to switch
    # from a display in the form of a list
    # to a display in the form of a matrix.
    @staticmethod
    def seq_to_matrice(sequence):
        sequence = [['{:>10}'.format(str(int(x))) if x.is_integer()
                     else '{:>10}'.format(str(x)) for x in y] for y in sequence]
        matrice = [' '.join(x) for x in sequence]
        matrice = '\n'.join(matrice)
        return matrice

    @staticmethod
    def result_print(answer):
        print(f'The result is:\n{answer}')

    @staticmethod
    def matrix_entry(position=''):
        n, m = [int(x) for x in input(f'Enter size of {position} matrix (n m): ').split()]
        print(f'Enter {position} matrix (each line is a row and each element separated by space): ')
        return Matrice(n, m, Matrice.matrice_former(n, m))

    @staticmethod
    def menu():
        while True:
            print('1. Add Matrices')
            print('2. Multiply matrix by a constant')
            print('3. Multiply matrices')
            print('4. Transpose matrix')
            print('5. Calculate a determinant')
            print('6. Inverse matrix')
            print('0. Exit')
            choice = input("Your choice: ")
            if choice == '0':
                exit()
            elif choice == '1':
                mat_a = Matrice.matrix_entry('first')
                mat_b = Matrice.matrix_entry('second')
                mat_a.matrix_sums(mat_b)
            elif choice == '2':
                mat_a = Matrice.matrix_entry()
                c = float(input("Enter constant:"))
                mat_a.mul_by_constant(c)
            elif choice == '3':
                mat_a = Matrice.matrix_entry('first')
                mat_b = Matrice.matrix_entry('second')
                mat_a.matrix_multiply(mat_b)
            elif choice == '4':
                print('1. Main diagonal')
                print('2. Side diagonal')
                print('3. Vertical line')
                print('4. Horizontal line')
                choice = input("Your choice: ")
                if choice == '1':
                    transposition_type = 'main'
                elif choice == '2':
                    transposition_type = 'side'
                elif choice == '3':
                    transposition_type = 'vertical'
                elif choice == '4':
                    transposition_type = 'horizontal'
                else:
                    break
                mat_a = Matrice.matrix_entry()
                matrix_transpose = mat_a.matrix_transposition(mat_a, transposition_type)
                Matrice.result_print(Matrice.seq_to_matrice(matrix_transpose))
            elif choice == '5':
                mat_a = Matrice.matrix_entry()
                Matrice.result_print(Matrice.determinant(mat_a))
            elif choice == '6':
                mat_a = Matrice.matrix_entry()
                if Matrice.inverse(mat_a) is None:
                    print("This Matrix doesn't have an inverse")
                    continue
                Matrice.result_print(Matrice.seq_to_matrice(Matrice.inverse(mat_a)))
            else:
                print('Error Please Retry')


Matrice.menu()
