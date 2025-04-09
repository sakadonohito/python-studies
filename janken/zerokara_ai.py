#!/usr/bin/env python

from enum import IntEnum
import random

class Hand(IntEnum):
    GU = 0
    CHOKI = 1
    PA = 2

    @classmethod
    def from_str(cls, s):
        mapping = {"グー": cls.GU, "チョキ": cls.CHOKI, "パー": cls.PA}
        return mapping.get(s, None)

    def to_str(self):
        labels = {Hand.GU: "グー", Hand.CHOKI: "チョキ", Hand.PA: "パー"}
        return labels[self]

class Result(IntEnum):
    DRAW = 0
    PLAYER_WIN = 1
    AI_WIN = 2

    def to_str(self):
        labels = {
            Result.DRAW: "引き分け",
            Result.PLAYER_WIN: "あなたの勝ち",
            Result.AI_WIN: "AIの勝ち"
        }
        return labels[self]

# judge 関数の定義（明示的に判定）
def judge(ai, player):
    #return Result((player - ai) % 3)
    if ai == player:
        return Result.DRAW
    elif (ai == Hand.GU and player == Hand.CHOKI) or \
         (ai == Hand.CHOKI and player == Hand.PA) or \
         (ai == Hand.PA and player == Hand.GU):
        return Result.AI_WIN
    else:
        return Result.PLAYER_WIN


def get_player_choice(i):
    while True:
        choice = input(f"【第{i+1}戦】 あなたの手を入力してください(グー / チョキ / パー)：")
        hand = Hand.from_str(choice)
        if hand is not None:
            return hand
        print("※無効な入力です。グー / チョキ / パー のいずれかを入力してください！")

def get_ai_choice(recent_moves):
    if len(recent_moves) < 3:
        return random.choice(list(Hand))
    most_common = max(set(recent_moves), key=recent_moves.count)
    counter = {
        Hand.GU: Hand.PA,
        Hand.CHOKI: Hand.GU,
        Hand.PA: Hand.CHOKI
    }
    return counter[most_common]

def update_recent_moves(recent_moves, new_move, limit=5):
    recent_moves.append(new_move)
    if len(recent_moves) > limit:
        recent_moves.pop(0)

def main():
    recent_moves = []
    ai_wins = player_wins = draws = 0

    for i in range(10):
        ai_choice = get_ai_choice(recent_moves)
        player_choice = get_player_choice(i)
        update_recent_moves(recent_moves, player_choice)

        result = judge(ai_choice, player_choice)

        if result == Result.PLAYER_WIN:
            player_wins += 1
        elif result == Result.AI_WIN:
            ai_wins += 1
        else:
            draws += 1

        print(f"【第{i+1}戦】 AI: {ai_choice.to_str()} vs あなた: {player_choice.to_str()} -> {result.to_str()}！")

    print("\n 【最終結果】")
    print(f"AIの勝ち：{ai_wins}回")
    print(f"あなたの勝ち：{player_wins}回")
    print(f"引き分け：{draws}回")

if __name__ == "__main__":
    main()
