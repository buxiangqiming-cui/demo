"""
第 02 课：字符串与格式化（重点：f-string，demo 里到处都是）
运行：~/miniconda3/envs/py312/bin/python 02_字符串与格式化.py

C/C++ 对比：
  - Python 字符串是对象，自带很多方法，不用 strcpy/strlen/strcmp
  - 不用 printf 的 %d %s，用更直观的 f-string
"""

name = "液压压力"
value = 21.3
unit = "MPa"

# ---- 1. 字符串基本操作 ----
s = "Hello"
print(len(s))           # 长度 = 5（C: strlen）
print(s + " World")     # 拼接用 +（C: strcat）
print(s * 3)            # 重复 3 次 = HelloHelloHello（C 没有）
print(s[0])             # 取第一个字符 = H（和 C 一样下标从 0）
print(s[-1])            # 取最后一个字符 = o（负数从末尾倒数，C 没有）
print(s[1:4])           # 切片，取下标 1~3 = ell（C 要手动 substr）

# ---- 2. f-string：最常用的格式化（demo 里 f"..." 全是这个）----
# 在字符串前加 f，然后 {变量} 直接嵌进去
msg = f"参数 ：{name} 当前值是 {value} {unit}"
print(msg)
# C 里要写：printf("参数 %s 当前值是 %.1f %s\n", name, value, unit);

# {} 里能放表达式、能控制格式
print(f"两倍是 {value * 2}")
print(f"保留一位小数：{value:.1f}")     # :.1f 就是 C 的 %.1f

# ---- 3. 常用字符串方法（点 . 调用，像 C++ 的 std::string 成员函数）----
text = "  一分钟前的气压高度  "
print(text.strip())              # 去掉两端空格（demo 里常见）
print("hydraulic" in "hydraulic_pressure")   
# 判断左边的是否在右边里面，返回 True（demo 里 if "当前" in question）
print("a.b.c".split("."))        # 按点切成列表 = ['a','b','c']
print("a,b,c".split(","))        # 按逗号切成列表 = ['a','b','c']
print("a,b,c".split("."))        # 按点切成列表，但没有点 = ['a,b,c']
print("气压" in text)            # 中文也能判断包含 = True

# ---- 4. 多行字符串 ----
doc = """这是第一行
这是第二行"""
print(doc)

print("\n==== 小结 ====")#单引号和双引号都可以
print('f"参数{name}值{value}" 是最常用的格式化；in 判断包含；.strip() 去空格')
print(f"参数{name}值{value} 是最常用的格式化；in 判断包含；.strip() 去空格")
#外单内双，或者外双内单都可以，只是为了让字符串里有引号时不冲突，但是会让f的{}变成正常的符号，而不是变量
#如果需要print里面加fstring，那就照着最后一行那样，只对fsting加引号
#因为如果全是单引号或者全是双引号，
#print('f‘参数{name}值{value}’ 是最常用的格式化；in 判断包含；.strip() 去空格')就报错了
#前两个单引号就结束了


