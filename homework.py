def matrixout(mx, size):
    print("┌" + "        " * size + "┐")
    for i in range(size):
        print("|", end=" ")
        for j in range(size):
            print(mx[i][j], end=" ")
        print("|")
    print("└" + "        " * size + "┘")

def input_matrix():
    n = int(input("행렬의 크기 n을 입력하세요: "))
    print(f"{n}×{n} 행렬의 각 행을 입력하세요 (공백으로 구분):")
    A = []
    for i in range(n):
        row = list(map(float, input(f"{i+1}행: ").split()))
        A.append(row)
    return A

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0]*A[1][1] - A[0][1]*A[1][0]
    total = 0
    for c in range(n):
        minor = [row[:c] + row[c+1:] for row in (A[1:])]
        total += ((-1)**c) * A[0][c] * determinant(minor)
    return total

def inverse_by_determinant(A):
    n = len(A)
    detA = determinant(A)
    if detA == 0:
        print("이 행렬은 역행렬이 존재하지 않습니다.")
        return 0

    cofactors = []
    for i in range(n):
        co_row = []
        for j in range(n):
            sub = [row[:j] + row[j+1:] for row in (A[:i] + A[i+1:])]
            cofactor = ((-1)**(i+j)) * determinant(sub)
            co_row.append(cofactor)
        cofactors.append(co_row)

    adj = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(cofactors[j][i] / detA)
        adj.append(row)
    return adj

def inverse_by_gauss_jordan(A):
    n = len(A)
    B = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(A[i][j])
        for j in range(n):
            if i == j:
                row.append(1.0)
            else:
                row.append(0.0)
        B.append(row)

    for i in range(n):
        # 피벗이 0인 경우, 아래 행 중 0이 아닌 값이 있는 행과 교환
        if B[i][i] == 0:
            for j in range(i + 1, n):
                if B[j][i] != 0:
                    B[i], B[j] = B[j], B[i]
                    break
            else:
                print("이 행렬은 역행렬이 존재하지 않습니다.")
                return 0

        # 현재 행의 기준값으로 나누기
        a = B[i][i]
        for k in range(2 * n):
            B[i][k] = B[i][k] / a

        # 다른 행의 해당 열을 0으로 만들기
        for j in range(n):
            if j != i:
                factor = B[j][i]
                for k in range(2 * n):
                    B[j][k] = B[j][k] - factor * B[i][k]

    inverse = []
    for i in range(n):
        inverse.append(B[i][n:])
    return inverse

def multiply_matrix(A, B):
    n = len(A)
    result = []
    for i in range(n):
        row = []
        for j in range(n):
            s = 0
            for k in range(n):
                s += A[i][k] * B[k][j]
            row.append(s)
        result.append(row)
    return result

def same_matrix(M1, M2):
    n = len(M1)
    for i in range(n):
        for j in range(n):
            if abs(M1[i][j] - M2[i][j]) > 0.000001:
                return 0
    return 1


def main():
    A = input_matrix()
    n = len(A)

    inv1 = inverse_by_determinant(A)
    if inv1:
        print("\n행렬식 기반 역행렬")
        matrixout(inv1, n)

    inv2 = inverse_by_gauss_jordan(A)
    if inv2:
        print("\n가우스-조던 소거법 기반 역행렬")
        matrixout(inv2, n)

    if inv1 and inv2:
        if same_matrix(inv1, inv2):
            print("\n두 방법의 역행렬 결과가 같습니다.")
        else:
            print("\n두 방법의 역행렬 결과가 다릅니다.")

    if inv2:
        product = multiply_matrix(A, inv2)
        print("\nA × A⁻¹ 결과")
        matrixout(product, n)

        identity = 1
        for i in range(n):
            for j in range(n):
                expected = 1
                if i != j:
                    expected = 0
                if abs(product[i][j] - expected) > 0.000001:
                    identity = 0
        if identity:
            print("본 행렬과 역행렬의 곱이 단위행렬입니다.")
        else:
            print("본 행렬과 역행렬의 곱이 단위행렬이 아닙니다.")

main()
