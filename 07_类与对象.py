"""
第 07 课：类与对象 class（对应 demo 的 AgentCore 类）
运行：~/miniconda3/envs/py312/bin/python 07_类与对象.py

C++ 对比（你熟悉 class，所以这课主要讲「不一样的地方」）：
  1. 没有 .h / .cpp 分离，类就写在一个文件里
  2. 没有 public/private 关键字（靠命名约定：下划线开头 _x 表示「私有，别动」）
  3. 每个方法第一个参数必须是 self（相当于 C++ 隐藏的 this 指针，但要手写出来）
  4. 构造函数叫 __init__（前后各两个下划线），不是和类同名

  class可以理解成工具箱，里面有很多def定义的工具（方法），也可以放一些数据（成员变量）
"""

# ============ 1. 定义一个最简单的类 ============
# C++:  class Dog { public: ... };
class Dog:
    # __init__ 是构造函数（C++ 的 Dog(){...}）
    # self 就是「当前这个对象自己」，相当于 C++ 的 this，但 Python 要求你手写出来
    #self不是关键字，是约定俗成的名字
    def __init__(self, name, age):  #__init__必须要这么写，如果想要在调用的时候有默认值,name\age是形参
                                    #下面的class没有__init__是因为他调用的时候不需要传参数，直接用默认的空构造函数
        # self.xxx = ... 就是给这个对象创建/赋值「成员变量」
        # C++ 要先在类里声明 string name; 这里不用，直接 self.name 就建好了
        self.name = name      # 成员变量 name，也就是对象的属性
        self.age = age        # 成员变量 age，也就是对象的属性

    # 这是一个「方法」（成员函数）。第一个参数永远是 self
    # C++:  void bark() { cout << name; }   —— 这里要写成 def bark(self):
    def bark(self):
        # 在方法里访问成员变量，必须写 self.name（C++ 可省略 this，Python 不能省 self）
        print(f"{self.name} 汪汪叫！")

    def birthday(self):
        self.age += 1
        print(f"{self.name} 现在 {self.age} 岁")

# ---- 创建对象（实例化）----  d是对象，是Dog的对象，Dog是类，这个类里面的def定义的是方法，方法里面的self是对象d自己
# 注意：不用 new！直接「类名(参数)」。这些参数传给 __init__（self 不用你传，自动传）
d = Dog("旺财", 3)        # C++: Dog d("旺财", 3);  或  Dog* d = new Dog(...);
d.bark()                  # 调用方法，点 . 调用。self 自动 = d，你不用管
d.birthday()              #会改变Dog("旺财", 3)里面的值，不是暂时的
print("名字是:", d.name)  # 直接读成员变量

# ============ 2. demo 里 AgentCore 长什么样（简化还原）============
class AgentCore:  #这个不像上一个有__init__，所以用默认的空构造函数
    """
    三个引号的这段叫「文档字符串 docstring」，写在类/函数开头，
    用来说明这个类是干嘛的。相当于 C++ 注释，但 Python 能用工具自动提取它。
    demo 里 AgentCore 的作用：把自然语言问题，解析成对飞参数据的查询。
    """

    # 一个内部辅助方法。名字以 _ 开头 = 约定俗成的「私有」，意思是「类内部用，外面别调」
    # 注意：Python 不像 C++ 有真正的 private，下划线只是「君子协定」
    def _cn_number_to_int(self, text):
        """把中文数字转成阿拉伯数字，例如 '十' -> 10"""
        mapping = {"一": 1, "二": 2, "两": 2, "十": 10}   # 一个字典做查找表
        if text.isdigit():          # 如果本身就是数字字符（如 "5"）
            return int(text)       # 直接转 int
        return mapping.get(text, 1) # 否则查表，查不到默认返回 1

    # 一个公开方法：解析「最近N秒」
    def parse_window_sec(self, question):
        """从问题里解析出时间窗口秒数"""
        if "十秒" in question:
            return self._cn_number_to_int("十")   # class内部调用自己的其它方法或者东西，要加 self.
        return 10                                  # 默认 10 秒

# 使用它
agent = AgentCore()                    # 创建对象（__init__ 没写，用默认的空构造）
print(agent.parse_window_sec("最近十秒液压正常吗"))   # 10
print(agent._cn_number_to_int("二"))                  # 2（外部其实也能调 _ 方法，只是不建议）

# ============ 3. self 到底是什么？再强调一次 ============
# self 就是「调用这个方法的那个对象」。
#   agent.parse_window_sec("...")  这一句，Python 自动把它翻译成：
#   AgentCore.parse_window_sec(agent, "...")   ← 看，agent 被当作 self 传进去了
# 所以方法定义里第一个参数 self，你调用时「不用也不能」自己传，Python 替你传。

print("\n==== 小结 ====")
print("class 定义类；__init__ 是构造函数；self ≈ C++ 的 this 但必须手写")
print("self.x = 值  创建成员变量；方法第一个参数永远是 self")
print("_开头的名字 = 约定的私有（不强制）；创建对象不用 new，直接 类名(参数)")

import le08模块与导入 #导入第八节，最好不要有_和中文，容易出错
print("导入完成")