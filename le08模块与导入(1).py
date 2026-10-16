"""
第 08 课：模块与导入 import（demo 每个文件开头那一堆 import 是什么）
运行：~/miniconda3/envs/py312/bin/python 08_模块与导入.py

C/C++ 对比：
  - import 模块  ≈ #include，但更智能（不会重复包含，自带命名空间）
  - 一个 .py 文件 = 一个「模块」，一个带 __init__.py 的文件夹 = 一个「包」
  - 不用写 .h 头文件，不用 Makefile 声明，import 谁就用谁

  模块就是一个py文件，类就是说这个py文件里面的class,方法就是这个class下面的def定义的
  包是要这个文件夹里面有 __init__.py 的文件
"""

# ============ 1. 三种 import 写法 ============

# 写法一：import 整个模块，用的时候带模块名前缀
import math                      # ≈ #include <cmath>
print(math.sqrt(16))             # 用 math 里的东西要写 math.  （像命名空间 math::）
print(math.pi)

# 写法二：from 模块 import 具体的东西，用时不带前缀（demo 最常用这种）
from math import sqrt, pi        # 只把 sqrt 和 pi 拿进来
print(sqrt(25))                  # 直接用，不写 math.
print(pi)

# 写法三：import ... as ... 起别名（数据分析库常见，如 import numpy as np）
import datetime as dt
print(dt.date.today())           # 用别名 dt 代替长名字 datetime

# ============ 2. 看懂 demo 里的 import ============
# demo 的 agent_core.py 开头是这样的，逐行解释：

# from __future__ import annotations
#   ↑ 这是个「未来特性开关」，让类型注解写起来更方便。看到它忽略即可，不影响理解。

# from datetime import timedelta
#   ↑ 从标准库 datetime 里，只拿 timedelta（时间差）这个类。timedelta(seconds=60)=60秒

# import re
#   ↑ 导入正则表达式模块（第11课讲）

# from typing import Any
#   ↑ 从 typing 拿 Any（“任意类型”，第06课讲过）

# from app.data.icd import find_parameter_by_text, get_icd_by_name
#   ↑ 关键！这是「导入项目自己的代码」。
#     app.data.icd 的意思是：app 文件夹 / data 文件夹 / icd.py 文件    这个是python路径
#     用「点 .」表示文件夹层级（C++ 用斜杠 / 写路径，Python import 用点）
#之前的math、datetime、re、typing都是python自带的标准库，icd.py是自己写的文件，所以要地址
#     从那个 icd.py 里，拿出 find_parameter_by_text 和 get_icd_by_name 两个函数

# from app.services.telemetry_store import store
#   ↑ 从 app/services/telemetry_store.py 里，拿出名为 store 的东西（一个对象）

print("已演示标准库导入")

# ============ 3. 包 package：带 __init__.py 的文件夹 ============
# demo 里 app/ app/data/ app/services/ 每个文件夹都有一个空的 __init__.py 文件。
# 这个文件的作用就是「告诉 Python：这个文件夹是一个包，可以被 import」。
# 内容常常是空的，但必须存在（旧规矩）。
# 所以 app.services.telemetry_store 能 import，是因为：
#   app/ 有 __init__.py，app/services/ 有 __init__.py，telemetry_store.py 在里面。

# ============ 4. if __name__ == "__main__": 是什么 ============
# 你会在很多 .py 末尾看到这句。意思是：
#   「只有当这个文件被直接运行时，才执行下面的代码；
#     如果它是被别的文件 import 进去的，下面就不执行。」
# 相当于 C/C++ 的 main()，但更灵活：一个文件既能当程序跑，又能当库被导入。
def main():
    print("我是主程序逻辑")

# main()  # 直接运行时，执行 main()。被导入时，这里执行,下面的main不执行，而且记得保存本文件再运行。
if __name__ == "__main__":      # __name__ 是 Python 自动设的特殊变量
    main()                      # 直接 python 08_xxx.py 运行时，这里会执行

print("\n==== 小结 ====")
print("import math（带前缀用 math.）；from math import sqrt（直接用）；import x as y（别名）")
print("from app.data.icd import f  =  从 app/data/icd.py 拿 f；点.表示文件夹层级")
print("文件夹里的 __init__.py 让它成为可导入的「包」")
print('if __name__=="__main__": 直接运行才执行，被导入时不执行（类似 main）')
