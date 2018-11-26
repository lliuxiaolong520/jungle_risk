import re
import item
import role
import time
import random
import magic


# 分割线
cut_line = "*" * 30

# 定义角色全局变量
now_player = None

# 存储选项和对应的菜单函数
menu = {}


# 定义装饰器
def add_menu(choice):
    def function(func):
        def interface(*args, **kwargs):
            func(*args, **kwargs)
            return now_player
        menu[choice] = interface
        return interface
    return function


# 主界面
def main_interface():
    # 循环, 每个界面都循环, 只设定一个出口
    while True:
        # 提示功能
        print(cut_line)
        if now_player is None:
            print("\n你好,旅行者,这里是冒险大世界")
        else:
            print(
                "\n你好 %s(等级:%d) 这里是冒险大世界" %
                (now_player.name, now_player.grade))
        msg = """\n1.新建角色\n2.人物属性\n3.查看背包\n4.神秘空间\n5.金币商店\n6.丛林冒险\n7.保存游戏\n8.读取存档\n0.退出冒险"""
        print(msg)
        # 接收 并返回输入
        choice = input("\n请输入你的选择：")
        return choice


# 新建角色界面
@add_menu("1")
def new_player():
    print(cut_line)
    # 判断 角色存在不能进入
    if now_player is not None:
        print("\n玩家已存在,不能新建,请退出后重试")
    else:
        while True:
            # 功能提示
            msg = """\n你好,旅行者！\n欢迎加入丛林冒险,请选择你的职业\n1.战士\n防御较高.\n2.刺客\n敏捷较高.\n3.猎人\n能力均衡.\n4.法师\n攻击爆表!\n0.退出角色新建\n"""
            print(msg)
            # 职业储存
            roles_list = {"1": "战士", "2": "刺客", "3": "猎人", "4": "法师"}
            # 提示输入
            choice = input("\n请选择你的的职业(1-4)：")
            # 判断输入
            # 退出
            if choice == "0":
                print("\n退出角色新建")
                break
            # 职业正确输入
            if choice in roles_list.keys():
                # 提示职业
                print("\n你选择的职业是:", roles_list[choice])
                # 循环输入名字
                while True:
                    # 接收输入
                    name_player = input("\n请输入角色名字(2-6个字符):")
                    print(cut_line)
                    # 匹配输入
                    result2 = re.match(r"^\w{2,6}$", name_player)
                    # 名字输入正确 开始建立角色
                    if result2:
                        # 建立职业对应类的字典
                        player_list = {
                            "1": role.Soldier,
                            "2": role.Assassinator,
                            "3": role.Hunter,
                            "4": role.Rabbi}
                        # 改变全局变量,申明
                        global now_player
                        # 创建角色
                        now_player = player_list[choice](name_player)
                        # 提示初始信息
                        print("\n你的初始信息如下")
                        now_player.sample_info()
                        # 新建成功,退出界面
                        break
                    # 名字错误 重新输入
                    else:
                        print("\n请输入正确的名字")
            # 职业选择错误
            else:
                print("\n请选择正确的职业")


# 人物属性
@add_menu("2")
def player_property():
    print(cut_line)
    # 判断玩家是否存在
    if now_player is None:
        print("\n玩家不存在,请先创建一个角色")
    else:
        while True:
            # 提示功能
            print("\n你好", now_player.name, "欢迎查看人物属性")
            print("\n1.人物信息\n2.武器信息\n3.装备信息\n4.技能信息\n0.退出人物属性界面")
            # 创建选项-功能字典
            choice_list = {}
            # TODO

            # 调用人物方法

            now_player.all_info()
            # 判断是否加点
            if now_player.null > 0:
                a = input("\n你有未添加的属性,是否添加,1确认, 0返回: ")
                print(cut_line)
                if a == "0":
                    pass
                elif a == "1":
                    now_player.player_add_property()
                else:
                    pass


# 玩家背包
@add_menu("3")
def bag():


    while True:
        print(cut_line)
        # 里面判断, 防止使用完物品,报错
        if len(now_player.bag) == 0:
            print("\n你还没有获得材料\n")
            break
        else:
            print("\n材料背包, 空间: %s\\%s" %
                  (len(now_player.bag), now_player.bag_len))
            print(
                "\n你当前生命值:%.0f\\%s" %
                (now_player.now_hp,
                 now_player.max_hp),
                end="\n\n")

            if now_player.profession == "法师":
                print(
                    "你当前法力值:%.0f\\%s" %
                    (now_player.now_mp,
                     now_player.max_mp),
                    end="\n\n")

            for index, item1 in enumerate(now_player.bag, 1):
                print(index, str(item1.grade) + "级 " + item1.name)
            print("0.退出背包查看")
            long_1 = len(now_player.bag)
            a = input("\n请选择你要使用的物品: ")
            print(cut_line)
            if a.isdecimal():
                a = int(a)
                if 0 <= a <= long_1:
                    if a == 0:
                        print("\n退出背包成功\n")
                        return now_player
                    else:
                        print("\n你选择的是:")
                        print(now_player.bag[a - 1])
                        b = input("\n输入 1 使用, 2 出售, 0或任意键取消: ")
                        print(cut_line)
                        if b == "1":

                            if now_player.grade < now_player.bag[a - 1].grade:
                                print("\n等级不够")
                            else:
                                now_player.get_bag_item(now_player.bag[a - 1])
                                del now_player.bag[a - 1]

                        elif b == "2":
                            # 先获取金币 ,在删除
                            now_player.gold += now_player.bag[a - 1].gold
                            print("\n出售成功,获得金币%s, 当前拥有金币%s" %
                                  (now_player.bag[a - 1].gold, now_player.gold))
                            del now_player.bag[a - 1]
                        else:
                            print("\n取消使用物品")
                else:
                    print("\n请选择一个正确的物品")
            else:
                print("\n请选择一个正确的物品")


# 金币商店
@add_menu("5")
def shop(now_player):
    print(cut_line)
    # 五级以上开放
    if now_player.grade < 5:
        print("\n商店五级开放\n")
    # 判断时间进入
    else:
        a = time.time()
        c = int(a % 10)
        if 0 < c < 4:
            print("\n欢迎光临")
            print("\n你当前有金币:", now_player.gold)
            print("\n商店物品如下")
            # 设置商店产品等级
            need = (now_player.grade // 5) * 5
            # 商店物品列表
            list1 = []
            # 添加4个武器在列表中
            for i in range(4):
                # 创建武器实例
                weapon = item.Weapon(need, now_player)
                weapon.create()
                list1.append(weapon)
            # 添加5个护甲在商品中
            for i in range(5):
                # 创建护甲实例对象
                armour = item.Armour(need, now_player)
                armour.create()
                list1.append(armour)

            while True:
                # 打印出产品列表
                for index, shop_item in enumerate(list1, 1):
                    print(index, "%d级 %s %s" %
                          (shop_item.grade, shop_item.ranking, shop_item.name))
                # 接收玩家输入选择
                choice = input("\n输入编号查看详情, 0 退出商店:")
                print(cut_line)

                if choice.isdecimal:
                    if choice == "0":
                        return now_player
                    else:
                        choice = int(choice) - 1
                        if 0 <= choice < len(list1):
                            # 打印出选择装备的详情
                            choice_item = list1[choice]
                            print("\n武器属性")
                            print(choice_item)
                            # 判断玩家的金币是否足够
                            if now_player.gold < choice_item.sale_gold:
                                print("\n你的金币不足")
                                print(cut_line)
                            else:
                                choice2 = input("\n1.购买装备\n0.返回商店")
                                print(cut_line)
                                # 匹配输入是否是0-9的数字
                                result = re.match("[01]$", choice2)
                                if result:
                                    if choice2 == "0":
                                        pass
                                        # break
                                    else:
                                        # 购买, 减少金币
                                        now_player.gold -= choice_item.sale_gold
                                        print("购买成功")
                                        now_player.player_get_item(choice_item)

                                        del list1[choice]

                                else:
                                    print("\n有误,请重新输入")

                        else:
                            print("\n请选择正确的商品")

                else:
                    print("\n请选择正确的商品")
                    print(cut_line)

        else:
            print("\n天色已晚,商店关门")


# 丛林冒险
@add_menu("6")
def go_jungle(now_player):

    print(cut_line)
    print("\n你好", now_player.name, ",欢迎进入丛林\n\n在这里你可以选择不同难度的地图进入冒险!")
    print("\n你当前的等级是:", now_player.grade)
    msg = "\n请输入你要去冒险的森林等级, 0返回主菜单: "

    while True:

        choice = input(msg)

        if choice.isdecimal():
            choice = int(choice)
            if choice > 60:
                choice = 60
            if choice == 0:
                return now_player

            while True:
                if now_player.now_hp <= 100:
                    print("\n血量太低,不能进入")
                    return now_player
                else:
                    print(cut_line)
                    print("\n寻找中...")
                    time.sleep(2)
                    print("\n发现一只落单的猎物\n")
                    wolf = role.Quarry(choice)
                    print(wolf)
                    print("你当前攻击:", now_player.normal_damage)
                    print(
                        "你当前生命值:%.0f\\%s" %
                        (now_player.now_hp,
                         now_player.max_hp))

                    if now_player.profession == "法师":
                        print(
                            "你当前法力值:%.0f\\%s" %
                            (now_player.now_mp, now_player.max_mp))

                    a = input("\n是否攻击,1确定, 0返回: ")
                    if a == "1":
                        print(cut_line)
                        if now_player.profession == "战士":
                            now_player.now_ap = 0
                        if now_player.profession in ["刺客", "猎人"]:
                            now_player.now_ap = 100
                        now_player.player_fighting(wolf)
                    else:
                        print("\n猎物凶猛, 返回\n")
                        break

            break

        else:
            print("\n请输入正确的等级")


# 保存游戏
@add_menu("7")
def save(now_player):
    pass




# 读取存档
@add_menu("8")
def load(now_player):
    pass



# 神秘空间
@add_menu("4")
def mysterious_space(now_player):
    print(cut_line)

    if now_player.grade == now_player.enter_grade:
        now_player.enter_grade += 5

        print("\n神秘人: 你好,", now_player.name)
        print("\n神秘人: 相聚就是有缘, 送你一本绝世秘籍吧!")

        # 创建魔法
        tem_magic = magic.Magic(now_player)
        tem_magic.create()
        print()
        print(tem_magic)
        print("\n你获得绝世秘籍一本")
        print("\n学习中..., 你两眼一黑, 顿时晕了过去...")

        now_player.magic = tem_magic
        return now_player

    elif now_player.grade > now_player.enter_grade:
        now_player.enter_grade += 5
        print("\n少侠一定错过了什么, 下次再来试试..")
        return now_player

    else:
        print("\n你还没看清那人长相,便被人%s了出来" %
              random.choice(["踢", "请", "吹", "赶", "踹"]))
        print("\n你发誓回去后一定勤学苦练...\n")
    return now_player
