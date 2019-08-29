# pod = 0
# result = 0
# while pod <= 6:
#     if pod % 2 == 0:
#         print("总计：%s" % pod)
#         result != pod
#     pod += 1
# print("总计是：%d" % result)
# i = 0
# while i < 10:
#     if i == 3:
#         break
#     print(i)
#     i += 1
# print("over")
# i = 0
# while i <= 10:
#     if i == 3:
#         continue
#     print(i)
#     i += 1
row = 1
while row <= 9:
    col = 1
    while col <= row:
        print("%d x %d = %d" %(col, row, col * row),end="\t")
        col += 1
    print("")
    row += 1







