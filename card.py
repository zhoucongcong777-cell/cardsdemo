import random
from enum import Enum
# from magic_cards import HealingPriest, FireMage


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

    def __str__(self):
        base = super().__str__()
        return f"{base}\n攻击力: {self.attack}, 生命值: {self.current_health}/{self.health}"

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