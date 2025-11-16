
A = [1, 2, 3, 4, 5]
n = len(A)

def input_relation_matrix(n):
    matrix = []
    print(f"{n}×{n} 관계 행렬을 행 단위로 입력하세요 (0/1, 공백 구분):")
    for _ in range(n):
        row = list(map(int, input().split()))
        matrix.append(row)
    return matrix

def print_matrix(mat):
    for row in mat:
        print(row)
    print()

def print_relation(matrix, A):
    print("관계 R에 포함된 순서쌍:")
    size = len(matrix)
    for i in range(size):
        for j in range(size):
            if matrix[i][j] == 1:
                print(f"({A[i]}, {A[j]})", end=" ")
    print("\n")


def is_reflexive(matrix):
    size = len(matrix)
    for i in range(size):
        if matrix[i][i] != 1:
            return False
    return True

def is_symmetric(matrix):
    size = len(matrix)
    for i in range(size):
        for j in range(size):
            if matrix[i][j] == 1 and matrix[j][i] != 1:
                return False
    return True

def is_transitive(matrix):
    size = len(matrix)
    for i in range(size):
        for j in range(size):
            if matrix[i][j] == 1:
                for k in range(size):
                    if matrix[j][k] == 1 and matrix[i][k] == 0:
                        return False
    return True

def is_equivalence(matrix):
    r = is_reflexive(matrix)
    s = is_symmetric(matrix)
    t = is_transitive(matrix)

    print("반사 관계:", "O" if r else "X")
    print("대칭 관계:", "O" if s else "X")
    print("추이 관계:", "O" if t else "X")
    print()

    return r and s and t

# ---------- ★ 추가 기능: 위반 지점 설명 ----------

def explain_properties(matrix, A):
    size = len(matrix)
    has_issue = False

    reflexive_viol = []
    for i in range(size):
        if matrix[i][i] != 1:
            reflexive_viol.append((A[i], A[i]))
    if reflexive_viol:
        has_issue = True
        print("반사 위반 지점:", end=" ")
        for a, b in reflexive_viol:
            print(f"({a},{b})", end=" ")
        print()

    symmetric_viol = []
    for i in range(size):
        for j in range(size):
            if matrix[i][j] == 1 and matrix[j][i] == 0:
                symmetric_viol.append((A[i], A[j]))
    if symmetric_viol:
        has_issue = True
        print("대칭 위반 지점: (i,j)는 있는데 (j,i)는 없음 ->", end=" ")
        for a, b in symmetric_viol:
            print(f"({a},{b})", end=" ")
        print()

    transitive_viol = []
    for i in range(size):
        for j in range(size):
            if matrix[i][j] == 1:
                for k in range(size):
                    if matrix[j][k] == 1 and matrix[i][k] == 0:
                        transitive_viol.append((A[i], A[j], A[k]))
    if transitive_viol:
        has_issue = True
        print("추이 위반 지점: i→j, j→k 는 있는데 i→k 없음 ->", end=" ")
        for a, b, c in transitive_viol:
            print(f"({a}→{b}→{c})", end=" ")
        print()

    if not has_issue:
        print("위반 지점이 없습니다. (이미 동치 관계입니다.)")
    print()

def equivalence_class(matrix, A, idx):
    cls = []
    size = len(A)
    for j in range(size):
        if matrix[idx][j] == 1 and matrix[j][idx] == 1:
            cls.append(A[j])
    return cls

def print_equivalence_classes(matrix, A):
    print("각 원소에 대한 동치류:")
    for i in range(len(A)):
        cls = equivalence_class(matrix, A, i)
        print(f"[{A[i]}] = {{", end="")
        print(", ".join(map(str, cls)), end="")
        print("}")
    print()

def reflexive_closure(matrix):
    size = len(matrix)
    new = [row[:] for row in matrix]
    for i in range(size):
        new[i][i] = 1
    return new

def symmetric_closure(matrix):
    size = len(matrix)
    new = [row[:] for row in matrix]
    for i in range(size):
        for j in range(size):
            if new[i][j] == 1 or new[j][i] == 1:
                new[i][j] = 1
                new[j][i] = 1
    return new

def transitive_closure(matrix):
    size = len(matrix)
    new = [row[:] for row in matrix]
    for k in range(size):
        for i in range(size):
            for j in range(size):
                if new[i][j] == 0 and new[i][k] == 1 and new[k][j] == 1:
                    new[i][j] = 1
    return new

def equivalence_closure(matrix):
    r = reflexive_closure(matrix)
    s = symmetric_closure(r)
    t = transitive_closure(s)
    return t


def main():
    matrix = input_relation_matrix(n)

    print("\n입력된 관계 행렬:")
    print_matrix(matrix)
    print_relation(matrix, A)

    print("▶ 원래 관계의 성질 판별")
    eq = is_equivalence(matrix)

    if eq:
        print("이 관계는 동치 관계입니다.\n")
        print_equivalence_classes(matrix, A)
        return
    print("이 관계는 동치 관계가 아닙니다.\n")
    explain_properties(matrix, A)
    print("▶ 반사 폐포 전 / 후")
    print("전:")
    print_matrix(matrix)
    r_closure = reflexive_closure(matrix)
    print("후(반사 폐포):")
    print_matrix(r_closure)
    if is_equivalence(r_closure):
        print("반사 폐포 후 동치 관계입니다.")
        print_equivalence_classes(r_closure, A)
    print("▶ 대칭 폐포 전 / 후")
    print("전:")
    print_matrix(matrix)
    s_closure = symmetric_closure(matrix)
    print("후(대칭 폐포):")
    print_matrix(s_closure)
    if is_equivalence(s_closure):
        print("대칭 폐포 후 동치 관계입니다.")
        print_equivalence_classes(s_closure, A)
    print("▶ 추이 폐포 전 / 후")
    print("전:")
    print_matrix(matrix)
    t_closure = transitive_closure(matrix)
    print("후(추이 폐포):")
    print_matrix(t_closure)
    if is_equivalence(t_closure):
        print("추이 폐포 후 동치 관계입니다.")
        print_equivalence_classes(t_closure, A)
    print("▶ 반사·대칭·추이 폐포를 모두 적용한 최종 관계")
    final = equivalence_closure(matrix)
    print_matrix(final)
    if is_equivalence(final):
        print("최종 관계는 동치 관계입니다.")
        print_equivalence_classes(final, A)
    else:
        print("모든 폐포를 적용해도 동치 관계가 되지 않았습니다.")

if __name__ == "__main__":
    main()
