"""
第 04 课：控制流 if/for/while + 列表推导式
运行：~/miniconda3/envs/py312/bin/python 04_控制流与推导式.py

C/C++ 对比：
  - 条件不用括号()，但要冒号: 和缩进
  - for 是 "for x in 集合"，不是 "for(i=0;i<n;i++)"
  - 用 and/or/not，不用 &&/||/!
  - 列表推导式：一行生成列表，C++ 没有对应语法
"""

# ============ 1. if / elif / else ============
score = 75
if score >= 90:
    print("优秀")
elif score >= 60:          # C 里是 else if，Python 是 elif
    print("及格")
else:
    print("不及格")

# 条件运算符（逻辑）：用英文单词
age = 20
if age >= 18 and age < 65:        # C: age>=18 && age<65
    print("成年人")
if not (age < 18):                # C: !(age<18)
    print("不是未成年")

# Python 特有：链式比较（C 不行）
if 18 <= age <= 65:
    print("适龄")

# 三元表达式：值 = A if 条件 else B（C 是 条件 ? A : B）
status = "成年" if age >= 18 else "未成年"
print(status)

# ============ 2. for 循环：遍历集合，不是计数 ============
# 要像 C 那样数 0~4，用 range
for i in range(5):          # 0,1,2,3,4（不含 5）
    print("i =", i, end=" ")  #print输出后会自动换行，end=" "让它不换行，改成空格
print()                         #单独换行

for i in range(2, 10, 2):   # 从2到10，步长2 → 2,4,6,8
    print(i, end=" ")
print()

# 直接遍历元素（最常用）
params = ["气压高度", "液压压力", "卫星高度"]
for p in params:
    print("参数:", p)

# ============ 3. while ============
n = 3
while n > 0:
    print("倒数:", n)
    n -= 1

# break / continue 和 C 一样
for i in range(10):
    if i == 3:
        continue       # 跳过这次
    if i == 6:
        break          # 跳出循环
    print("值:", i, end=" ")
print()

# ============ 4. 列表推导式（Python 精华，demo 里常见）============
# 需求：把每个数平方。C 要写循环 + push_back，Python 一行：
nums = [1, 2, 3, 4]
squares = [x * x for x in nums]#列表推导式长这样
print(squares)                       # [1, 4, 9, 16]
# for x in nums:
#     print(x * x,end=" ")
# print()输出的是不带[]的1 4 9 16，上面没有注释的squares输出的是带[]的[1, 4, 9, 16]

# 带条件：只要偶数的平方
even_sq = [x * x for x in nums if x % 2 == 0]
print(even_sq)                       # [4, 16]

# 等价的传统写法（对照理解）：
result = []#创建一个空列表，准备后面往里面装东西。
for x in nums:
    if x % 2 == 0:
        result.append(x * x)
print(result)                        # 一样 [4, 16]

# 字典推导式（生成 dict）
name_len = {name: len(name) for name in params}
print(name_len)

print("\n==== 小结 ====")
print("elif/and/or/not；for x in 集合；range()计数；[x*x for x in 列表 if 条件] 一行生成")
