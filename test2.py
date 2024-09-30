import sys

global a
global people
global result
def stdinNum():
    for line in sys.stdin:
        global a
        a = line.split(" ")
        a[a.__len__()-1] = a[a.__len__()-1].split("\n")[0];
        break

def stdinPeople():
    for line in sys.stdin:
        global people
        people = line.split(" ")
        people[people.__len__()-1] = people[people.__len__()-1].split("\n")[0];
        break
    # print(people)

def stdinMoney():
    for line in sys.stdin:
        money = line.split(" ")
        money[people.__len__()-1] = money[people.__len__()-1].split("\n")[0];
        break

    costMoney = int(money[0])
    if(a[0] == 0):
        e = use92and5(costMoney)
        printmin(e[0], e[1])
        return
    if a[1] == 0:
        c = use10and5(costMoney)
        printmin(c[0], c[1])
        return

    if a[2] == 0:
        b = use92and10(costMoney)
        d = use10and92(costMoney)
        minNum = min( b[0], d[0])
        if minNum == b[0]:
            printmin(b[0], b[1])
        if minNum == d[0]:
            printmin(d[0], d[1])
        return

    e = use92and5(costMoney)
    b = use92and10(costMoney)
    c = use10and5(costMoney)
    d = use10and92(costMoney)
    minNum = min(e[0],b[0],c[0],d[0])

    if minNum == e[0]:
        printmin(e[0],e[1])

    if minNum == b[0]:
        printmin(b[0],b[1])

    if minNum == c[0]:
        printmin(c[0],c[1])

    if minNum == d[0]:
        printmin(d[0],d[1])

def printmin(a,b):
    print(str(a)+" "+str(b))

# a[1]
def bonus92(costMoney):
    return int(0.92*costMoney)

# a[0]
def bonus10(costMoney):
    return costMoney - 10

# a[2]
def bonus5(costMoney):
    return costMoney - 5

def use92and10(costMoney):
    costTicket = 0
    result = [3,3]
    times = int(costMoney / 100)
    # print("可以用满减" + str(times) + "次")
    if int(a[0]) < times:
        times = int(a[0])

    if int(a[1]) != 0:
        costMoney = bonus92(costMoney)
        costTicket += 1
        # print("用了一张打折")

    for i in range(times):
        costMoney = bonus10(costMoney)
        costTicket += 1
        # print("用了一张满减")

    result[0] = costMoney
    result[1] = costTicket
    return result

def use10and92(costMoney):
    costTicket = 0
    result = [3,3]

    times = int(costMoney / 100)
    if int(a[0]) < times:
        times = int(a[0])

    for i in range(times):
        costMoney = bonus10(costMoney)
        costTicket += 1

    if int(a[1]) != 0:
        costMoney = bonus92(costMoney)
        costTicket += 1

    result[0] = costMoney
    result[1] = costTicket
    return result


def use10and5(costMoney):
    costTicket = 0
    times = int(costMoney / 100)
    result = [3,3]
    if int(a[0]) < times:
        times = int(a[0])

    for i in range(times):
        costMoney = bonus10(costMoney)
        costTicket += 1

    for i in range(int(a[2])):
        costMoney = bonus5(costMoney)
        costTicket += 1
        # print("用了一张满减")

    result[0] = costMoney
    result[1] = costTicket
    return result

def use92and5(costMoney):
    costTicket = 0
    result = [3,3]
    if int(a[1]) != 0:
        costMoney = bonus92(costMoney)
        costTicket += 1
        # print("用了一张打折")

    for i in range(int(a[2])):
        costMoney = bonus5(costMoney)
        costTicket += 1
        # print("用了一张满减")

    result[0] = costMoney
    result[1] = costTicket
    return result

if __name__ == "__main__":
    # print(5/0.08) # 62.5以上，用92折都是赚的。
    # print(10 / 0.08) # 125 以上，用92折都是赚的，单张。
    # print(30 / 0.08) # 375 以上，用92折都是赚的，单张
    stdinNum()
    stdinPeople()
    # print(people)
    for i in range(int(people[0])):
        stdinMoney()
