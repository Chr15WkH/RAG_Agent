import numpy as np
'''
计算两个向量的余弦相似度（衡量方向相似性，忽略长度影响）

参数：
    vec_a (np.array): 向量A
    vec_b (np.array): 向量B

返回：
    float: 余弦相似度结果（范围[-1, 1]，越接近1方向越一致）

公式：
    cos_sim = (vec_a · vec_b) / (||vec_a|| × ||vec_b||)

详解：
    1. 点积：vec_a · vec_b = vec_a[0]×vec_b[0] + vec_a[1]×vec_b[1] + ... + vec_a[n]×vec_b[n]
    2. 模长：||vec_a|| = √(vec_a[0]^2 + vec_a[1]^2 + ... + vec_a[n]^2)
    3. 模长：||vec_b|| = √(vec_b[0]^2 + vec_b[1]^2 + ... + vec_b[n]^2)

A: [0.5, 0.5]
B: [0.7, 0.7]
C: [0.7, 0.5]
D: [-0.6, -0.5]
'''

def get_dot(vec_a, vec_b):
    """计算两个向量的点积,两个同纬度向量数字乘积之和"""
    if len(vec_a) != len(vec_b):
        raise ValueError("两向量维度必须一致")
    
    dot_sum = 0
    for a, b in zip(vec_a, vec_b):
        dot_sum += a * b
        
    return dot_sum

def get_norm(vec):
    """计算单个向量的模长，对向量的每个数字求平方，计算平方和再开根号"""
    sum_squares = 0
    for v in vec:
        sum_squares += v ** 2
    return np.sqrt(sum_squares)

def Cosine_Similarity(vec_a, vec_b):
    """余弦相似度计算：两向量点积除以两向量模长的乘积"""
    return get_dot(vec_a, vec_b) / (get_norm(vec_a) * get_norm(vec_b))

if __name__ == '__main__':
    A = [0.5, 0.5]
    B = [0.7, 0.7]
    C = [0.7, 0.5]
    D = [-0.6, -0.5]
    print("AB的余弦相似度为:",Cosine_Similarity(A, B))
    print("AC的余弦相似度为:",Cosine_Similarity(A, C))
    print("AD的余弦相似度为:",Cosine_Similarity(A, D))
