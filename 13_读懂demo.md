# 第 13 课：逐行读懂你的 demo-v2.0 真实代码

学完 01~12 课，现在用学到的知识，逐行读你项目里**真实存在**的代码。
读之前建议先把 01~12 跑一遍。下面每段代码都是从你的 `~/桌面/demo-v2.0/backend/pi_agent/` 里原样摘出来的。

---

## 一、config.py —— 读配置（对应第 06、07、09 课）

文件：`backend/pi_agent/app/config.py`

```python
from __future__ import annotations                          # ① 未来特性开关，忽略即可

from pydantic_settings import BaseSettings, SettingsConfigDict  # ② 导入配置基类（第08课 import）

class Settings(BaseSettings):                               # ③ 定义配置类，继承 BaseSettings（第07课 class）
    model_config = SettingsConfigDict(                      # ④ 告诉它去哪读配置
        env_file=".env",                                    #    读 .env 文件
        env_file_encoding="utf-8",
        extra="ignore",                                     #    多余的配置项忽略
    )

    dashscope_api_key: str = ""                             # ⑤ 字段：API key，类型 str，默认空字符串（第06课注解）
    qwen_model: str = "qwen-plus"                           #    模型名，默认 qwen-plus
    dashscope_base_url: str = "https://..."                 #    接口地址

    @property                                               # ⑥ 第09课！把方法伪装成属性
    def llm_enabled(self) -> bool:                          #    返回 bool（第06课）
        """是否已配置 key，没配就回退到规则解析。"""        #    docstring 说明（第07课）
        return bool(self.dashscope_api_key.strip())         # ⑦ key 去空格后非空 → True

settings = Settings()                                       # ⑧ 创建一个全局配置对象（第07课实例化，不用 new）
```

**整体读法**：这个文件定义了"程序的配置"，从 `.env` 文件读 API key 等。
关键是 ⑥ 的 `llm_enabled`：别处代码用 `settings.llm_enabled`（不加括号，因为 @property）来判断"有没有配 key"，有就调大模型，没有就走规则。

---

## 二、schemas.py —— 数据格式定义（对应第 06、12 课）

文件：`backend/pi_agent/app/schemas.py`

```python
from typing import Any, Literal                  # 第06课：Any=任意类型, Literal=只能取固定值
from pydantic import BaseModel, Field            # 第12课：数据模型基类和字段规则

class DetectAnomalyRequest(BaseModel):           # 第12课：定义"异常检测请求"长什么样
    parameter: str | None = Field(               # 第06课 str|None：可以是字符串，也可以空
        default="hydraulic_pressure",            # 不传默认查液压压力
        description="参数英文名；为空则默认检测液压压力"
    )
    window_sec: int = Field(default=10, ge=1, le=300, description="检测最近多少秒")
    #            ↑int  ↑默认10        ↑1≤值≤300（第12课范围校验）

class DetectAnomalyResponse(BaseModel):          # 定义"异常检测的回复"长什么样
    has_anomaly: bool                            # 有没有异常（必填，没默认值）
    answer: str                                  # 给人看的中文答复
    window_sec: int                              # 检测了多少秒
    anomalies: list[dict[str, Any]]              # 第03/06课：一个列表，每个元素是字典
```

**整体读法**：这种 `XxxRequest` / `XxxResponse` 成对出现，
就是规定"浏览器发请求时该带哪些字段""后端回复时会给哪些字段"。
pydantic 自动校验：浏览器漏传字段、类型不对、`window_sec` 超出 1~300，都会被自动拦下报错——
**不用你手写一堆 if 检查**，这就是 demo 大量用 pydantic 的原因。

---

## 三、agent_core.py —— 智能体核心逻辑（对应第 04、05、07、10、11 课）

文件：`backend/pi_agent/app/services/agent_core.py`（摘最关键的部分）

```python
from datetime import timedelta        # 时间差工具
import re                             # 第11课：正则表达式
from typing import Any
from app.data.icd import find_parameter_by_text   # 第08课：从 app/data/icd.py 导入函数
from app.services.telemetry_store import store     # 从那个文件导入 store 对象（存飞参数据的）

class AgentCore:                      # 第07课：智能体类
    """最小版 Agent Core。Demo 里先用规则解析，保证没有模型 Key 也能跑通。"""

    def parse_time_offset_sec(self, question: str) -> int:   # 第05/06课：方法，收字符串返回int
        """解析'一分钟前/10秒前/当前'，返回负数表示过去。"""
        if "当前" in question or "现在" in question:          # 第02课 in 判断包含；第04课 or
            return 0

        minute_match = re.search(r"(\d+|一|两|二)分钟?前", question)  # 第11课：正则找"X分钟前"
        if minute_match:                                      # 找到了（不是 None）
            value = self._cn_number_to_int(minute_match.group(1))  # 抠出数字部分并转整数
            return -value * 60                                # 分钟转秒，负号=过去

        second_match = re.search(r"(\d+|一|两|二|十)秒前", question)  # 正则找"X秒前"
        if second_match:
            value = self._cn_number_to_int(second_match.group(1))
            return -value

        return 0                                              # 默认查当前

    def _cn_number_to_int(self, text: str) -> int:            # 第07课：_开头=内部私有方法
        mapping = {"一": 1, "二": 2, "两": 2, "十": 10}        # 第03课：字典当查找表
        if text.isdigit():                                    # 本身就是数字字符
            return int(text)
        return mapping.get(text, 1)                           # 第03课 .get：查不到默认返回1

    async def query_value(self, question: str) -> dict[str, Any]:  # 第10课 async；返回字典
        """自然语言查询，例如'一分钟前的气压高度？'"""
        icd = find_parameter_by_text(question)                # 调导入的函数：从问题里认出是哪个参数
        if icd is None:                                       # 第06课：没认出来（返回了None）
            return {                                          # 第03课：返回一个字典
                "answer": "没有识别到要查询的飞行参数，请换种说法",
            }
        # ...（下面会用 icd 和 store 去取数据、组织答复）
```

**整体读法**（这就是"智能体"的雏形）：
1. 用户问"一分钟前的气压高度？"
2. `parse_time_offset_sec` 用**正则**（第11课）从问题里解析出时间 → -60 秒
3. `find_parameter_by_text` 从问题里认出参数 → 气压高度
4. 拿时间和参数去 `store`（数据仓库）里取对应的值
5. 组织成中文答复，打包成**字典**（第03课）返回

注意 `async def`（第10课）：读逻辑时**完全可以忽略 async**，把它当普通函数，
业务流程一模一样。async 只是为了能同时处理多个用户请求。

---

## 四、读代码的通用顺序（任何 .py 文件都这么读）

1. **先看文件顶部的 import**（第08课）：知道它用了哪些工具、依赖哪些自己的文件
2. **再看有没有 class**（第07课）：找到主角类，看它的 `__init__` 有哪些成员
3. **逐个看方法**：方法名 + docstring 通常就说明了它干嘛
4. **看方法签名**（第06课）：参数类型、返回类型，心里有数它吃什么吐什么
5. **读方法体**：if/for/正则/字典操作，都是 01~11 课的内容
6. **遇到 async/await**：当透明的，按普通函数读逻辑

---

## 五、建议的下一步

- 把 01~12 课每个文件都 `python3 跑一遍`，看输出对照注释理解
- 然后打开真实文件对照本课读：
  - `~/桌面/demo-v2.0/backend/pi_agent/app/config.py`（最短，先读这个）
  - `~/桌面/demo-v2.0/backend/pi_agent/app/schemas.py`（全是 pydantic，练第12课）
  - `~/桌面/demo-v2.0/backend/pi_agent/app/services/agent_core.py`（智能体逻辑）
- 有任何一行看不懂，把那一行发我，我专门给你拆解。
```
```
