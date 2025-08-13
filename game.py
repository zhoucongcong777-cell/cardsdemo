from player import Player

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
        # TODO:此处可能有bug，双方血量可能同时低于0
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
                    unit_index = int(input("选择要出动的单位 (1-{}): ".format(len(self.current_player.field)))) - 1
                except ValueError:
                    print("无效的选择!")
                    continue
                self.opponent.health -= 2
                if self.current_player.attack(unit_index, self.opponent):
                    return  # 如果攻击导致对手死亡，游戏结束
            
            elif choice == 3:  # 结束回合
                break
            
            else:
                print("无效的选择!")




    