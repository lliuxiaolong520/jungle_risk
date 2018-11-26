import random
import time
import item
import re


# 定义角色类(玩家, 猎物, 有血量,能攻击的)
class Role:

    # 特殊触发计算函数, 触发返回T,否则F
    @staticmethod
    def trigger(you_rate, enemy_rate=0):
        # 随机取值
        i = random.randint(1,1000)
        all_rate = you_rate * 10 - enemy_rate * 10
        # 触发
        if i <= all_rate:
            return True
        else:
            return False


    # 攻击方法
    def att(self, enemy):
        # 循环
        while True:
            print(self.name, "开始攻击")
            # 命中判断
            if self.trigger(self.hit_rate, enemy.dodge_rate):
                # 暴击判断
                if self.trigger(self.critical_rate):
                    # 暴击
                    print("暴击")
                    # 回气
                    if self.profession in ["战士", "刺客", "猎人"]:
                        self.player_recover_mp()
                        self.player_recover_mp()
                    if enemy.hurt(self, what_damage=2):
                        break
                else:
                    # 普通攻击
                    print("普通攻击")
                    if self.profession in ["战士", "刺客", "猎人"]:
                        self.player_recover_mp()
                    if enemy.hurt(self):
                        break

            # 未命中
            else:
                print("未命中")

        time.sleep(self.attack_speed)


    # 方法, 受伤类型默认为1普通,2暴击,3魔法, 死亡返回T,否则F
    def hurt(self, enemy, what_damage=1):
        # 伤害类型选项列表
        damage_list = {1: enemy.normal_damage, 2: enemy.critical_damage, 3: enemy.magic.damage}
        # 血量减少
        self.now_hp -= damage_list[what_damage] - self.armour * 1.2
        # 血量取整
        self.now_hp //= 1
        if self.now_hp <= 0:
            # 血量不能小于0
            self.now_hp = 0
            print("\n%s杀死了 %s" % (enemy.name, self.name))
            return True

        else:
            # 提示血量改变
            print("%s血量剩余%d" % (self.name, self.now_hp))
            return False

    # 魔法/怒气/集中值 回复方法, 每个职业不一样
    def player_recover_mp(self):
        pass




# 定义玩家类(战士,刺客,猎人,法师)
class Player(Role):
    # 属性
    def __init__(self):
        # 不可变属性
        # 名字
        self.name = ""
        # 职业
        self.profession = ""
        # 普通背包
        self.bag = []
        # 暴击系数
        self.critical_num = 1.8

        # 自改变属性
        # 武器属性
        self.weapon = "无"
        # 护甲属性
        self.armours1 = {
            1: "头盔",
            2: "肩甲",
            3: "胸甲",
            4: "护腕",
            5: "护腿",
            6: "鞋子"}

        self.armours2 = {
            1: "无",
            2: "无",
            3: "无",
            4: "无",
            5: "无",
            6: "无"}
        # 金币
        self.gold = 0
        # 背包最大格数
        self.bag_len = 20
        # 魔法属性
        self.magic = "无"
        # 等级
        self.grade = 1
        # 当前经验
        self.now_exp = 0
        # 升级所需经验 放等级后面
        self.nex_exp = (10 + 20 * (self.grade - 1)) * \
                       (20 + 20 * (self.grade - 1))
        # 力量
        self.strength = 0
        # 敏捷
        self.agility = 0
        # 体质
        self.constitution = 0
        # 智力
        self.intellect = 0
        # 最大魔法值------------法师
        self.max_mp = 100
        # 当前魔法值
        self.now_mp = self.max_mp
        # 命中率
        self.hit_rate = 80

        # 属性点影响
        # 暴击率
        self.critical_rate = 0
        # 攻击间隔
        self.attack_speed = 3.5
        # 普通攻击
        self.normal_damage = 0
        # 暴击攻击
        self.critical_damage = 0
        # 护甲
        self.armour = 0
        # 最大血量
        self.max_hp = 0
        # 当前血量
        self.now_hp = self.max_hp
        # 闪避概率
        self.dodge_rate = 0

    # 改变属性点后需要改变的属性
    def change_property(self):
        self.attack_speed = self.agility * 100 // 200 / 100
        self.critical_rate = self.agility * 10
        self.dodge_rate = self.agility * 10
        self.max_hp = self.constitution * 30
        self.armour = self.constitution
        if self.profession == "法师":
            if self.weapon == "无":
                self.normal_damage = self.intellect * 10
            else:
                self.normal_damage = self.intellect * 10 + self.weapon.damage
            self.max_hp = self.intellect * 4
        else:
            if self.weapon == "无":
                self.normal_damage = self.strength * 10
            else:
                self.normal_damage = self.strength * 10 + self.weapon.damage
        self.critical_damage = self.normal_damage * self.critical_num

    # 玩家升级获得的属性, 每个职业不一样
    def setup(self):
        pass

    # 玩家获取经验/升级方法
    def player_up_grade(self, enemy):
        # 最高100级
        if self.grade == 100:
            print("你已经满级了,不再获取经验")
        else:
            # 获取经验
            self.now_exp += enemy.now_exp
            print("\n%s获得经验%s" % (self.name, enemy.now_exp))

            # 判断是否够升级, 无限循环, 能测试连续升几级
            while True:
                if self.now_exp >= self.nex_exp:
                    # 升级后当前等级经验清空
                    self.now_exp -= self.nex_exp
                    # 等级+1
                    self.grade += 1
                    # 升下一级经验变化
                    self.nex_exp = (10 + 20 * (self.grade - 1)) * \
                                   (20 + 20 * (self.grade - 1))
                    # 提示信息
                    print("\n恭喜%s升级,当前等级为%s:" % (self.name, self.grade))
                    # 升级后属性变化方法
                    self.setup()
                # 不够升级,退出
                else:
                    break
            print("距离升级经验", self.nex_exp - self.now_exp)

    # 装备武器方法
    def get_weapon(self, weapon):
        # 判断是否达到武器需求

        # 判断是否已经装备武器
        if not self.weapon == "无":
            self.bag.append(self.weapon)
            print("\n卸下装备返回背包")
        self.weapon = weapon
        print("装备武器成功")
        # 改变武器提供的的属性
        self.normal_damage += weapon.damage
        self.attack_speed -= weapon.attack_speed
        self.critical_rate += weapon.critical_rate
        self.hit_rate += weapon.hit_rate

    # 装备护甲方法
    def get_armour(self, armour):

        # 判断是否存在装备
        if not self.armours[armour.part] == "无":
            self.bag.append(self.armours[armour.part])
            print("\n卸下装备返回背包")
        self.armours[armour.part] = armour
        print("装备护甲成功")
        # 改变装备提供的属性
        self.constitution += armour.constitution
        self.strength += armour.strength
        self.agility += armour.agility

    # 装备背包方法

    def get_bag(self, bag):
        self.bag_len += bag.bag_len
        print("\n你的背包增加到:", self.bag_len)
        print()

    # 使用背包物品方法
    def get_bag_item(self, bag_item):
        if bag_item.char == "武器":
            self.get_weapon(bag_item)
        elif bag_item.char == "护甲":
            self.get_armour(bag_item)
        elif bag_item.char == "背包":
            self.get_bag(bag_item)
        else:
            self.player_recover_hp(bag_item)

    # 装备魔法方法
    def get_magic(self, magic):
        self.magic = magic

    # 魔法/生命 回复
    def player_recover_hp(self, r_item):
        # 判断药瓶类型
        if r_item.char == "hp回复":
            self.now_hp += r_item.recover_hp
            print("\n生命回复成功")
            if self.now_hp >= self.max_hp:
                self.now_hp = self.max_hp
                print("\n你的生命已经回满!")

        elif r_item.char == "mp回复":
            self.now_mp += r_item.recover_mp
            print("\n魔法回复成功")
            if self.now_mp >= self.max_mp:
                self.now_mp = self.max_mp
                print("\n你的魔法已经回满!")

    # 玩家拾取物品方法
    def player_get_item(self, g_item):

        # 判断背包大小
        if len(self.bag) >= self.bag_len:
            print("你的背包已经装满")

        else:
            self.bag.append(g_item)

    # 详细信息
    def player_info(self):
        print("\n人物信息")
        print("\n姓名:%s\n等级:%s\n职业:%s\n生命")

    # 玩家加点方法  法师不适用

    def player_add_property(self):
        while True:
            if self.null <= 0:
                print("\n你没有多余的属性点了,退出")
                break
            else:
                print("\n你当前的属性值")
                print("\n1-力量:%s\n2-体质:%s\n3-敏捷:%s\n剩余加点:%s\n0-退出加点" %
                      (self.strength, self.constitution, self.agility, self.null))
                choice = input("\n请输入对应的选择: ")
                result = re.match("[0-3]$", choice)
                if result:
                    if choice == "0":
                        print("\n退出加点")
                        break
                    elif choice == "1":
                        self.strength += 1
                        self.null -= 1
                        print("\n你的力量增加了1点")
                    elif choice == "2":
                        self.constitution += 1
                        self.null -= 1
                        print("\n你的体质增加了1点")
                    else:
                        self.agility += 1
                        self.null -= 1
                        print("\n你的敏捷增加了1点")
                    # 普通攻击 力量*10
                    self.normal_damage = self.strength * 10
                    # 暴击伤害 普通*系数
                    self.critical_damage = self.normal_damage * self.critical_num
                    # 护甲 体质
                    self.armour = self.constitution
                    # 最大生命 体质*100+力量*20
                    self.max_hp = self.constitution * 100 + \
                        self.strength * 20 + 100 * (self.grade - 1)
                    # 闪避率
                    self.dodge_rate = self.agility * 0.2
                    self.critical_rate = self.agility * 0.2

                else:
                    print("\n请选择正确的属性点")


# 定义战士类
class Soldier(Player):

    def __init__(self, name):
        super().__init__(name)
        self.profession = "战士"

        # 属性点属性
        self.critical_rate = self.agility * 0.2
        self.normal_damage = self.strength * 10
        self.critical_damage = self.normal_damage * self.critical_num

        self.armour = self.constitution
        self.max_hp = self.constitution * 100 + \
            self.strength * 20 + 100 * (self.grade - 1)
        self.now_hp = self.max_hp
        self.dodge_rate = self.agility * 0.2
    # 玩家怒气回复方法

    def player_recover_ap(self):
        self.now_ap += 15
        # print("怒气回复 5 点")
        # 最大一百点, 防止溢出
        if self.now_ap >= 100:
            self.now_ap = 100


# 定义刺客类
class Assassinator(Player):

    def __init__(self, name):
        super().__init__(name)
        self.profession = "刺客"

        # 属性点属性
        self.strength = 3
        self.agility = 4
        self.constitution = 3

        self.attack_speed = 1.9 - 0.1 * self.agility

        self.now_ap = 100

        self.critical_rate = self.agility * 0.2
        self.normal_damage = self.strength * 10
        self.critical_damage = self.normal_damage * self.critical_num

        self.armour = self.constitution
        self.max_hp = self.constitution * 100 + \
            self.strength * 20 + 100 * (self.grade - 1)
        self.now_hp = self.max_hp
        self.dodge_rate = self.agility * 0.2

    # 怒气回复方法
    def player_recover_ap(self):
        self.now_ap += 5
        # print("集中值回复 2 点")
        # 最大一百点, 防止溢出
        if self.now_ap >= 100:
            self.now_ap = 100


# 定义猎人类
class Hunter(Player):

    def __init__(self, name):
        super().__init__(name)
        self.profession = "猎人"

        # 属性点属性
        self.strength = 4
        self.agility = 3
        self.constitution = 3

        self.attack_speed = 2.1 - 0.1 * self.agility

        self.now_ap = 100

        self.critical_rate = self.agility * 0.2
        self.normal_damage = self.strength * 10
        self.critical_damage = self.normal_damage * self.critical_num

        self.armour = self.constitution
        self.max_hp = self.constitution * 100 + \
            self.strength * 20 + 100 * (self.grade - 1)
        self.now_hp = self.max_hp
        self.dodge_rate = self.agility * 0.2

    # 怒气回复方法
    def player_recover_ap(self):
        self.now_ap += 5
        # print("集中值回复 2 点")
        # 最大一百点, 防止溢出
        if self.now_ap >= 100:
            self.now_ap = 100


# 定义法师类
class Rabbi(Player):

    def __init__(self, name):
        super().__init__(name)
        self.profession = "法师"

        self.strength = 0
        self.agility = 1
        self.constitution = 4
        self.intellect = 5

        self.attack_speed = 2.1 - 0.1 * self.agility

        self.normal_damage = self.intellect * 10
        self.max_mp = self.intellect * 8
        self.now_mp = self.max_mp

        self.critical_rate = self.agility * 0.2
        self.critical_damage = self.normal_damage * self.critical_num

        self.armour = self.constitution
        self.max_hp = self.constitution * 100 + 100 * (self.grade - 1)
        self.now_hp = self.max_hp
        self.dodge_rate = self.agility * 0.2

    # 简单讯息
    def sample_info(self):

        print(
            "\n名字:%s\n等级:%s\n职业:%s\n血量:%s\\%s\n攻击:%s\n智力:%s\n体质:%s\n敏捷:%s\n剩余加点:%s\n" %
            (self.name,
             self.grade,
             self.profession,
             self.now_hp,
             self.max_hp,
             self.normal_damage,
             self.intellect,
             self.constitution,
             self.agility,
             self.null))

    # 详细信息
    def all_info(self):
        print("\n基础信息")
        print(
            "\n姓名:%s\n职业:%s\n等级:%s\n距离下级经验:%s\n金币:%s\n" %
            (self.name,
             self.profession,
             self.grade,
             (self.nex_exp - self.now_exp),
             self.gold))
        print("\n装备信息")
        print("\n武器:%s\n技能:%s\n" %
              (self.weapon, self.magic))
        print("护甲信息\n")
        for a, b in self.armours.items():
            print(a + ":", b)
        print("\n属性点信息")
        print("\n智力:%s\n体质:%s\n敏捷:%s\n剩余加点:%s\n" %
              (self.intellect, self.constitution, self.agility, self.null))
        print("\n攻击属性")
        print(
            "\n攻击:%s\n攻击间隔:%s\n命中率:%s\n暴击率:%s\n" %
            (self.normal_damage,
             self.attack_speed,
             self.hit_rate,
             self.critical_rate))
        print("\n防御属性")
        print(
            "\n生命:%s\\%s\n魔法:%s\\%s\n护甲:%s\n闪避:%s\n" %
            (self.now_hp,
             self.max_hp,
             self.now_mp,
             self.max_mp,
             self.armour,
             self.dodge_rate))

    # 法师加点方法
    def player_add_property(self):
        while True:
            if self.null <= 0:
                print("\n你没有多余的属性点了,退出")
                break
            else:
                print("\n你当前的属性值")
                print(
                    "\n1-智力:%s\n2-体质:%s\n3-敏捷:%s\n剩余加点:%s\n0-退出加点" %
                    (self.intellect, self.constitution, self.agility, self.null))
                choice = input("\n请输入对应的选择: ")
                result = re.match("[0-3]$", choice)
                if result:
                    if choice == "0":
                        print("\n退出加点")
                        break
                    elif choice == "1":
                        self.intellect += 1
                        self.null -= 1
                        print("\n你的智力增加了1点")
                    elif choice == "2":
                        self.constitution += 1
                        self.null -= 1
                        print("\n你的体质增加了1点")
                    else:
                        self.agility += 1
                        self.null -= 1
                        print("\n你的敏捷增加了1点")
                    # 普通攻击 力量*10
                    self.normal_damage = self.intellect * 10
                    # 暴击伤害 普通*系数
                    self.critical_damage = self.normal_damage * self.critical_num
                    # 护甲 体质*10
                    self.armour = self.constitution
                    # 最大生命 体质*100+力量*20
                    self.max_hp = self.constitution * \
                        100 + 100 * (self.grade - 1)
                    # 闪避率 敏捷*2
                    self.dodge_rate = self.agility * 0.2
                    self.critical_rate = self.agility * 0.2
                    self.max_mp = self.intellect * 10

                else:
                    print("\n请选择正确的属性点")


# 定义猎物(普通, 精英)
class Quarry(Role):
    pass

# 定义普通猎物
class GeneralQuarry(Quarry):
    # 属性
    def __init__(self, grade):
        # 名称列表
        name_list = ["灰狼", "灰熊", "狗熊", "老虎", "野狗"]
        # 随机获取
        self.name = random.choice(name_list)
        # 等级
        self.grade = grade
        # 金币 掉落用
        self.gold = self.grade * random.randint(40, 50)
        # 经验 掉落用
        self.now_exp = self.grade * random.randint(16, 24) * 4
        # 物品掉落概率
        self.drop_rate = 30
        # 暴击
        self.critical_rate = 5 + (self.grade // 6) * 2
        # 暴击系数
        self.critical_num = 1.8
        # 普通攻击
        self.normal_damage = random.randint(
            10, 16) + (self.grade * random.randint(9, 15))
        # 暴击伤害
        self.critical_damage = self.normal_damage * self.critical_num
        # 命中
        self.hit_rate = 80
        # 攻击间隔
        self.attack_speed = 2.2 - (self.grade // 10) / 10
        # 魔法值 无
        self.mp = 0
        # 护甲
        self.armour = self.grade
        # 最大血量
        self.max_hp = random.randint(
            80, 90) + self.grade * random.randint(35, 58)
        # 当前血量
        self.now_hp = self.max_hp
        # 闪避
        self.dodge_rate = 5 + (self.grade // 5) * 2
        # 魔法技能
        self.magic = None
        # 类型
        self.profession = "普通"

    # 魔法受伤方法
    def enemy_magic_hurt(self, enemy):
        self.now_hp -= enemy.magic.damage

    # 猎物物品掉落方法

    def quarry_drop(self, enemy):
        time.sleep(0.2)

        # 生命药水掉落
        # 创建生命药水实例
        a = item.RecoverHp(self)
        # 狼随机掉落物品
        i = random.randint(1, 100)
        # 满足条件掉落
        if i <= self.drop_rate:
            # 设置掉落件数
            for _ in range(0, random.randint(1, 3)):
                a.create()
                # 调用敌人的拾取物品方法
                print("%s拾取到物品%s" % (enemy.name, a))
                enemy.player_get_item(a)

        # 魔法药水掉落
        b2 = item.RecoverMp(self)
        i = random.randint(1, 100)
        if i <= self.drop_rate:
            for _ in range(0, random.randint(1, 3)):

                b2.create()
                print("\n%s拾取到:\n%s" % (enemy.name, b2))
                enemy.player_get_item(b2)

        # 按特定等级掉落武器
        if self.grade % 5 == 0:

            i = random.randint(1, 100)
            if i <= self.drop_rate - 10:
                c = item.Armour(self.grade, enemy)
                c.create()
                print("\n%s拾取到:\n%s" % (enemy.name, c))
                enemy.player_get_item(c)

            i = random.randint(1, 100)
            if i <= self.drop_rate - 10:
                d = item.Weapon(self.grade, enemy)
                d.create()
                print("\n%s拾取到:\n%s" % (enemy.name, d))
                enemy.player_get_item(d)

        # 掉落背包

        i = random.randint(1, 100)
        if i <= self.drop_rate - 10:

            bag3 = item.Bag(self.grade, enemy)
            bag3.create()
            print("\n%s拾取到:\n%s" % (enemy.name, bag3))
            enemy.player_get_item(bag3)

    # 猎物普通受伤方法
    def enemy_hurt(self, enemy):
        time.sleep(0.2)
        # 血量减少
        self.now_hp -= enemy.normal_damage - self.armour
        # 判断是否死亡
        if self.now_hp <= 0:
            # 血量不能低于0
            self.now_hp = 0
            # 死亡提示
            print("\n%s杀死了 %s" % (enemy.name, self.name))
            # 猎物死亡会掉落装备 ,掉落方法
            self.quarry_drop(enemy)
            # 玩家获取金钱
            enemy.gold += self.gold
            print("\n%s拾取金币%s,当前拥有金币%s" % (enemy.name, self.gold, enemy.gold))
            # 玩家获取经验
            enemy.player_up_grade(self)
        else:
            # 没有死亡, 提示信息
            print("%s攻击--> %s血量剩余%d" % (enemy.name, self.name, self.now_hp))

    # 猎物暴击受伤方法
    def enemy_critical_hurt(self, enemy):
        time.sleep(0.2)
        print(enemy.name, "--> 致命一击.")
        # 血量减少
        self.now_hp -= enemy.critical_damage - self.armour * 1.5
        # 判断是否死亡
        if self.now_hp <= 0:
            # 血量不能低于0
            self.now_hp = 0
            # 死亡提示
            print("\n%s杀死了 %s" % (enemy.name, self.name))
            # 猎物死亡会掉落装备 ,掉落方法

            self.quarry_drop(enemy)
            # 玩家获取金钱
            enemy.gold += self.gold
            print("\n%s拾取金币%s,当前拥有金币%s" % (enemy.name, self.gold, enemy.gold))
            # 玩家获取经验
            enemy.player_up_grade(self)
        else:
            # 没有死亡
            print("%s攻击--> %s血量剩余%d" % (enemy.name, self.name, self.now_hp))

    # 信息
    def __str__(self):
        return "名称:%s\n等级:%s\n类型%s\n攻击:%s\n血量:%s\n护甲:%s\n" % (
            self.name, self.grade, self.type, self.normal_damage, self.max_hp, self.armour)



# 定义精英猎物
class HeadQuarry(Quarry):

    def __init__(self, grade):

        # 名称列表
        name_list = ["灰狼", "灰熊", "狗熊", "老虎", "野狗"]
        # 随机获取
        self.name = random.choice(name_list)
        # 等级
        self.grade = grade
        # 金币 掉落用
        self.gold = self.grade * random.randint(40, 60)
        # 经验 掉落用
        self.now_exp = self.grade * random.randint(16, 24) * 4
        # 物品掉落概率
        self.drop_rate = 30
        # 暴击
        self.critical_rate = self.grade / 2
        # 暴击系数
        self.critical_num = 1.8
        # 普通攻击
        self.normal_damage = random.randint(40, 60) * self.grade
        # 暴击伤害
        self.critical_damage = self.normal_damage * self.critical_num
        # 命中
        self.hit_rate = 80 + self.grade / 2
        # 攻击间隔
        self.attack_speed = 3.5 - (self.grade * 100 // 40) / 100
        # 魔法值 无
        self.mp = 0
        # 护甲
        self.armour = self.grade
        # 最大血量
        self.max_hp = random.randint(
            80, 90) + self.grade * random.randint(35, 58)
        # 当前血量
        self.now_hp = self.max_hp
        # 闪避
        self.dodge_rate = 5 + (self.grade // 5) * 2
        # 魔法技能
        self.magic = None
        # 类型
        self.profession = "普通"

    # 魔法受伤方法
    def enemy_magic_hurt(self, enemy):
        self.now_hp -= enemy.magic.damage

    # 猎物物品掉落方法

    def quarry_drop(self, enemy):
        time.sleep(0.2)

        # 生命药水掉落
        # 创建生命药水实例
        a = item.RecoverHp(self)
        # 狼随机掉落物品
        i = random.randint(1, 100)
        # 满足条件掉落
        if i <= self.drop_rate:
            # 设置掉落件数
            for _ in range(0, random.randint(1, 3)):
                a.create()
                # 调用敌人的拾取物品方法
                print("%s拾取到物品%s" % (enemy.name, a))
                enemy.player_get_item(a)

        # 魔法药水掉落
        b2 = item.RecoverMp(self)
        i = random.randint(1, 100)
        if i <= self.drop_rate:
            for _ in range(0, random.randint(1, 3)):

                b2.create()
                print("\n%s拾取到:\n%s" % (enemy.name, b2))
                enemy.player_get_item(b2)

        # 按特定等级掉落武器
        if self.grade % 5 == 0:

            i = random.randint(1, 100)
            if i <= self.drop_rate - 10:
                c = item.Armour(self.grade, enemy)
                c.create()
                print("\n%s拾取到:\n%s" % (enemy.name, c))
                enemy.player_get_item(c)

            i = random.randint(1, 100)
            if i <= self.drop_rate - 10:
                d = item.Weapon(self.grade, enemy)
                d.create()
                print("\n%s拾取到:\n%s" % (enemy.name, d))
                enemy.player_get_item(d)

        # 掉落背包

        i = random.randint(1, 100)
        if i <= self.drop_rate - 10:

            bag3 = item.Bag(self.grade, enemy)
            bag3.create()
            print("\n%s拾取到:\n%s" % (enemy.name, bag3))
            enemy.player_get_item(bag3)

    # 猎物普通受伤方法
    def enemy_hurt(self, enemy):
        time.sleep(0.2)
        # 血量减少
        self.now_hp -= enemy.normal_damage - self.armour
        # 判断是否死亡
        if self.now_hp <= 0:
            # 血量不能低于0
            self.now_hp = 0
            # 死亡提示
            print("\n%s杀死了 %s" % (enemy.name, self.name))
            # 猎物死亡会掉落装备 ,掉落方法
            self.quarry_drop(enemy)
            # 玩家获取金钱
            enemy.gold += self.gold
            print("\n%s拾取金币%s,当前拥有金币%s" % (enemy.name, self.gold, enemy.gold))
            # 玩家获取经验
            enemy.player_up_grade(self)
        else:
            # 没有死亡, 提示信息
            print("%s攻击--> %s血量剩余%d" % (enemy.name, self.name, self.now_hp))

    # 猎物暴击受伤方法
    def enemy_critical_hurt(self, enemy):
        time.sleep(0.2)
        print(enemy.name, "--> 致命一击.")
        # 血量减少
        self.now_hp -= enemy.critical_damage - self.armour * 1.5
        # 判断是否死亡
        if self.now_hp <= 0:
            # 血量不能低于0
            self.now_hp = 0
            # 死亡提示
            print("\n%s杀死了 %s" % (enemy.name, self.name))
            # 猎物死亡会掉落装备 ,掉落方法

            self.quarry_drop(enemy)
            # 玩家获取金钱
            enemy.gold += self.gold
            print("\n%s拾取金币%s,当前拥有金币%s" % (enemy.name, self.gold, enemy.gold))
            # 玩家获取经验
            enemy.player_up_grade(self)
        else:
            # 没有死亡
            print("%s攻击--> %s血量剩余%d" % (enemy.name, self.name, self.now_hp))

    # 信息
    def __str__(self):
        return "名称:%s\n等级:%s\n类型%s\n攻击:%s\n血量:%s\n护甲:%s\n" % (
            self.name, self.grade, self.type, self.normal_damage, self.max_hp, self.armour)



# if __name__ == '__main__':

    # # 创建一个角色
    # test = Soldier("liu")
    # # 等级60
    # test.grade = 50
    # # 创建一个武器
    # weapon = item.Weapon(50)
    # weapon.create()
    #
    # # 创建一个装备
    # for i in range(3):
    #     hu = item.Armour(50)
    #     hu.create()
    #     test.armour_bag.append(hu)
    #
    # a = test.armour_bag[1]
    #
    # # 创建猎物
    # wolf = Quarry(40)
    #
    # # 创建药瓶
    # recover = item.RecoverMp(wolf)
    # recover.create()
    #
    #
    #
    # test.get_bag_item(weapon)
    # test.get_bag_item(a)
    # test.get_bag_item(recover)
    #
    #
    # test.all_info()
