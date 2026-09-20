# 极简单头注意力（纯 Python，不依赖 numpy）
# Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V
#
# 三个 token：小明、小红、她
# 向量只有 2 维，方便和手算对照。

import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ---------- 输入：已经从嵌入变出来的 Q / K / V ----------
# 每一行是一个 token 的向量。


Q = [
    [0.2, 0.1],  # 小明 在找什么
    [0.3, 0.2],  # 小红 在找什么
    [2.0, 0.0],  # 她   在找「女性人名」这一侧
]

K = [
    [0.3, 0.0],  # 小明：男性人名
    [2.0, 0.0],  # 小红：女性人名 —— 和「她」的 Q 同向
    [-0.5, 1.0],  # 苹果：物品
]

V = [
    [1.0, 0.0],  # 匹配到小明时，注入的内容
    [0.0, 1.0],  # 匹配到小红时，注入的内容
    [0.0, 0.0],  # 匹配到苹果时，几乎没有内容
]

# 行 = 谁在问（Q）：小明、小红、她
# 列 = 被问的人（K/V）：小明、小红、苹果
ROW_NAMES = ["小明", "小红", "她"]
COL_NAMES = ["小明", "小红", "苹果"]

#点积
def dot(a, b):
    total=0
    for x,y in zip(a,b):         #zip(a, b)：把两个列表一对一对牵起来
        total= total + x*y
    return total

#每个词问遍所有词
def attention_scores(Q, K):
    scores = []
    for q in Q:          # 每一个「我在找什么」
        row = []
        for k in K:      # 去问每一个「你是什么」
            row.append(dot(q, k))
        scores.append(row)
    return scores

def softmax(row):
    # 先减最大值，避免 exp 爆掉；不改变谁大谁小。
    m = max(row)
    exps = [math.exp(x - m) for x in row]
    total = sum(exps)
    return [e / total for e in exps]


def weighted_sum(weights, V):
    """按注意力权重混合每一行 V。"""
    dim = len(V[0])
    out = [0.0] * dim
    for w, v in zip(weights, V):
        for d in range(dim):
            out[d] += w * v[d]
    return out

#总函数
def scaled_dot_product_attention(Q, K, V):
    d_k = len(K[0])
    scale = math.sqrt(d_k)
    raw = attention_scores(Q, K)
    scaled = [[x / scale for x in row] for row in raw]
    weights = [softmax(row) for row in scaled]
    output = [weighted_sum(w, V) for w in weights]
    return raw, scaled, weights, output


def fmt(row):
    return "  ".join(f"{x:7.3f}" for x in row)


if __name__ == "__main__":
    raw, scaled, weights, output = scaled_dot_product_attention(Q, K, V)
    d_k = len(K[0])

    print(f"d_k = {d_k}，缩放除以 sqrt(d_k) = {math.sqrt(d_k):.3f}")
    print()
    print("1) 原始分数  Q · K")
    print("         ", "  ".join(f"{n:>7}" for n in COL_NAMES))
    for name, row in zip(ROW_NAMES, raw):
        print(f"  {name}  {fmt(row)}")

    print()
    print("2) 缩放后    分数 / sqrt(d_k)")
    print("         ", "  ".join(f"{n:>7}" for n in COL_NAMES))
    for name, row in zip(ROW_NAMES, scaled):
        print(f"  {name}  {fmt(row)}")

    print()
    print("3) Softmax 权重（每行加起来 = 1）")
    print("         ", "  ".join(f"{n:>7}" for n in COL_NAMES))
    for name, row in zip(ROW_NAMES, weights):
        print(f"  {name}  {fmt(row)}")

    print()
    print("4) 输出 = 权重 × V")
    for name, row in zip(ROW_NAMES, output):
        print(f"  {name}  {fmt(row)}")

    print()
    print("看「她」那一行：权重最大的应该是「小红」，")
    print("所以「她」的输出会更靠近 小红 的 V = [0, 1]。")
