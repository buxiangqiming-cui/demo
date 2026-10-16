"""
第 03 课：容器 —— 列表 list / 字典 dict / 元组 tuple
运行：~/miniconda3/envs/py312/bin/python 03_容器_列表字典元组.py

C/C++ 对比（这是 demo 里返回值的核心，必须熟）：list是中括号，字典是花括号，元组是圆括号
  - list  ≈ std::vector，但能装不同类型，写法 [ ]
  - dict  ≈ std::map / 哈希表，写法 { 键: 值 }   ← demo 函数大多返回 dict
  - tuple ≈ 不可变的数组，写法 ( )
"""

# ============ 1. 列表 list（≈ vector，但更灵活）============
nums = [10, 20, 30]            # C++: std::vector<int> nums = {10,20,30};
print(nums[0])                 # 取下标 = 10
nums.append(40)                # 末尾追加（vector::push_back）
print(nums)                    # [10, 20, 30, 40]
print(len(nums))               # 长度 = 4
print(nums[-1])                # 最后一个 = 40（负下标）
print(nums[1:3])               # 切片 = [20, 30]

# 列表能混装不同类型（C++ 的 vector 做不到）
mixed = [1, "二", 3.0, True]
print(mixed)

# 遍历列表：for x in 列表（不用下标！）
for n in nums:  #02节讲的in单独用，看左边是否在右边里面，返回 True/False；
                #for in 是遍历，左边是变量，右边是容器，从容器中一个个拿出来放到变量里
    print("元素:", n)

# 如果确实要下标，用 enumerate
for i, n in enumerate(nums):  #enumerate(nums)会产生0,10 1,20 2,30 3,40这样的元组，左边两个变量接收
    print(f"第{i}个 = {n}")

# ============ 2. 字典 dict（≈ map，demo 返回值几乎都是它）============
# 键值对，键通常是字符串
person = {
    "name": "张三",
    "age": 18,
    "height": 1.75,
}

#注意下面的person["age"] = 19，用的是中括号，person.get("age")用的是圆括号
print(person["name"])           # 按键取值 = 张三（C++: person["name"]）
person["age"] = 19              # 修改
person["city"] = "济南"         # 新增键（map 里键不存在就自动插入）
print(person)

# demo 里典型的返回值就长这样：
result = {
    "answer": "液压压力当前 21.3 MPa",
    "parsed_query": {"parameter": "hydraulic_pressure", "offset": 0},
    "data": {"value": 21.3, "unit": "MPa"},   #dict里面套 dict
}
print(result["answer"])
print(result["data"]["value"])   # 字典套字典，一层层取，=> 21.3

# 安全取值：用 .get()，键不存在返回 None 而不报错
print(person.get("name"))        # 张三
print(person.get("phone"))       # None（键不存在，但不崩溃）
print(person.get("phone", "无")) # 给默认值 = 无

# 遍历字典
for key, val in person.items():
    print(f"{key} -> {val}")
#只需要键person.keys()，只需要对person.values()，都需要person.items(),固定

# ============ 3. 元组 tuple（≈ 不可变数组/结构体）============
point = (3, 4)                  # 圆括号，元组最重要的是逗号，y=3,5也是元组，w=（3,）也是
print(point[0])                 # = 3
# point[0] = 9                  # ← 报错！元组不能改（这是它和 list 唯一的关键区别）

# 元组常用来一次返回多个值（C++ 要用 struct 或 pair）
def get_min_max(data):
    return min(data), max(data)   # 返回一个元组

#下面这行必须要加中括号list或者圆括号tuple，否则就是传了四个参数，跟定义的不一样
lo, hi = get_min_max([5, 1, 9, 3])  # 拆包，一次接两个返回值，5,19,3是list,也可以换成圆括号的元组
print(f"最小 {lo}, 最大 {hi}")
#hi = get_min_max([5, 1, 9, 3])会让hi=（1,9），因为def设计的就是返回两个数，返回的是1,9
#但是左边只有一个hi,没法接受两个数，所以这两个数就被当成一个元组了，hi=（1,9）

print("\n==== 小结 ====")
print("list[]≈vector，dict{}≈map(demo返回值)，tuple()≈不可变；for x in 容器 直接遍历")
