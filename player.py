from card import UnitCard, MagicCard, CardType

import random

from magic_cards import *

class Player:
    """玩家类"""
    def __init__(self, name):
        self.name = name
        self.deck = []    #玩家尚未抽到的卡组
        self.hand = []    #玩家的手牌
        # self.field = []   # 战场上的单位
        self.mana = 0     
        self.max_mana = 0
        self.health = 30
        self.initialize_deck()
        # self.front_line = []  # 前线单位(暂时空)
        # self.back_line = []   # 后方单位


    def initialize_deck(self):
        """初始化玩家的卡组"""
        # 添加单位卡
        self.deck.append(BraveSoldier("勇敢的士兵", "普通士兵单位", 0, 3, 3))
        self.deck.append(EagleEye("精锐弓箭手", "远程攻击单位", 0, 3, 2))
        self.deck.append(HealingPriest("治疗牧师", "打出时治疗玩家3点生命", 0, 1, 4))
        self.deck.append(FireMage("火焰法师", "打出时对敌方单位造成2点伤害", 0, 4, 3))
        self.deck.append(HeavyKnight("重装骑士", "高生命值单位", 0, 4, 7))
        
        # 添加法术卡
        self.deck.append(FireballMagic("火球术", "对敌方玩家造成5点伤害", 0))
        self.deck.append(HealingTouchMagic("治疗之触", "恢复5点生命值", 0))
        self.deck.append(ChainLightningMagic("闪电链", "对所有敌方单位造成2点伤害", 0))
        self.deck.append(StrengthBuffMagic("力量祝福", "使一个友方单位+2/+2", 0))
        self.deck.append(ReinforcementsMagic("召唤援军", "抽两张牌", 0))
        
        # 洗牌
        random.shuffle(self.deck)

    def draw_card(self, opponent):
        """从卡组抽一张牌"""
        if not self.deck:
            print(f"{self.name}的卡组已空！")
            return False
    
        else:
            card = self.deck.pop()
            self.hand.append(card)
            print(f"{self.name} 抽到了: {card.name}")
        
           # 触发抽取效果
            card.on_draw(self, opponent)
            return True

    def play_card(self, card_index, opponent):
        """打出一张手牌"""
        if card_index < 0 or card_index >= len(self.hand):
            print("无效的卡牌选择！")
            return False
        
        card = self.hand[card_index]
        
        # 检查是否有足够的费用
        if card.cost > self.mana:
            print(f"费用不足！需要 {card.cost} 点法力，当前有 {self.mana} 点")
            return False
        
        # 消耗费用
        self.mana -= card.cost
        
        # 触发打出效果
        card.on_play(self, opponent)
        # if card.on_play(self, opponent):
            # # 根据卡牌类型处理
            # if card.type == CardType.UNIT:
            #     self.back_line.append(card)
            #     print(f"{self.name} 在后方部署了 {card.name}！")
            #     print("_"*20)
            #     self.field.append(card)
            # elif card.type == CardType.MAGIC:
            #     print(f"{self.name} 使用了法术 {card.name}！")     
        
        # 从手牌中移除
        self.hand.pop(card_index)
        # return True
        return card  #i dont know


        
      
    def start_turn(self):
        """开始新回合"""
        self.max_mana = min(self.max_mana + 1, 10)
        self.mana = self.max_mana
        print(f"\n{self.name} 的回合开始！法力值: {self.mana}/{self.max_mana}")
    
    def display_status(self):
        """显示玩家状态"""
        print(f"\n{self.name} - 生命值: {self.health}  法力: {self.mana}/{self.max_mana}")
        # print("战场上的单位:")
        # for i, unit in enumerate(self.field):
        #     print(f"{i+1}.{unit.name} ({unit.cost}-{unit.attack}-{unit.current_health}/{unit.health})", end=" ^ ^ ^")
        
        print("\n手牌:")
        for i, card in enumerate(self.hand):
            print(f"{i+1} {card.name} ({card.type.value}, 费用: {card.cost})", end="|" )
        print()
    # def remove_dead_units(self):
    #     """移除死亡的战场单位"""
    #     self.front_line = [unit for unit in self.front_line if unit.current_health > 0]
    #     self.back_line = [unit for unit in self.back_line if unit.current_health > 0]
    
    # def get_all_units(self):
    #     """获取所有战场单位"""
    #     return self.front_line + self.back_line
    


    # def attack(self, attacker_index, opponent):
    #     """单位攻击"""
    #     if attacker_index < 0 or attacker_index >= len(self.field):
    #         print("无效的单位选择！")
    #         return False
        
    #     attacker = self.field[attacker_index]
    #     print(f"{attacker.name} 准备攻击！")
        
    #     # 攻击敌方玩家
    #     opponent.health -= attacker.attack
    #     print(f"{attacker.name} 对 {opponent.name} 造成了 {attacker.attack} 点伤害！")
        
    #     # 检查对手是否死亡
    #     if opponent.health <= 0:
    #         print(f"{opponent.name} 被击败了！")
    #         return True

    #     return False