import random
from enum import Enum

class CardType(Enum):
    """卡牌类型枚举"""
    UNIT = "单位"   # 单位牌，可以放置在战场上
    MAGIC = "法术"  # 法术牌，使用后立即生效并进入墓地

class Card:
    """卡牌基类"""
    def __init__(self, name, card_type, description, cost=0):
        self.name = name
        self.type = card_type
        self.description = description
        self.cost = cost  # 打出卡牌所需的费用
    
    def __str__(self):
        return f"{self.name} ({self.type.value}) - 费用: {self.cost}\n描述: {self.description}"
    
    def on_draw(self, player, opponent):
        """抽取效果"""
        print(f"{player.name} 抽到了 {self.name}，但此卡没有抽取效果")
        return False
    
    def on_play(self, player, opponent):
        """打出效果"""
        print(f"{player.name} 打出了 {self.name}，但此卡没有特殊打出效果")
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

class Player:
    """玩家类"""
    def __init__(self, name):
        self.name = name
        self.deck = []
        self.hand = []
        self.field = []  # 战场上的单位
        self.mana = 0
        self.max_mana = 0
        self.health = 30
        self.initialize_deck()
    
    def initialize_deck(self):
        """初始化玩家的卡组"""
        # 添加单位卡
        self.deck.append(UnitCard("勇敢的士兵", "普通士兵单位", 2, 3, 3))
        self.deck.append(UnitCard("精锐弓箭手", "远程攻击单位", 3, 2, 2))
        self.deck.append(UnitCard("治疗牧师", "打出时治疗玩家3点生命", 4, 1, 4))
        self.deck.append(UnitCard("火焰法师", "打出时对敌方单位造成2点伤害", 5, 3, 3))
        self.deck.append(UnitCard("重装骑士", "高生命值单位", 6, 4, 6))
        
        # 添加法术卡
        self.deck.append(MagicCard("火球术", "对敌方玩家造成5点伤害", 3))
        self.deck.append(MagicCard("治疗之触", "恢复5点生命值", 2))
        self.deck.append(MagicCard("闪电链", "对所有敌方单位造成2点伤害", 4))
        self.deck.append(MagicCard("力量祝福", "使一个友方单位+2/+2", 1))
        self.deck.append(MagicCard("召唤援军", "抽两张牌", 2))
        
        # 洗牌
        random.shuffle(self.deck)
    
    def draw_card(self, opponent):
        """从卡组抽一张牌"""
        if not self.deck:
            print(f"{self.name}的卡组已空！")
            return False
        
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
        if card.on_play(self, opponent):
            # 根据卡牌类型处理
            if card.type == CardType.UNIT:
                print(f"{self.name} 在战场上召唤了 {card.name}！")
                self.field.append(card)
            elif card.type == CardType.MAGIC:
                print(f"{self.name} 使用了法术 {card.name}！")
            
            # 从手牌中移除
            self.hand.pop(card_index)
            return True
        return False
    
    def start_turn(self):
        """开始新回合"""
        self.max_mana = min(self.max_mana + 1, 10)
        self.mana = self.max_mana
        print(f"\n{self.name} 的回合开始！法力值: {self.mana}/{self.max_mana}")
    
    def display_status(self):
        """显示玩家状态"""
        print(f"\n{self.name} - 生命值: {self.health}  法力: {self.mana}/{self.max_mana}")
        print("战场上的单位:")
        for i, unit in enumerate(self.field):
            print(f"  {i+1}. {unit.name} ({unit.attack}/{unit.current_health})")
        
        print("\n手牌:")
        for i, card in enumerate(self.hand):
            print(f"  {i+1}. {card.name} ({card.type.value}, 费用: {card.cost})")
    
    def attack(self, attacker_index, opponent):
        """单位攻击"""
        if attacker_index < 0 or attacker_index >= len(self.field):
            print("无效的单位选择！")
            return False
        
        attacker = self.field[attacker_index]
        print(f"{attacker.name} 准备攻击！")
        
        # 攻击敌方玩家
        opponent.health -= attacker.attack
        print(f"{attacker.name} 对 {opponent.name} 造成了 {attacker.attack} 点伤害！")
        
        # 检查对手是否死亡
        if opponent.health <= 0:
            print(f"{opponent.name} 被击败了！")
            return True
        
        return False

class Game:
    """游戏主控制器"""
    def __init__(self):
        self.player1 = Player("玩家1")
        self.player2 = Player("玩家2")
        self.current_player = self.player1
        self.opponent = self.player2
        self.turn_count = 0
    
    def switch_players(self):
        """切换当前玩家"""
        self.current_player, self.opponent = self.opponent, self.current_player
    
    def start_game(self):
        """开始游戏"""
        print("===== 卡牌对战游戏开始! =====")
        
        # 初始抽牌
        for _ in range(3):
            self.player1.draw_card(self.player2)
            self.player2.draw_card(self.player1)
        
        # 游戏主循环
        while self.player1.health > 0 and self.player2.health > 0:
            self.turn_count += 1
            print(f"\n===== 回合 {self.turn_count} =====")
            
            # 当前玩家开始回合
            self.current_player.start_turn()
            
            # 抽牌阶段
            self.current_player.draw_card(self.opponent)
            
            # 主阶段
            self.main_phase()
            
            # 结束回合
            print(f"\n{self.current_player.name} 的回合结束")
            self.switch_players()
        
        # 游戏结束
        winner = self.player1 if self.player1.health > 0 else self.player2
        print(f"\n===== 游戏结束! =====\n{winner.name} 获胜!")
    
    def main_phase(self):
        """主阶段，玩家可以执行多个动作"""
        while True:
            self.current_player.display_status()
            
            print("\n可选操作:")
            print("1. 打出手牌")
            print("2. 使用单位攻击")
            print("3. 结束回合")
            
            try:
                choice = int(input("请选择操作: "))
            except ValueError:
                print("无效的选择!")
                continue
            
            if choice == 1:  # 打出手牌
                if not self.current_player.hand:
                    print("手牌为空!")
                    continue
                
                try:
                    card_index = int(input("选择要打出的卡牌 (1-{}): ".format(len(self.current_player.hand)))) - 1
                except ValueError:
                    print("无效的选择!")
                    continue
                
                self.current_player.play_card(card_index, self.opponent)
            
            elif choice == 2:  # 单位攻击
                if not self.current_player.field:
                    print("战场上没有单位!")
                    continue
                
                try:
                    unit_index = int(input("选择要攻击的单位 (1-{}): ".format(len(self.current_player.field)))) - 1
                except ValueError:
                    print("无效的选择!")
                    continue
                
                if self.current_player.attack(unit_index, self.opponent):
                    return  # 如果攻击导致对手死亡，游戏结束
            
            elif choice == 3:  # 结束回合
                break
            
            else:
                print("无效的选择!")

# 重写部分卡牌类以添加特殊效果
class HealingPriest(UnitCard):
    def on_play(self, player, opponent):
        """打出时治疗玩家3点生命"""
        player.health += 3
        print(f"{player.name} 恢复了 3 点生命值!")
        return super().on_play(player, opponent)

class FireMage(UnitCard):
    def on_play(self, player, opponent):
        """打出时对敌方单位造成2点伤害"""
        if opponent.field:
            target = random.choice(opponent.field)
            print(f"{self.name} 对 {target.name} 造成了 2 点伤害!")
            if target.take_damage(2):
                print(f"{target.name} 被消灭了!")
                opponent.field.remove(target)
        return super().on_play(player, opponent)

class FireballMagic(MagicCard):
    def on_play(self, player, opponent):
        """对敌方玩家造成5点伤害"""
        opponent.health -= 5
        print(f"{self.name} 对 {opponent.name} 造成了 5 点伤害!")
        return super().on_play(player, opponent)

class HealingTouchMagic(MagicCard):
    def on_play(self, player, opponent):
        """恢复5点生命值"""
        player.health += 5
        print(f"{player.name} 恢复了 5 点生命值!")
        return super().on_play(player, opponent)

class ChainLightningMagic(MagicCard):
    def on_play(self, player, opponent):
        """对所有敌方单位造成2点伤害"""
        print(f"{self.name} 对所有敌方单位造成了 2 点伤害!")
        for unit in opponent.field[:]:  # 使用副本遍历，因为可能会移除元素
            if unit.take_damage(2):
                print(f"{unit.name} 被消灭了!")
                opponent.field.remove(unit)
        return super().on_play(player, opponent)

class StrengthBuffMagic(MagicCard):
    def on_play(self, player, opponent):
        """使一个友方单位+2/+2"""
        if player.field:
            try:
                unit_index = int(input("选择要强化的单位 (1-{}): ".format(len(player.field)))) - 1
                if 0 <= unit_index < len(player.field):
                    unit = player.field[unit_index]
                    unit.attack += 2
                    unit.health += 2
                    unit.current_health += 2
                    print(f"{unit.name} 获得了 +2/+2 强化!")
                else:
                    print("无效的选择!")
            except ValueError:
                print("无效的选择!")
        else:
            print("战场上没有友方单位!")
        return super().on_play(player, opponent)

class ReinforcementsMagic(MagicCard):
    def on_draw(self, player, opponent):
        """抽到时抽一张额外的牌"""
        print(f"{self.name} 的抽取效果激活!")
        player.draw_card(opponent)
        return True
    
    def on_play(self, player, opponent):
        """打出时抽两张牌"""
        print(f"{self.name} 让 {player.name} 抽两张牌!")
        player.draw_card(opponent)
        player.draw_card(opponent)
        return super().on_play(player, opponent)

# 修改Player的initialize_deck方法以使用特殊卡牌
def initialize_deck_with_special_cards(self):
    """使用特殊效果的卡牌初始化玩家的卡组"""
    # 添加单位卡
    self.deck.append(UnitCard("勇敢的士兵", "普通士兵单位", 2, 3, 3))
    self.deck.append(UnitCard("精锐弓箭手", "远程攻击单位", 3, 2, 2))
    self.deck.append(HealingPriest("治疗牧师", "打出时治疗玩家3点生命", 4, 1, 4))
    self.deck.append(FireMage("火焰法师", "打出时对敌方单位造成2点伤害", 5, 3, 3))
    self.deck.append(UnitCard("重装骑士", "高生命值单位", 6, 4, 6))
    
    # 添加法术卡
    self.deck.append(FireballMagic("火球术", "对敌方玩家造成5点伤害", 3))
    self.deck.append(HealingTouchMagic("治疗之触", "恢复5点生命值", 2))
    self.deck.append(ChainLightningMagic("闪电链", "对所有敌方单位造成2点伤害", 4))
    self.deck.append(StrengthBuffMagic("力量祝福", "使一个友方单位+2/+2", 1))
    self.deck.append(ReinforcementsMagic("召唤援军", "抽到时抽一张牌，打出时抽两张牌", 2))
    
    # 洗牌
    random.shuffle(self.deck)

# 替换Player的initialize_deck方法
Player.initialize_deck = initialize_deck_with_special_cards

# 启动游戏
if __name__ == "__main__":
    game = Game()
    game.start_game()