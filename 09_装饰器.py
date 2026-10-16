"""
第 09 课：装饰器 @（demo 里 @property、@router.get、@app.route 是什么）
运行：~/miniconda3/envs/py312/bin/python 09_装饰器.py

一句话理解：
  装饰器就是「在一个函数/方法上面贴一行 @某某」，
  作用是「给这个函数额外套一层功能，但不改动函数本身的代码」。
  C/C++ 没有完全对应的语法，最接近的是「宏」或「包一层的函数」，但装饰器更优雅。
  你现在不需要会「写」装饰器，只需要「看懂别人贴的 @ 是干嘛的」。
"""

# ============ 1. 先理解：函数可以被「包一层」============
# 假设我想在调用任何函数前后打印日志，但不想改原函数。

def my_log(func):        # 这个函数接收「一个函数」作为参数，想做成装饰器的函数形参必须是func
    def wrapper(*args, **kwargs):  # 定义一个「包装函数」
        print(f"[日志] 即将调用 {func.__name__}")#固定这么写__name__，打印函数名
        result = func(*args, **kwargs)   # 调用原来的函数, *负责接收不是词典的，**负责接收词典的参数，不管顺序
        print(f"[日志] 调用结束，{func.__doc__}")#__doc__ 是函数的文档字符串，也就是28行 """...""" 里的内容
        return result
    return wrapper        # 返回这个包装后的函数，而且注意没有括号！返回的是函数对象本身，而不是调用结果。
                            #如果是带（）就会直接调用，返回的是函数的返回值，而不是函数本身。
#如果32行是say_hello(name="张三", age=18)，那么args就是()，kwargs就是{"name":"张三","age":18}
#如果32行是say_hello('"name"="张三", "age"=18',)，那么args就是('"name": "张三", "age": 18'，)，kwargs就是{}
#                                                    必须有逗号，表示只有一个元素的元组    ↑
# ---- 用装饰器语法 @ 来套上面这层 ----
@my_log        # 这一行 = 「给下面的 say_hello 套上 my_log」     这一行只有函数名没有括号，表示传函数对象本身，而不是调用结果
def say_hello(name):
    """say_hello 函数的文档字符串"""
    print(f"你好，{name}")

say_hello("张三")
# 输出会是：
#   [日志] 即将调用 say_hello
#   你好，张三
#   [日志] 调用结束
# 看！say_hello 自己的代码没改，但被 @my_log 包了一层额外功能。这就是装饰器。

# @my_log 等价于手写：say_hello = my_log(say_hello)
# 「@装饰器」只是这句话的简写。

# ============ 2. @property：把方法「伪装成」属性（demo 的 config.py 用了）============
class Settings:
    def __init__(self, key):
        self.dashscope_api_key = key   # 成员变量：API key
#Python 里一般有个习惯：如果它像一个“状态/属性”，就适合用 @property
    @property  # ★ 贴上 @property,从而让这个方法变成一个属性，也就是对象可以用过.llm_enabled 访问，而不用加括号，加了括号就是调用方法了
    def llm_enabled(self):  # 这本来是个方法（要 s1.llm_enabled() 调用），现在只需要 s1.llm_enabled 就能访问了
        """是否配置了 key"""
        # 贴了 @property 后，调用时「不用加括号」，像访问变量一样
        return bool(self.dashscope_api_key.strip())
        # bool(...) 把值转成 True/False；.strip() 去空格；空字符串 → False

s1 = Settings("my-key-123")
s2 = Settings("")                      # 空 key

# 注意：访问 llm_enabled 不加括号！因为 @property 把它伪装成了属性
print(s1.llm_enabled)                  # True（有 key）
print(s2.llm_enabled)                  # False（空 key）
# 如果没有 @property，就得写 s1.llm_enabled() 加括号。这就是 @property 的作用：
# 让「需要计算的值」用起来像「普通成员变量」。

# ============ 3. demo 里的 @router.get / @app.route 是什么 ============
# 你会在 Web 后端代码看到这种：
#
#   @router.get("/health")
#   def health():
#       return {"status": "ok"}
#
# 意思是：「把下面这个 health 函数，注册为『当浏览器访问 /health 网址时』要调用的函数」。
# 装饰器在这里的作用是「登记路由表」——告诉框架哪个网址对应哪个函数。
# 你不用关心它内部怎么实现，只要知道：
#   @router.get("/xxx")  → 访问 GET /xxx 时跑下面的函数
#   @router.post("/yyy") → 提交 POST /yyy 时跑下面的函数
# demo 的 pi_agent 就是用一堆这样的 @ 把各个网址和函数对应起来的。

# 模拟演示（不联网，仅示意登记效果）：
routes = {}          # 一个字典当「路由表」，后面慢慢填东西进去

def get(path):                         # 简化版的 @router.get
    def decorator(func):
        routes[path] = func            # 把 路径->函数 登记进表
        return func
    return decorator

@get("/health")                        # 登记：/health 对应 health 函数
def health():
    return {"status": "ok"}

@get("/simulator/status")              # 登记：/simulator/status 对应 status 函数
def status():
    return {"running": True}

print("已登记的路由表:", list(routes.keys()))   # ['/health', '/simulator/status']
print("访问 /health 得到:", routes["/health"]())  # 模拟访问，调用对应函数

print("\n==== 小结 ====")
print("@装饰器 = 给函数套一层额外功能，不改原函数；@x 等价于 f = x(f)")
print("@property：方法伪装成属性，调用时不加括号（demo config.py 的 llm_enabled）")
print('@router.get("/health")：把函数登记为某网址的处理器（demo 后端路由）')
