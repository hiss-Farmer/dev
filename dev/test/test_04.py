# def test(num):
#     print("===== %d  _______%d" %(num, id(num)))
#     result = "hello"
#     print("+++++++ %d" % id(result))
#     return result
# a = 10
#
# print("-------- %d" % id(a))
#
# r = test(a)
# print("%s^^^^^^^ %d" % (r, id(r)))

# num = 10
#
# def dem01():
#     global num
#     num = 99
#     print("--------- %d" % num)
# def dem02():
#     print("===== %d" % num )
#
#
# dem01()
# dem02()
#
# gl_num = 10
# gl_title = "大幅度发生的"
# gl_name = "奥术大师"
# def demo():
#     num = 99
#     print("%d" % gl_num)
#     print("%s" % gl_title)
#     print("%s" % gl_name)
#
# demo()
# def measure():
#     print("sdfdf")
#     temp = 39
#     wetness = 50
#     print("dddd")
#     return  temp, wetness
# result = measure()
# print(result)
# print(result[0])
# print(result[1])
# gl_temp,gl_wetness = measure()
# print(gl_temp)
# print(gl_wetness)
#
#
#
# a = 6
# b = 100
# # c = a
# # a = b
# # b = c
# # a += b
# # b *= a
# # a -= b
# a, b = (b, a)
# print(a)
# print(b)



# def demo(num, num_list):
#     print("sadsad")
#     num = 100
#     num_list = [1, 2, 3]
#     print(num)
#     print(num_list)
#     print("sdsadsdasd")
# gl_num = 99
# gl_list = [4, 5, 6]
# demo(gl_num, gl_list)
# print(gl_num)
# print(gl_list)

#
# def dem01(num_list):
#     print("dsadasdas")
#     num_list.append(9)
#     print(num_list)
#     print("123434")
# gl_list = [1, 2, 3]
# dem01(gl_list)
# print(gl_list)



# def demo(num, num_list):
#     print("1111111")
#     num += num
#     num_list += num_list
#     print(num)
#     print("sdassa")
# gl_num = 9
# gl_list = [1, 2, 3]
# demo(gl_num, gl_num)
# print(gl_num)
# print(gl_list)

#
# gl_list = [6, 3, 9]
# #gl_list.sort(reverse=True)
# gl_list.sort()
# print(gl_list)


# def print_info(name, title, gender=True):
#     gender_test = "男生"
#     if not gender:
#         gender_test = "女生"
#     print("[%s] %s or %s " % (name, title, gender_test))
# print_info("小明","23")


# def demo(num, *nums, **person):
#     print(num)
#     print(nums)
#     print(person)
# #demo(1)
# demo(1, 2, 3, 4, 5, name = "dasdas")

#
# def sum_numbers(*args):
#     num = 0
#     print(args)
#     for n in args:
#         num += n
#     return num
# result = sum_numbers((1, 2, 3, 4, 5))
# print(result)

# def demo(*args, **kwargs):
#     print(args)
#     print(kwargs)
# gl_agrs = (1, 2, 3)
# gl_dict = {"name": "1213","age": "18"}
# demo(*gl_agrs, **gl_dict)
# demo(1, 2, 3, name="小明", age=18)
#
# def sum_number(num):
#     print(num)
#     if num == 1:
#         return
#     sum_number(num - 1)
# sum_number(3)

# def sum_numbers(num):
#     if num == 1:
#         return 1
#     temp = sum_numbers(num - 1)
#     return num + temp
# result = sum_numbers(2)
# print(result)
# class CaT:
#     def eat(self):
#         print("%s dsdsddd" % self.name)
#     def drink(self):
#         print("%s aaaaaa" % self.cc)
# tom = CaT()
# tom.name = "TOM"
# tom.eat()
#
# print(tom)
# addr = id(tom)
# print("%d" % addr)
#
# lazt_cat = CaT()
# lazt_cat.cc = "cctom"
#
# lazt_cat.drink()

# class TaS:
#     def __init__(self, new_name):
#         print("sdasdsadsad")
#         self.name = new_name
#     def df(self):
#         print("%s sadas" % self.name)
# tom = TaS("----")
# print(tom.name)
# print(tom.df())
# class DeF:
#     def __init__(self, new_name):
#         self.name = new_name
#         print("%s  ========" % self.name)
#     def __del__(self):
#         print(" %s del" % self.name)
#     def __str__(self):
#         return  "sdasdas"
# tom = DeF("YOU")
# print(tom)
# del tom
# print("-" * 20)

# class Person:
#     def __init__(self, name, weight):
#         self.name = name
#         self.weight = weight
#     def __str__(self):
#         return "sadsadsadas %s %.2f " %(self.name, self.weight)
#     def run(self):
#         return "%s dddddd %.2f" %(self.name)
#
#     def eat(self):
#         return "%s ffffff%.2f" % (self.name)
# xiaoming = Person("-----", 22)
# xiaoming.eat()
# xiaoming.eat()
# print(xiaoming)
#
# class HounsItem:
#     def __init__(self, name, area):
#         self.name = name
#         self.area = area
#     def __str__(self):
#         return "[%s] ---- % .2f" % (self.name, self.area)
# class House:
#     def __init__(self, hosu_type, area):
#         self.hosu_type = hosu_type
#         self.area = area
#         self.free_area = area
#         self.item_list = []
#     def __str__(self):
#         return ("[%s]===\n===%.2f[---%.2f]\n %s" %(self.hosu_type, self.area, self.free_area, self.item_list))
#     def add_itme(self, item):
#         print("%s" % item)
#         if item.area > self.free_area:
#             print("%s ++++++" % item.name)
#             return
#         self.item_list.append(item.name)
#         self.free_area -= item.area
#
#
# bed = HounsItem("asdc", 4)
# chest = HounsItem("qwe", 2)
# table = HounsItem("uiop", 1.5)
#
# print(bed)
# print(chest)
# print(table)
# 
#
# my_hone =House("ASDSAD", 60)
# my_hone.add_itme(bed)
# my_hone.add_itme(chest)
# my_hone.add_itme(table)
# print(my_hone)

#
# class Gun:
#     def __init__(self, model):
#         self.model = model
#         self.bullet_count = 0
#     def add_bullet(self, count):
#         self.bullet_count += count
#     def shoot(self):
#         if self.bullet_count <= 0:
#             print(" %s meriyou le ..." % self.model)
#             return
#         self.bullet_count -= 1
#
#         print("[%s]...[%d]" %(self.model, self.bullet_count))
#
# class Soldier:
#     def __init__(self, name):
#         self.name = name
#         self.gun = None
#     def fire(self):
#        if self.gun == None:
#            print("%sdfdsfd" % self.name)
#            self.gun.add_bullet(50)
#            self.gun.shoot()
#
#
# ak47 = Gun("AK47")
# # ak47.add_bullet(50)
# # ak47.shoot()
#
# xusanduo = Soldier("xusan")
# xusanduo.gun = ak47
# xusanduo.fire()
# print(xusanduo.gun)

# class Women:
#     def __init__(self, name):
#         self.name = name
#         self.__age = 18
#     def secret(self):
#         print("%sfdfds  %d" %(self.name, self.__age))
# xiaofang = Women("xiaofang")
# print(xiaofang._Women__age)
# xiaofang._Women__secret()
#
# class Animal:
#     def eat(self):
#         print("chi")
#     def drink(self):
#         print("pao")
#     def run(self):
#         print("pao")
#     def sleep(self):
#         print("shui")
# class Dog(Animal):
#     # def eat(self):
#     #     print("chi")
#     # def drink(self):
#     #     print("pao")
#     # def run(self):
#     #     print("pao")
#     # def sleep(self):
#     #     print("shui")
#     # def bark(self):
#     #     print("wangwangwang")
#     pass
# wangcai = Dog()
# wangcai.eat()
# wangcai.drink()
# wangcai.sleep()
# wangcai.run()
# # wangcai.bark()

#
# class Animal:
#     # print("xxixixi")
#     pass
# class Dog(Animal):
#     def bark(self):
#         print("hheheheh")
# class XiaoTianQuan(Dog):
#     def fly(self):
#         print("fffffffff")
#     # def bark(self):
#     #     print("wangwangwangnwagn")
#     def bark(self):
#         print("sdsssssss")
#         super().bark()
#         print("$%$$$%$%$%$%$%")
# xtq = XiaoTianQuan()
# xtq.bark()

# class A:
#     def __init__(self):
#         self.num1 = 100
#         self.__num2 = 200
#     def __test(self):
#         print("....%d....%d.." % (self.num1, self.__num2))
#     def test(self):
#         print("$$$$$$$$ %d" % self.__num2)
# class B(A):
#     def demo(self):
#         print("++++++++++++++++++ %d" % self.num1)
#
# b = B()
# print(b)
# b.demo()
# print(b.num1)
# b.test()


# class A:
#     def test(self):
#         print("!!!!!!!!!!!!!11111")
#     def demo(self):
#         print("@@@@@@@@@@@@@@11111")
# class B:
#     def test(self):
#         print("!!!!!!!!!!!!!!! 222")
#     def demo(self):
#         print("@@@@@@@@@@@@@@@2222")
# class C(B, A):
#     pass
#
# ff = C()
# ff.test()
# ff.demo()
#
# print(C.__mro__)

#
# class PerSon(object):
#     def __init__(self, name):
#         self.name = name
#     def game(self):
#         print("%s......." % self.name)
# class Dog(PerSon):
#     def game(self):
#
# class xiaoming:
#
# class Tool(object):
#     conut = 0
#     @classmethod
#     def show_tool_count(cls):
#         print("dddddddd %d" % cls.conut)
#     def __init__(self, name):
#         self.name = name
#         Tool.conut += 1
# tool1 = Tool("kk")
# tool2 = Tool("cc")
# tool3 = Tool("dd")
# tool3.conut = 99
# Tool.show_tool_count()
# print(Tool.conut)
# print("------ %d" % tool3.conut)
# print("===== %d" % Tool.conut)


#
# class Dog(object):
#     @staticmethod
#     def run():
#         print("sssssssssss")
# Dog.run()


# class Game(object):
#     top_score = 0
#     def __init__(self, player_name):
#         self.player_name = player_name
#         @staticmethod
#         def show_help():
#             print("..............")
#         @classmethod
#         def show_top_scorp(cls):
#             print("sdsdd   %d " % cls.top_score)
#         def start_game(self):
#              print(";;;;;; %s" % self.player_name)
#
# tt = Game.top_score
# print(tt)
#
# class MusicPlayer(object):
#     def __new__(cls, *args, **kwargs):
#         print("sdasdsa, sadasdas")
#         instance = super().__new__(cls)
#         return instance
#
#     def __init__(self):
#         print("chushifa")
# player = MusicPlayer()
# print(player)

# class MusicPlayer(object):
#     instnce = None
#     init_flag = False
#     def __new__(cls, *args, **kwargs):
#     def __init__(self):
#         if MusicPlayer.init_flag:
#             return
#         print("sdfdsfsdf")
#         MusicPlayer.init_flag = True
#
# player = MusicPlayer()
# player2 = MusicPlayer()
# print(player)
# print(player2)
# try:
#     num = int(input("sdasdasd:"))
# except:
#     print("ddsfsdfsd")
# print("*" * 50)

# try:
#     num = int(input("sdsad:"))
#     result = 8 / num
#     print(result)
# except ZeroDivisionError as aaa:
#     print("00000 %s" % aaa)
# except ValueError as bbb:
#     print("111111 %s" % bbb)
# except Ellipsis as vvv:
#     print("ffff %s" % vvv)
# else:
#     print("!!!!!!!")
# finally:
#     print("pppppppppppppp")
# print("%" * 50)


#
# def demo1():
#     return  int(input("sdasd:"))
# def demo2():
#     return  demo1()
# try:
#     print(demo1())
# except Exception as reus:
#     print("sdsad %s" % reus)


# def input_password():
#     pwd = input("sadas:")
#
#     if len(pwd) >= 8:
#         return pwd
#     print("sdasdasdad")
#     ex = Exception("DFDSFDSFDS")
#
#     raise ex
#
# try:
#     print(input_password())
# except Exception as yy:
#     print(yy)
# print(input_password())

# import  random
# print(random.__file__)
#
# ran = random.randint(0, 10)
# print(ran)
