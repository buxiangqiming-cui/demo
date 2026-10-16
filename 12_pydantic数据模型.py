"""
第 12 课：pydantic 数据模型（★看懂 demo 的第二把钥匙，对应 schemas.py 全部）
运行：~/miniconda3/envs/py312/bin/python 12_pydantic数据模型.py

pydantic 是什么、为什么 demo 到处用它：
  Web 后端要收发数据（浏览器发来一个 JSON，后端要回一个 JSON）。
  pydantic 让你「用一个 class 定义数据长什么样」，然后它自动帮你：
    1. 校验：收到的数据类型不对/缺字段，自动报错（不用你手写 if 检查）
    2. 转换：字符串 "18" 自动转成 int 18
    3. 文档：自动生成接口文档
  你可以把 pydantic 的 class 理解成「带自动校验的 C 结构体 struct」。

  第06课的「类型注解」在这里从「建议」变成了「强制」——这就是 pydantic 的核心作用。
"""

# pydantic 是第三方库，demo 已经装了。从它导入两样东西：
from pydantic import BaseModel, Field
#   BaseModel = 所有数据模型的「父类」，你的模型都要继承它
#   Field     = 用来给字段加「详细规则」（默认值、范围、说明等）

# ============ 1. 最简单的模型：像定义一个 struct ============
# C:  struct Point { int x; int y; };
class Point(BaseModel):  # 写了括号表示继承，继承 BaseModel（括号里写父类，这是 Python 继承语法）
    x: int                    # 字段 x，类型 int —— 这里的类型注解是「强制」的！因为BaseModel他是强制检查的
    y: int                    # 字段 y，类型 int,也是强制的
#上面这个定义的Point这个类由于继承了BaseModel，所以它就有了pydantic的功能：自动校验、转换、文档等
#必须要有两个字段 x 和 y，类型必须是 int，否则会报错。

# 创建实例：用「字段名=值」传入
p = Point(x=3, y=4) #令p=一个类，所以p就是这个类的对象
print(p)            # x=3 y=4
print(p.x, p.y)     # 像访问成员变量一样 = 3 4

# ★ 自动校验演示：类型不对会怎样
p2 = Point(x="5", y=4)        # x 传的是字符串 "5"
print("字符串'5'被自动转成:", p2.x, type(p2.x))   # pydantic 自动转成 int 5.在print里面逗号表示在各个之间加空格，然后顺序输出

# 缺字段 / 类型彻底不对会抛错（这就是「强制校验」）：
try:
    Point(x="不是数字", y=4)   # "不是数字" 没法转成 int
except Exception as e:
    print("校验失败，pydantic 自动报错（节选）:", str(e)[:60], "...")

# ============ 2. 默认值 + Field（demo 大量用这个）============
class DetectAnomalyRequest(BaseModel):
    # 字段: 类型 = 默认值
    parameter: str = "hydraulic_pressure"     # 不传就用这个默认值（液压压力）
    # Field 给字段加更多规则：
    #   default=10  默认值
    #   ge=1        >= 1（ge = greater or equal，大于等于）
    #   le=300      <= 300（le = less or equal）
    #   description 给人看的说明，会进接口文档
    window_sec: int = Field(default=10, ge=1, le=300, description="检测最近多少秒")

r = DetectAnomalyRequest()                 # 全用默认
print(r.parameter, r.window_sec)           # hydraulic_pressure 10

r = DetectAnomalyRequest(window_sec=30)    # 改其中一个
print(r.window_sec)                        # 30

# ★ 范围校验演示：window_sec 限定 1~300，传 999 会报错
try:
    DetectAnomalyRequest(window_sec=999)   # 超过 le=300
except Exception as e:
    print("超范围被拦下:", str(e)[:50], "...")

# ============ 3. 逐行读懂 demo 的 schemas.py 字段 ============
# demo 里有这样一段（ICDItem，描述一个飞行参数的定义）：
from typing import Any, Literal

class ICDItem(BaseModel):
    name: str = Field(..., description="参数英文名")
    #   ↑ 注意这个 ...（三个点，叫 Ellipsis）。在 Field 里它表示「必填，没有默认值」。
    #     所以 name 是必须传的字符串。

    cn_name: str = Field(..., description="参数中文名")     # 必填，中文名

    period_ms: float = Field(..., description="采样周期 ms")  # 必填，浮点

    data_type: Literal["continuous", "discrete"] = Field(..., description="连续量或离散量")
    #   ↑ Literal[...]（第06课）：data_type 只能是 "continuous" 或 "discrete"，传别的会报错

    unit: str | None = Field(default=None, description="单位")
    #   ↑ str | None（第06课）：可以是字符串，也可以是 None（没单位）。默认 None。

    normal_min: float | None = Field(default=None, description="正常最小值")
    normal_max: float | None = Field(default=None, description="正常最大值")
    #   ↑ 这两个：正常范围的上下限，可能没有（None）

    normal_values: list[Any] | None = Field(default=None, description="离散量正常取值")
    #   ↑ list[Any] | None：可能是「一个任意类型的列表」，也可能是 None

    description: str = ""        # 普通默认值写法（不用 Field 也行），默认空字符串

# 创建一个飞参定义试试
item = ICDItem(
    name="hydraulic_pressure",
    cn_name="液压压力",
    period_ms=100.0,
    data_type="continuous",
    unit="MPa",
    normal_min=20.0,
    normal_max=22.0,
)
print(item.cn_name, item.normal_min, "~", item.normal_max, item.unit)

# 转成字典 / JSON（后端回给浏览器时就是这么干的）
print(item.model_dump())          # 转成 Python 字典
print(item.model_dump_json()[:80], "...")   # 转成 JSON 字符串

# ============ 4. 三个点 ... 和 None 别搞混 ============
# Field(..., ...) 里的 ...  → 「这个字段必填」
# str | None / default=None → 「这个字段可以是空」
# 两者是不同的事：前者管「必不必填」，后者管「值能不能为空」。

print("\n==== 小结（看懂 schemas.py 全靠这些）====")
print("class X(BaseModel): 定义带自动校验的数据结构（≈带校验的 struct）")
print("字段名: 类型 = 默认值；类型注解在这里是「强制」的，类型不对自动报错")
print("Field(..., description=...)：... 表示必填；Field(default=10, ge=1, le=300) 加范围")
print("str | None = 可空；Literal['a','b'] = 只能取这几个值")
print(".model_dump() 转字典，.model_dump_json() 转JSON")
