"""
第 06 课：类型注解（★看懂 demo 的关键！demo 里 str | None、list[Any] 满天飞）
运行：~/miniconda3/envs/py312/bin/python 06_类型注解.py

核心观念（和 C/C++ 最大的不同）：
  Python 的类型注解「只是给人看和给工具检查的提示」，运行时不强制！
  你写 age: int = 5，然后 age = "字符串" 也照样能跑，不会报错。
  C/C++ 的类型是「强制的」，Python 的注解是「建议的」。
  —— 但 demo 用了 pydantic（第12课），它会把注解变成「真的强制校验」。
"""

# ============ 1. 变量注解：变量名: 类型 ============
age: int = 18              # 读作「age 是 int，值 18」。C: int age = 18;
name: str = "张三"          # str = 字符串
height: float = 1.75       # float = 浮点
ok: bool = True            # bool

# 注解不强制，下面这行不会报错（但不建议这么写）：
age = "其实我变成字符串了"
print(age)                 # 照样打印，Python 不拦你

# ============ 2. 函数注解：参数: 类型，返回值用 -> ============
# C: int add(int a, int b)
def add(a: int, b: int) -> int:
    return a + b
# 读法：a 是 int，b 是 int，箭头 -> 后面 int 是返回类型

print(add(3, 4))

# demo 真实例子：
def parse_window_sec(question: str) -> int:
    """参数 question 是字符串，返回一个 int"""
    return 10
print(parse_window_sec("最近10秒"))

# ============ 3. 容器的类型：list[X]、dict[K, V] ============
#变量名: 容器类型[里面元素的类型] = 值
nums: list[int] = [1, 2, 3]              # 一个装 int 的列表，list这四个单词必须要这么写，不能改成aa
names: list[str] = ["a", "b"]            # 装 str 的列表
person: dict[str, int] = {"age": 18}     # 键是 str，值是 int 的字典。必须是dict才表达词典

# demo 里最常见的返回注解：dict[str, Any]
from typing import Any  #Any是关键字，表示任意类型数据int,float...
def query() -> dict[str, Any]:#这里是中括号
    # dict[str, Any] = 键是字符串str，值是「任意类型」的字典
    # Any 表示「啥类型都行」，因为返回的字典里有字符串、数字、嵌套字典
    #其实不写-> dict[str, Any]也行，只不过写了是告诉人和工具，这个函数返回的是一个字典，键是字符串，值可以是任意类型
    return {"answer": "21 MPa", "value": 21.0, "ok": True}
print(query())

# ============ 4. ★ X | None ：可能是 X，也可能是「空」 ============
# 这是 demo 里出现最多的写法，必须懂！
# None 就是「空值」，相当于 C++ 的 nullptr / NULL。
# str | None 读作「字符串 或者 空」—— 竖线 | 是「或」的意思。

unit: str | None = "MPa"     # 这次有值。这里是让unit默认初始化为字符串"MPa"，表示有值
unit = None                  # 也允许是空。这里是把unit默认初始化为None，表示还没有值

# demo 真实例子（schemas.py 里的字段）：
def find_param(text: str) -> dict | None: #dict后面可以跟着中括号，表示这个字典里面的键值对类型，这里没有写，所以就是任意类型的字典
    """找到了返回字典，找不到返回 None（空）"""
    if "液压" in text:
        return {"name": "hydraulic_pressure"}
    return None              # 没找到，返回空

r = find_param("查液压压力")  #这样后续还能接着用
print(r)                     # {'name': 'hydraulic_pressure'}
r2 = find_param("无关的话")
print(r2)                    # None

# 用 None 的标准判断方式：is None / is not None
if r2 is None:     #== 不能写成 r2 == None，== 是值比较，is 是对象比较，None 是单例对象，必须用 is 判断
    print("没找到参数")      # demo 里 if icd is None: 就是这个

# ============ 5. Literal：只能是这几个固定值之一 ============
from typing import Literal
# 类型是 Literal["ground","onboard"] 表示这个值只能是这两个字符串之一
# demo 里：data_type: Literal["continuous","discrete"]  区分连续量/离散量
def set_endpoint(ep: Literal["ground", "onboard"]) -> str:
    return f"使用 {ep} 端"
print(set_endpoint("ground"))

print("\n==== 小结（demo 高频）====")
print("x: int        变量是整数")
print("def f(q: str) -> int   参数 str，返回 int")
print("dict[str, Any]   键字符串、值任意 的字典（demo 返回值）")
print("str | None       可能是字符串，也可能是空(None)  ← 最常见")
print("None ≈ C++ 的 nullptr；判断用 is None / is not None")