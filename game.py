from player import Player
from card import CardType

class Game:
    """游戏主控制器"""
    def __init__(self):
        self.player1 = Player("同盟国")
        self.player2 = Player("轴心国")
        self.current_player = self.player1
        self.opponent = self.player2
        self.turn_count = 0

        # 统一管理战场状态
        self.battlefields = {
            self.player1: {
                'frontline': [],  # 前线区域
                'backline': []    # 后方区域
            },
            self.player2: {
                'frontline': [],
                'backline': []
            }
        }

    
    def switch_players(self):
        """切换当前玩家"""
        self.current_player, self.opponent = self.opponent, self.current_player
    
    def start_game(self):
        """开始游戏"""
        print("===== 类kards卡牌对战游戏开始! =====")
        print("同盟国 vs 轴心国")

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
        # TODO:此处可能有bug，双方血量可能同时低于0
        winner = self.player1 if self.player1.health > 0 else self.player2
        print(f"\n===== 游戏结束! =====\n{winner.name} 获胜!")

    def main_phase(self):
        """主阶段，玩家可以执行多个动作"""
        while True:
            self.display_battlefield()
            self.current_player.display_status()
            print("\n|############################|")
            print("|可选操作:                   |")
            print("|1. 打出手牌                 |")
            print("|2. 使用单位攻击             |")
            print("|3.移动单位到前线            |")
            print("|4. 结束回合                 |")
            print("|############################|")

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

                # 获取卡牌引用
                card_to_play = self.current_player.hand[card_index]
                
                # 尝试打出卡牌
                played_card = self.current_player.play_card(card_index, self.opponent)
                
                # 检查是否成功打出单位卡
                if played_card and played_card.type == CardType.UNIT:
                    self.summon_minion(self.current_player, played_card, 'backline')
                    print(f"{self.current_player.name} 在后方部署了 {played_card.name}！")
            
            elif choice == 2:  # 单位攻击
                # 获取当前玩家所有前线单位
                frontline_units = self.battlefields[self.current_player]['frontline']
                if not frontline_units:
                    print("前线没有可攻击的单位!")
                    continue
                
                try:
                    unit_index = int(input("选择要出动的单位 (1-{}): ".format(len(frontline_units)))) - 1
                    if unit_index < 0 or unit_index >= len(frontline_units):
                        print("无效的选择!")
                        continue
                except ValueError:
                    print("无效的选择!")
                    continue
                
                # 执行攻击
                attacker = frontline_units[unit_index]
                self.opponent.health -= attacker.attack
                print(f"{attacker.name} 对 {self.opponent.name} 造成了 {attacker.attack} 点伤害！")
                
                # 检查对手是否死亡
                if self.opponent.health <= 0:
                    print(f"{self.opponent.name} 被击败了！")
                    return
                
                
                
            
            elif choice == 3:  #移动单位
                # 获取当前玩家所有后方单位
                backline_units = self.battlefields[self.current_player]['backline']
                if not backline_units:
                    print("后方没有可移动的单位!")
                    continue
                
                try:
                    unit_index = int(input("选择要移动到前线的单位 (1-{}): ".format(len(backline_units)))) - 1
                    if unit_index < 0 or unit_index >= len(backline_units):
                        print("无效的选择!")
                        continue
                except ValueError:
                    print("无效的选择!")
                    continue
                
                # 执行移动
                minion = backline_units[unit_index]
                self.move_to_frontline(self.current_player, minion)
            
            elif choice == 4:  # 结束回合
                break

            else:
                print("无效的选择!")

            #移除死亡单位
            self.remove_dead_units()

    def summon_minion(self, player, minion, position='backline'):
        """召唤随从到指定位置"""
        battlefield = self.battlefields[player]
        
        if position not in ['frontline', 'backline']:
            raise ValueError("Invalid position")
        
        battlefield[position].append(minion)
        minion.position = position
        minion.has_moved = (position == 'frontline')  # 前线单位已移动过
    
    def move_to_frontline(self, player, minion):
        """将随从移动到前线，无需对方同意"""
        battlefield = self.battlefields[player]
        
        # 检查随从是否在后方
        if minion not in battlefield['backline']:
            print(f"{minion.name} 不在后方!")
            return False
        
        # 检查是否已经移动过
        if minion.has_moved:
            print(f"{minion.name} 本回合已经移动过!")
            return False
        
        # 执行移动
        battlefield['backline'].remove(minion)
        battlefield['frontline'].append(minion)
        
        # 更新随从状态
        minion.position = 'frontline'
        minion.has_moved = True
        
        print(f"{player.name} 将 {minion.name} 移动到了前线!")
        return True
    
    def remove_dead_units(self):
        """移除所有死亡的单位"""
        for player in [self.player1, self.player2]:
            battlefield = self.battlefields[player]
            
            # 检查前线单位
            for position in ['frontline', 'backline']:
                # 使用副本遍历，避免修改列表时出错
                for minion in battlefield[position][:]:
                    if minion.current_health <= 0:
                        print(f"{minion.name} 被消灭了!")
                        battlefield[position].remove(minion)


    def display_battlefield(self):
        """显示KARDS风格的战场布局"""
        # # 清屏（模拟）
        # print("\n" * )
        
        # 战场宽度
        width = 100
        
        # 1. 敌方大本营
        print("=" * width)
        print(f"{self.opponent.name.upper()} HQ [生命值: {self.opponent.health}]".center(width))
        print("=" * width)
        
        # 2. 敌方后方单位
        print(f"{self.opponent.name} 后方单位:".center(width))
        backline_units = self.battlefields[self.opponent]['backline']
        if backline_units:
            for unit in backline_units:
                unit_info = f"{unit.name} ({unit.attack}/{unit.current_health})"
                print(unit_info.center(width))
        
        else:
            print("(无单位)".center(width))
        # print(f"{self.opponent.name} 后方单位:".center(width))
        # if self.opponent.back_line:
        #     for i, unit in enumerate(self.opponent.back_line):
        #         unit_info = f"{unit.name} ({unit.attack}/{unit.current_health})"
        #         print(unit_info.center(width))
        # else:
        #     print("(无单位)".center(width))
        # # print("-" * width)
        
        # 3. 前线
        print(" FRONT LINE ".center(width, "="))
        frontline_units = self.battlefields[self.opponent]['frontline'] + self.battlefields[self.current_player]['frontline']
        if frontline_units:
            for unit in frontline_units:
                owner = self.opponent.name if unit in self.battlefields[self.opponent]['frontline'] else self.current_player.name
                unit_info = f"[{owner}] {unit.name} ({unit.attack}/{unit.current_health})"
                print(unit_info.center(width))
        
        else:
            print("(无单位)".center(width))
        print("=" * width)

        # 4. 我方后方单位
        print(f"{self.current_player.name} 后方单位:".center(width))
        backline_units = self.battlefields[self.current_player]['backline']

        # if self.current_player.back_line:
        #     for i, unit in enumerate(self.current_player.back_line):
        #         unit_info = f"{unit.name} ({unit.attack}/{unit.current_health})"
        #         print(unit_info.center(width))
        if backline_units:
            for unit in backline_units:
                unit_info = f"{unit.name} ({unit.attack}/{unit.current_health})"
                print(unit_info.center(width))

        else:
            print("(无单位)".center(width))
        # print("-" * width)
        
        # 5. 我方大本营
        print("=" * width)
        print(f"{self.current_player.name.upper()} HQ [生命值: {self.current_player.health}]".center(width))
        print("=" * width)





    