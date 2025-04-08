#!/usr/bin/env python

import random

def judge(ai, player):
    if ai == player:
        return "引き分け"
    win_patterns = {
        "グー": "チョキ",
        "チョキ": "パー",
        "パー": "グー"
    }
    return "AIの勝ち" if win_patterns[ai] == player else "あなたの勝ち"

def get_player_choice(i, hands):
    while True:
        choice = input(f"【第{i+1}戦】 あなたの手を入力してください(グー / チョキ / パー)：")
        if choice in hands:
            return choice
        # 無効な入力の場合、whileを抜けられない
        print("※無効な入力です。グー / チョキ / パー のいずれかを入力してください！")

def get_ai_choice(recent_moves, hands):
    if len(recent_moves) < 3: # 最初の3回はランダム
        return random.choice(hands)
    # 直近の手を学習(最新5回のデータを使う)
    most_common = max(set(recent_moves), key=recent_moves.count)
    counter = {"グー": "パー", "チョキ": "グー", "パー": "チョキ"}
    return counter[most_common]

def update_recent_moves(recent_moves, new_move, limit=5):
    recent_moves.append(new_move)
    # 古いデータを削除し、最新5回だけ残す
    if len(recent_moves) > limit:
        recent_moves.pop(0)


def main():

    #じゃんけんの手を定義
    hands = ["グー","チョキ","パー"]

    # AIの学習用(最新5回の手を記録)
    recent_moves = []

    # 勝敗カウント用変数
    ai_wins = player_wins = draws = 0

    # 10回対戦(AI vs User)
    for i in range(10):
        # AIの手の選び方(学習を続ける)
        ai_choice = get_ai_choice(recent_moves, hands)

        # プレイヤーの手を入力
        player_choice = get_player_choice(i, hands)

        # プレイヤーの手を記録(最新5回のみ保持)
        update_recent_moves(recent_moves, player_choice)

        # 勝敗判定
        result = judge(ai_choice, player_choice)
        if result == "引き分け":
            draws += 1
        elif result == "AIの勝ち":
            ai_wins += 1
        else:
            player_wins += 1

        # 対戦ごとの結果を表示
        print(f"【第{i+1}戦】 AI: {ai_choice} vs あなた: {player_choice} -> {result}！")

    # 最終結果を表示
    print("\n 【最終結果】")
    print(f"AIの勝ち：{ai_wins}回")
    print(f"あなたの勝ち：{player_wins}回")
    print(f"引き分け：{draws}回")

if __name__ == "__main__":
    main()
