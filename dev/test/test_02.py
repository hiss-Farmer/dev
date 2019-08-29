#
# def multiple_table():
#     row = 1
#     while row <= 9:
#         col = 1
#         while col <= row:
#             print("%d x %d = %d" % (col, row, col * row), end="\t")
#             col += 1
#         print("")
#         row += 1
#
# def say_hello():
#
#     print("hello 1")
#     print("hello 2")
#     print("hello 3")
#
# def sun_num(num1, num2):
#     # num1 = 20
#     # num2 = 30
#     restr = num1 + num2
#
#     print("%d + %d = %d" % (num1, num2, restr))
# sun_num(10, 20)
#
# def sun_1_unm(num3,num4):
#     result = num3 + num4
#     return result
# sun_resulf = sun_1_unm(10, 20)
# print("计算结果为：%d" % sun_resulf)
card_list = []
def zhushi():
    """显示菜单"""
    print("*" * 50)
    print("还原使用...." )
    print("1.dfdsfsdf")
    print("2..dfsdfs")
    print("3...dsfsdfdsf")
    print("0  exit")
    print("*" * 50)

def show_oll():
    """显示名片"""
    name_str = input("请输入名字：")
    phone_str = input("请输入电话：")
    qq_str = input("请输入qq：")
    email_str = input("请输入邮箱：")
    card_dist = {
               "name": name_str,
                "phone": phone_str,
                "qq": qq_str,
                "email": email_str
    }
    card_list.append(card_dist)
    print(card_list)
    print("dasasdsa %s" % name_str)
def search_carh():


    print("-" * 50)
    print("=" * 3)
    if len(card_list) == 0:
        print("no " * 4)
        return
    for name in ["姓名", "电话", "qq", "邮箱"]:
        print(name, end="\t\t")

    print(" ")
    print("-" * 50)
    for card_dict in card_list:
        print("%s\t\t%s\t\t%s\t\t%s" % (card_dict["name"],
                                        card_dict["phone"],
                                        card_dict["qq"],
                                        card_dict["email"]))
def search_card():
    find_name = input("输入要搜索的姓名：")

    print("find...")
    for card_dict in card_list:
        if card_dict["name"] == find_name:
            print("-" * 50)
            print("姓名\t\t电话\t\tqq\t\t邮箱")

            print("%s\t\t%s\t\t%s\t\t%s" % (card_dict["name"],
                                            card_dict["phone"],
                                            card_dict["qq"],
                                            card_dict["email"]))
            print("-" * 50)
            deal_card(card_dict)
            break
    else:
        print("no no no no no")

def deal_card(find_name):
    print(find_name)
    action_str = input("dfssss 1 del 2 ff 0 find")
    if action_str == "1":
        card_list.remove(find_name)
    elif action_str == "2":
       find_name["name"] == input("xingm:")
       find_name["phone"] == input("dianua:")
       find_name["qq"] == input("qq:")
       find_name["email"] == input("youxiang:")
       print("okokokokok !")
def inpit_card_info(dict_value, tip_message):
    result_str == input(tip_message)
