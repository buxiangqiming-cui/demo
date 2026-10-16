"""
第 01 课：基础语法、变量、缩进
运行：~/miniconda3/envs/py312/bin/python 01_基础_变量与语法.py

给 C/C++ 程序员的核心提示：
  1. 没有分号 ;        —— 一行一句，换行就是结束
  2. 没有大括号 {}      —— 用「缩进」表示代码块（通常 4 个空格）
  3. 变量不用声明类型   —— 直接赋值，类型由值决定（动态类型）
  4. 不用 main 函数也能跑 —— 文件从上到下顺序执行
"""

#This is from dev branch. 

# ---- 1. 变量：不用写 int / double / char* ------=
age = 18              # C: int age = 18;
height = 1.755         # C: double height = 1.75;
name = "张三"         # C: const char* name = "张三";  （Python 字符串是对象，能存中文）
is_ok = True          # C: bool is_ok = true;   注意 Python 是 True/False（首字母大写）

# 同一个变量可以换类型（C/C++ 不允许，Python 可以）
x = 10
x = "现在我是字符串"   # 合法！x 重新绑定到一个字符串对象
print("x 现在是:", x)

# ---- 2. print 就是输出，自动换行、自动加空格 ----
print("姓名:", name, "年龄:", age)   # 多个值用逗号隔开，输出时用空格连接
print("身高:", height, "米")

# ---- 3. 缩进决定代码块（最重要的区别！）----
# C 里：  if (age >= 18) { printf("成年\n"); }
# Python：冒号 + 换行 + 缩进
if age >= 18:
    print("已成年")          # 这一行属于 if，因为它缩进了
    print("可以考驾照")      # 同样缩进，也属于 if
print("这一行不缩进，无论如何都执行")  # 回到顶格，不属于 if

# 缩进错误 = 报错。下面这种在 C 里没事，在 Python 里是语法错误：
# if age >= 18:
# print("没缩进")   # ← IndentationError

# ---- 4. 注释 ----
# 单行注释用 #（C 里是 //）
"""
三个引号是多行字符串，常被当作多行注释用（C 里是 /* ... */）
"""

# ---- 5. 基本运算，和 C 几乎一样，但有两个特别的 ----
print(7 / 2)    # = 3.5   注意！Python 的 / 永远是浮点除法（C 里 7/2=3）
print(7 // 2)   # = 3     // 才是整除（取整）
print(7 % 2)    # = 1     取余，和 C 一样
print(2 ** 10)  # = 1024  ** 是幂运算（C 里要用 pow()）

# ---- 6. 没有 ++ 和 -- ----
count = 0
count += 1      # 可以用 +=（和 C 一样）
# count++       # ← Python 没有 ++，这行会报错
print("count =", count)

print("\n==== 本课小结 ====")
print("Python 靠缩进分块、不用分号大括号、变量不声明类型、/ 是浮点除法")
