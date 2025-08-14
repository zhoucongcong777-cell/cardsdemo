import random
from enum import Enum

# class Position(Enum):
#     """单位位置类型枚举"""
#     FRONT = "前线"   
#     BACK = "后方"    


class CardType(Enum):
    """卡牌大类"""
    UNIT = "单位"
    MAGIC = "法术"


 
class Card:
    """卡牌细类"""
    def __init__(self,name,card_type,description,cost=0):
        self.name = name
        self.type = card_type
        self.description = description
        self.cost = cost

    def __str__(self):
        return f"{self.name} ({self.type.value}) - 费用:{self.cost}\n描述:{self.describtion}"

    #  def __str__(self):
    #     position = f", 位置: {self.position.value}" if hasattr(self, 'position') else ""
    #     return f"{self.name} ({self.type.value}) - 费用: {self.cost}{position}\n描述: {self.description}"
    
    def on_draw(self,player,opponent):
        """抽取效果"""
        print(f"{player.name} 抽到了 {self.name}, 但是此卡没有特殊抽取效果")
        return False

    def on_play(self,player,opponent):
        """打出效果"""
        print(f"{player.name} 打出了 {self.name}")
        return True

class UnitCard(Card):
    """单位卡牌"""
    def __init__(self, name, description, cost, attack, health):
        super().__init__(name, CardType.UNIT, description, cost)
        self.attack = attack
        self.health = health
        self.current_health = health    
        self.has_moved = False  # 添加移动状态标记        how
        self.position = None    # 添加位置标记

        # self.position = position

    def __str__(self):
        base = super().__str__()
        position_info = f", 位置: {self.position}" if self.position else ""
        return f"{base}\n攻击力: {self.attack}, 生命值: {self.current_health}/{self.health}{position_info}"


    def take_damage(self, amount):
        """单位受到伤害"""
        self.current_health -= amount
        if self.current_health <= 0:
            return True  # 单位死亡
        return False

class MagicCard(Card):
    """法术卡牌"""
    def __init__(self, name, description, cost):
        super().__init__(name, CardType.MAGIC, description, cost)