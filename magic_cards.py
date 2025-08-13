from card import UnitCard, MagicCard
import random
# 重写部分卡牌类以添加特殊效果
class HealingPriest(UnitCard):
    def on_play(self, player, opponent):
        """打出时治疗玩家3点生命"""
        player.health -= 3
        print(f"{player.name} 扣了 3 点生命值!")
        return super().on_play(player, opponent)

# class HealingPriest(UnitCard):
#     def on_play(self, player, opponent):
#         """打出时治疗玩家3点生命"""
#         player.health += 3
#         print(f"{player.name} 恢复了 3 点生命值!")
#         return super().on_play(player, opponent)        

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

# class ChainLightningMagic(MagicCard):
#     def on_play(self, player, opponent):
#         """对所有敌方单位造成2点伤害"""
#         print(f"{self.name} 对所有敌方单位造成了 2 点伤害!")
#         for unit in opponent.field[:]:  # 使用副本遍历，因为可能会移除元素
#             if unit.take_damage(2):
#                 print(f"{unit.name} 被消灭了!")
#                 opponent.field.remove(unit)
#         return super().on_play(player, opponent)

# class StrengthBuffMagic(MagicCard):
#     def on_play(self, player, opponent):
#         """使一个友方单位+2/+2"""
#         if player.field:
#             try:
#                 unit_index = int(input("选择要强化的单位 (1-{}): ".format(len(player.field)))) - 1
#                 if 0 <= unit_index < len(player.field):
#                     unit = player.field[unit_index]
#                     unit.attack += 2
#                     unit.health += 2
#                     unit.current_health += 2
#                     print(f"{unit.name} 获得了 +2/+2 强化!")
#                 else:
#                     print("无效的选择!")
#             except ValueError:
#                 print("无效的选择!")
#         else:
#             print("战场上没有友方单位!")
#         return super().on_play(player, opponent)

# class ReinforcementsMagic(MagicCard):
#     def on_draw(self, player, opponent):
#         """抽到时抽一张额外的牌"""
#         print(f"{self.name} 的抽取效果激活!")
#         player.draw_card(opponent)
#         return True
    
#     def on_play(self, player, opponent):
#         """打出时抽两张牌"""
#         print(f"{self.name} 让 {player.name} 抽两张牌!")
#         player.draw_card(opponent)
#         player.draw_card(opponent)
#         return super().on_play(player, opponent)
