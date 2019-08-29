# # import test_02
# import time
#
#
# # test_02.multiple_table()
#
#
# def test1():
#     print("-" * 10)
#
#
# def test2(aaa, bbb):
#     print(aaa * bbb)
#     time.sleep(10)
#     test1()
#
#
# test2("99", 20)
#
#
# def test3(ccc, nnn):
#     """
#
#     :param ccc:
#     :param nnn:
#     """
#     row = 0
#     while row < 5:
#         print(ccc * nnn)
#         row += 1
#
#
# test3("-", 20)


# naem_list = ["zhangsan", "lishi", "wangwu"]
# print(naem_list[1])
# print(naem_list)
# print(naem_list.index("wangwu"))
# naem_list[0] = "李四"
# naem_list.append("wudalang")
# naem_list.insert(1,"xiaomei")
# tmp_lis = ["zhuerge", "xiaoerge"]
# naem_list.extend(tmp_lis)
# naem_list.remove("wangwu")
# naem_list.pop()
# naem_list.pop(2)
# del naem_list[2]
# ddd = len(naem_list)
# print(ddd)
# print(naem_list)
# name_lsi = ["2", "1", "3", "4"]
# for n in name_lsi:
#     print(n)

# name_lsi.sort()
# name_lsi.reverse()
#
#
# print(name_lsi)
#
# import keyword
# rty = len(keyword.kwlist)
# print(rty)
# print(keyword.kwlist)

# info_tuple = ("zhangsan", 18, 1.75, "zhangsan")
# for my_info in info_tuple:
#      print(my_info)

# info_tuple = ("小明", 18, 1.75)
# print("%s 年龄是%d 身高是%.2f" % info_tuple)
# print(type(info_tuple))
# print(info_tuple[1])
# print(info_tuple.index("zhangsan"))
# print(info_tuple.count("zhangsan"))

# info_tulp  = {"name": "小明",
#               "age": 18,
#               "gender": True,
#               "height": 1.75,
#               "weight": 75.5}
# info_tu = {"he": "buzhdiao",
#            }
# info_tulp.update(info_tu)
# print(len(info_tulp))
# for tt in info_tulp:
#     print("%s  %s" % (tt, info_tulp[tt]))
#info_tulp.clear()
# print(info_tulp["name"])
# print(info_tulp["age"])
# info_tulp["name"] = "小小明"
# info_tulp.pop("name")
# print(info_tulp)
#
# card_list = [
#     {"name": "zhangsan",
#     "qq": "123456",
#     "phone": "110"},
#     {"name":"lisi",
#      "qq":"654321",
#      "phone":"10086"}
#
#
# ]
#
# for k in card_list:
#    print(k)
#    # print("%s  %s" % (k,card_list[k]))

str1 = "hello pthon"
# str2 = '我的外号是"大西瓜"'
# print(str2)
# print(str1[4])
# print(str1.startswith("Hello"))
#
#
# print(str1.endswith("python"))
# print(str1.find("llo"))
# print(str1.replace("pthon", "world"))

# poem = ["是的发送到",
#         "是电饭锅电饭锅",
#         "是的发送到郭德纲"]
#
# # for  ger in  poem:
# #     print("|%s|"% ger.center(20, " "))
# poe = "发光时\r代鬼地方个地\t方官的双\n方各得给对方"
# print(poe.split())
# red = "".join(poe)
# print(red)

# nam_str = "0123456789"
# print(nam_str[2:6])
# print(nam_str[2:])
#  print(nam_str[:6])
import test_02

test_02.zhushi()
while True:
    action = input("请选择输入执行的操作:")
    print("选择的操作是 %s" % action)

    if action in ["1", "2", "3"]:

        if action == "1":
            test_02.show_oll()
        elif action == "2":
            test_02.search_carh()
        elif action == "3":
            test_02.search_card()
    elif action == "0":
        break
    else:
        print("您输入的不正确，请重新选择")

























































