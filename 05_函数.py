"""
第 05 课：函数 def
运行：~/miniconda3/envs/py312/bin/python 05_函数.py

C/C++ 对比：
  - 用 def 定义，不写返回类型（可选注解，见第06课）
  - 不用声明参数类型
  - 能有「默认参数」「关键字参数」「返回多个值」
"""

# ============ 1. 最简单的函数 ============
# C: int add(int a, int b) { return a + b; }
def add(a, b):
    return a + b

print(add(3, 5))            # 8
print(add("你", "好"))      # 你好（字符串也能加，动态类型的威力）

# ============ 2. 默认参数（demo 里非常常见）============
# 调用时不传就用默认值。C++ 也有默认参数，类似。
def greet(name, greeting="你好"):#第二个参数greeting有默认值"你好"，如果调用时不传，就用这个默认值
    return f"{greeting}, {name}"

print(greet("张三"))                 # 你好, 张三
print(greet("张三", "早上好"))       # 早上好, 张三

# demo 真实例子：window_sec 默认 10
def detect_anomaly(parameter="hydraulic_pressure", window_sec=10):
    return f"检测 {parameter}，最近 {window_sec} 秒"

print(detect_anomaly())                  # 全用默认
print(detect_anomaly("altitude"))        # 只改第一个，双引号是因为这是字符，下一行30是数字，不用双引号
print(detect_anomaly(window_sec=30))     # 关键字参数：直接点名要改哪个！这个不加双引号
# ☆ 关键字参数：调用时写 参数名=值，可跳过前面的、顺序随意。C++ 没有这个。
print(detect_anomaly(window_sec=5, parameter="speed"))

# ============ 3. 返回多个值（其实是返回元组）============
def min_max(data):
    return min(data), max(data)

lo, hi = min_max([4, 1, 9])     # 拆包接收
print(f"min={lo}, max={hi}")

# ============ 4. 函数也是值，可以传递（C 的函数指针，但更简单）============
def apply(func, x):
    return func(x)              # 把传进来的函数拿来调用

def square(n):
    return n * n

print(apply(square, 6))         # 把 square 当参数传进去 = 36

# ============ 5. *args 和 **kwargs（demo/库里常见，先认识）============
# *args：收集任意多个「位置参数」成一个元组
def total(*nums):
    return sum(nums)
print(total(1, 2, 3, 4))        # 10

# **kwargs：收集任意多个「关键字参数」成一个字典
def show(**info):
    for k, v in info.items():
        print(f"  {k} = {v}")
show(name="张三", age=18)       # 传进去变成字典 {'name':'张三','age':18}
#**只能接收 名字=值 形式的参数

print("\n==== 小结 ====")
print("def 定义；默认参数 greeting='你好'；关键字参数 window_sec=30；return a,b 返回多值")
