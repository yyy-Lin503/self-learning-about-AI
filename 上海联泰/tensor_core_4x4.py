# 对照 Tensor Core：一次算完 4×4 小块
# 数字和图里的 A、B、D 相同。先手算 D[0][1]，再跑脚本对答案。

A = [
    [1, 2, 3, 4],
    [0, 1, 0, 1],
    [2, 0, 1, 0],
    [1, 1, 1, 1],
]

B = [
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 1, 0],
    [0, 1, 0, 1],
]


def matmul_4x4(A, B):
    D = []
    for i in range(4):          # D 的第几行
        row = []
        for j in range(4):      # D 的第几列
            total = 0
            for k in range(4):  # 一行和一列，四个位置对乘再相加
                total = total + A[i][k] * B[k][j]
            row.append(total)
        D.append(row)
    return D


if __name__ == "__main__":
    D = matmul_4x4(A, B)
    print("D = A × B")
    for row in D:
        print("  ", row)
    print()
    print("只看 D[0][1]：A 的第 0 行 · B 的第 1 列")
    print("  A[0] =", A[0])
    print("  B的第1列 =", [B[k][1] for k in range(4)])
    print("  四个乘积：")
    total = 0
    for k in range(4):
        prod = A[0][k] * B[k][1]
        total = total + prod
        print(f"    k={k}: {A[0][k]} × {B[k][1]} = {prod}")
    print("  合计 =", total)
