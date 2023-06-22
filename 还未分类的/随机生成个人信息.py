# 导入相关模块
import random
import pandas as pd

# 定义一个函数，用于随机生成一个姓名
def generate_name():
  # 定义姓氏列表，包含常见的百家姓
  surnames = ["赵", "钱", "孙", "李", "周", "吴", "郑", "王", "冯", "陈", "褚", "卫", "蒋", "沈", "韩",
              "杨", "朱", "秦", "尤", "许", "何", "吕", "施", "张", "孔", "曹", "严", "华", "金",
              "魏", "陶", "姜", "戚", "谢", "邹", "喻", "柏", "水", "窦", "章","云","苏","潘","葛",
              "奚","范","彭","郎","鲁","韦","昌","马","苗","凤","花","方","俞","任","袁",
              "柳","酆","鲍","史","唐","费","廉","岑","薛","雷","贺","倪","汤","滕","殷",
              "罗","毕","郝","邬","安" ,"常" ,"乐" ,"于" ,"时" ,"傅" ,"皮" ,"卞" ,"齐" ,"康" ,"伍",
              "余" ,"元" ,"卜" ,"顾" ,"孟" ,"平" ,"黄" ,"和" ,"穆" ,"萧" ,"尹" ,"姚" ,"邵" ,"湛",
              "汪" ,"祁" ,"毛" ,"禹" ,"狄" ,"米" ,"贝" ,"明" ,"臧" ,"计" ,"伏" ,"成" ,"戴",
              "谈" ,"宋" ,"茅"]
  # 定义名字列表，包含常见的单字和双字名
  names = ["华", "明", "丽", "强", 
           # 省略部分内容，以节省空间
           # ...
           # ...
           # ...
           # ...
           # ...
           # ...
           # ...
           # ...
           # ...
           # ...
           # ...
           # ...
           # ...
           # ...
           # ...
           # ...
           # ...
           # ...
           # ...
           # 结束省略
           ]
  # 从姓氏列表中随机选择一个
  surname = random.choice(surnames)
  # 从名字列表中随机选择一个或两个
  name = random.choice(names) + random.choice(names + [""])
  # 返回拼接后的姓名
  return surname + name

# 定义一个函数，用于随机生成一个家庭住址
def generate_address():
  # 定义省份列表，包含中国所有的省份和直辖市
  provinces = ["北京市", 
               # 省略部分内容，以节省空间
               # ...
               # ...
               # 结束省略
               ]
  # 定义城市列表，包含中国所有的地级市和自治州
  cities = ["东城区",
            # 省略部分内容，以节省空间
            # ...
            # ...
            # 结束省略
            ]
  # 定义街道列表，包含一些常见的街道名称
  streets = ["东直门街道",
             # 省略部分内容，以节省空间
             # ...
             # 结束省略
             ]
  # 定义门牌号列表，由1到100的数字加上号或号楼组成
  numbers = [str(i) + random.choice(["号","号楼"]) for i in range(1,101)]
  # 从省份列表中随机选择一个
  province = random.choice(provinces)
  # 从城市列表中随机选择一个
  city = random.choice(cities)
  # 从街道列表中随机选择一个
  street = random.choice(streets)
  # 从门牌号列表中随机选择一个
  number = random.choice(numbers)
  # 返回拼接后的家庭住址
  return province + city + street + number

# 定义一个函数，用于随机生成一个电话号码
def generate_phone():
  # 定义电话号码前缀列表，包含常见的手机号码前三位
  prefixes = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
              "150", "151", "152", "153", "155", "156", "157", "158", "159",
              "180", "181", "182", "183", "184", "185", "186", "187", "188", "189"]
  # 定义电话号码后缀列表，由四位数字组成
  suffixes = [str(random.randint(0,9999)).zfill(4) for i in range(10000)]
  # 从前缀列表中随机选择一个
  prefix = random.choice(prefixes)
  # 从后缀列表中随机选择一个
  suffix = random.choice(suffixes)
  # 返回拼接后的电话号码
  return prefix + suffix

# 定义一个空的数据框，用于存放生成的信息
df = pd.DataFrame(columns=["姓名", "家庭住址", "电话"])

# 定义一个函数，用于随机生成一条个人信息，并返回一个字典
def generate_info():
  # 调用函数，生成一个姓名
  name = generate_name()
  # 调用函数，生成一个家庭住址
  address = generate_address()
  # 调用函数，生成一个电话号码
  phone = generate_phone()
  # 返回一个字典，包含生成的信息
  return {"姓名": name, "家庭住址": address, "电话": phone}

# 定义一个循环，用于生成多条个人信息，并添加到数据框中
for i in range(100):
  # 调用函数，生成一条个人信息
  info = generate_info()
  # 将生成的信息添加到数据框中，忽略索引
  df=df._append(info, ignore_index=True)#,inplace=True)
  # df._append(info, ignore_index=True)

# 打印数据框，查看生成的信息
print(df)

# 将数据框保存到excel表格中，命名为info.xlsx，不保存索引
df.to_excel("info.xlsx", index=False)
