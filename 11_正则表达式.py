"""
第 11 课：正则表达式 re（demo 的 parse_time_offset_sec 用它从问题里抠数字）
运行：~/miniconda3/envs/py312/bin/python 11_正则表达式.py

正则是什么：
  一种「用一个模式字符串，去另一段文本里找符合规律的内容」的工具。
  比如从「一分钟前的气压高度」里，找出「分钟前」并提取数字。
  C/C++ 也有 <regex>，概念一样，Python 用起来更简洁。
  demo 用它做「自然语言解析」——没有大模型 key 时，靠正则规则也能听懂简单问题。
"""

import re      # 正则表达式模块，Python 标准库自带

# ============ 1. 最基本：搜索一段文本里有没有某个模式 ============
text = "最近10秒液压压力正常吗"

# re.search(模式, 文本)：在文本里找第一个匹配。找到返回「匹配对象」，找不到返回 None
m = re.search("液压", text)  #.search返回的是匹配对象，是有很多信息的东西，类似于词典那样，但并不是词典
if m:                              # 找到了（匹配对象为真）
    print("找到了'液压'")
else:
    print("没找到")

# ============ 2. 关键符号（先认识这几个，demo 就够用了）============
# \d   表示「一个数字字符」（0~9）。d = digit
# \d+  表示「一个或多个数字」。+ = 一个或多个
# +    前面的东西出现「1次或多次」
# ?    前面的东西「可有可无」（0次或1次）
# ( )  「分组」——把想单独提取出来的部分用括号框起来
# |    「或」

# 例：从文本里提取数字
m = re.search(r"\d+", "最近10秒") 
# \d+ 匹配「连续的数字」= "10"。而引号负责定义字符串范围，反斜杠负责在字符串内部表示特殊字符，所以必须加 r，表示「原始字符串」，让 \d 不被 Python 字符串处理掉
print(m.group())     # .group() 取出匹配到的内容 = "10"。m是有很多信息的东西，现在我只想要取出来他其中的匹配到的字符串，所以用.group()
# 注意模式字符串前面的 r：r"..." 叫「原始字符串」，
# 作用是让 \d 里的反斜杠 \ 不被特殊处理。正则模式「永远加 r」是好习惯。

# ============ 3. 分组 ( )：把要的部分单独抠出来 ============
# demo 真实代码：re.search(r"(\d+|一|两|二)分钟?前", question)
# 逐块拆解这个模式：
#   (\d+|一|两|二)  ← 括号是「第1组」，内容是「数字 或 一 或 两 或 二」。必须匹配，作为一个整体
#   分          单独作为一个整体。必须匹配「分」字
# 钟            和？作为一个整体，表示「钟」可有可无（"分前"也匹配）
#   ?               ← 问号只作用于前一个字「钟」，表示「钟」可有可无（"分前"也匹配）
#   前              ← 最后是「前」字。作为一个整体，这个也是必须匹配的
# 整体意思：匹配「(数字或一两二)分钟前」这种表达，并把数字部分单独存进第1组

question = "一分钟前的气压高度"
m = re.search(r"(\d+|一|两|二)分钟?前", question)
if m:
    print("整体匹配到:", m.group())     # m.group() 或 m.group(0)这俩一样都 = 整个匹配 "一分钟前"
    print("第1组(数字部分):", m.group(1))  # m.group(1) = 只取第1个括号里的东西。这个括号是第50行.search的顺序

question2 = "10分钟前的速度"
m2 = re.search(r"(\d+|一|两|二)分钟?前", question2)
print("第1组:", m2.group(1))            # = "10"

# ============ 4. 把上面拼成 demo 的逻辑（简化还原 parse_time_offset_sec）============
def parse_time_offset_sec(question):
    """解析'一分钟前/10秒前/当前'，返回偏移秒数（负数=过去）"""
    # 先看是不是问「当前」
    if "当前" in question or "现在" in question or "最新" in question:
        return 0

    # 找「X分钟前」
    minute_match = re.search(r"(\d+|一|两|二)分钟?前", question)#这个肯定和下面的if是二选一的，分和秒都是必须选的
    if minute_match:
        num_text = minute_match.group(1)         # 抠出数字部分，如 "一" 或 "10"
        value = cn_number_to_int(num_text)# 中文转阿拉伯（下面的辅助函数）。这里没有使用，如果使用在前，定义在后不可以
        return -value * 60                       # 分钟转秒，负号表示「过去」

    # 找「X秒前」
    second_match = re.search(r"(\d+|一|两|二|十)秒前", question)
    if second_match:
        value = cn_number_to_int(second_match.group(1))
        return -value

    return 0    # 默认查当前

def cn_number_to_int(text):
    mapping = {"一": 1, "二": 2, "两": 2, "十": 10}
    if text.isdigit():            # 已经是数字字符
        return int(text)
    return mapping.get(text, 1)   # 查表，查不到默认 1,如果查到就按查到的返回

# 测试
print(parse_time_offset_sec("一分钟前的气压"))   # -60（一分钟 = 过去60秒）
print(parse_time_offset_sec("10秒前的速度"))     # -10
print(parse_time_offset_sec("当前液压压力"))     # 0

print("\n==== 小结 ====")
print(r"re.search(r'模式', 文本) 找匹配；找到返回匹配对象，找不到返回 None")
print(r"\d=数字  \d+=多个数字  ?=可有可无  ()=分组  |=或")#原始字符串r是管\不被处理的，之前的f是管替换变量的
print("m.group()=整个匹配  m.group(1)=第1个括号里的内容")
print("正则模式字符串前面永远加 r，如 r'(\\d+)秒前'")
