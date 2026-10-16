"""
第 10 课：异步 async / await（demo 里函数前面那个 async 是什么）
运行：~/miniconda3/envs/py312/bin/python 10_异步async.py

为什么会有这个：
  Web 后端要同时处理很多人的请求。如果一个请求在「等」（等数据库、等网络、等大模型回复），
  传统做法会卡住整个线程。async 让程序「在等的时候，先去干别的请求」，提高并发。
  这有点像多线程，但更轻量。

给 C/C++ 程序员：
  - async def 定义的函数叫「协程」，调用它「不会立刻执行」，要用 await 才真正跑
  - await 的意思是「在这里等它完成，但这段等待期间，程序可以去处理别的任务」
  - 你看 demo 时，90% 情况下可以「忽略 async/await，把它当普通函数读」，逻辑完全一样！
    它们只影响「并发调度」，不影响「业务逻辑」。
"""

import asyncio        # Python 的异步运行库（标准库自带）

# ============ 1. 普通函数 vs 异步函数 长什么样 ============

# 普通函数（你已经会了）
def normal_add(a, b):
    return a + b

# 异步函数：只是前面多了个 async 关键字
async def async_add(a, b):
    return a + b
# 区别：normal_add(1,2) 直接得到 3；
#       async_add(1,2) 得到的不是 3，而是一个「协程对象」（一个待执行的任务）
print("普通函数直接给结果:", normal_add(1, 2))      # 3
print("异步函数给的是:", async_add(1, 2))           # <coroutine object ...> 一个任务，还没跑
# 上面那行还会有个警告说协程没被 await，正常现象，忽略。

# ============ 2. 怎么真正运行异步函数：用 await ============
# await 只能写在「另一个 async 函数」里面。所以我们写一个 async 的 main 来驱动。

async def main():
    # 在 async 函数里，用 await 调用另一个 async 函数，才能拿到真正的结果
    result = await async_add(3, 4)      # await = 等它跑完，拿结果
    print("await 拿到结果:", result)    # 7

    # 演示「等待」：模拟一个要花时间的操作（比如等大模型回复）
    print("开始等待...")
    await asyncio.sleep(1)              # 异步地睡 1 秒（期间可处理别的任务）
    print("等待结束（1秒后）")

# 程序入口：用 asyncio.run(...) 来启动最外层的 async 函数
# （你只在最外面用一次 asyncio.run，里面全靠 await 串起来）
asyncio.run(main())

# ============ 3. 看懂 demo 里的 async ============
# demo 的 agent_core.py 里有：
#
#   async def query_value(self, question: str) -> dict[str, Any]:
#       icd = find_parameter_by_text(question)
#       if icd is None:
#           return {...}
#       ...
#
# 解读：
#   - async def     → 这是个异步方法（因为可能要等大模型/数据库，不想卡住别人）
#   - self          → 第07课讲的，对象自己
#   - question: str → 参数是字符串
#   - -> dict[str, Any] → 返回一个「键是字符串、值任意」的字典
#   - 函数体里的 if/return 逻辑，和普通函数「完全一样」，正常读就行！
#
# 关键结论：读 demo 业务逻辑时，把 async 当透明的、把 await 当「调用」，
#          你理解的逻辑不会有任何偏差。async/await 只是性能机制。

# ============ 4. 调用别的 async 函数要 await（demo 里常见）============
async def step1():  #async定义了一个异步函数，调用后返回一个协程对象（coroutine object），不会立刻执行
    await asyncio.sleep(0.2)  #asyncio.sleep是asyncio这个库（模块）里提供的异步睡眠函数，模拟一个耗时操作
    return "第一步结果"

async def step2():
    # 调用另一个 async 函数，前面要加 await
    r = await step1()  #step1是一个async函数，所以调用它时要加 await，表示「等它完成拿结果」
    return r + " -> 第二步结果"

print(asyncio.run(step2()))
#这个程序，是先跑asyncio.run,然后进入step2函数，进去之后执行到await step1这个函数的时候，step2
# 函数暂停，也就是当前协程暂停，先去执行step1函数，进入step1函数后，执行asyncio.sleep函数，然后暂
# 停当前协程，也就是step1函数暂停，asyncio.sleep 设置一个 0.2 秒的计时器，然后立即把执行权交还给事
# 件循环，但是没有其他的任务，所以等待计时器到期，0.2 秒后事件循环再恢复 step1。，这个时候step2还是
# 不执行的，等sleep执行完成之后step1函数执行，返回了一个返回值，再进入step2函数，也返回了一个值，最后执行print
print("\n==== 小结 ====")
print("async def 定义异步函数（协程）；调用要 await 才真正执行")
print("await x = 等 x 完成拿结果，期间程序可去处理别的任务（提高并发）")
print("★ 读 demo 业务逻辑时：把 async 忽略、把 await 当普通调用，逻辑完全一样")
