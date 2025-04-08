#!/usr/bin/env python

import pytest
from zerokara_ai import judge

def test_judge_draw():
    assert judge("グー","グー") == "引き分け"
    assert judge("チョキ","チョキ") == "引き分け"
    assert judge("パー","パー") == "引き分け"

def test_judge_ai_win():
    assert judge("グー","チョキ") == "AIの勝ち"
    assert judge("チョキ","パー") == "AIの勝ち"
    assert judge("パー","グー") == "AIの勝ち"

def test_judge_player_win():
    assert judge("グー","パー") == "あなたの勝ち"
    assert judge("チョキ","グー") == "あなたの勝ち"
    assert judge("パー","チョキ") == "あなたの勝ち"


from zerokara_ai import get_ai_choice

def test_ai_choice_random_for_few_moves(monkeypatch):
    # 2回未満の履歴 → ランダム（選択肢に含まれるか）
    hands = ["グー", "チョキ", "パー"]
    for _ in range(10):
        choice = get_ai_choice(["グー", "チョキ"], hands)
        assert choice in hands

def test_ai_choice_learns_most_common():
    hands = ["グー", "チョキ", "パー"]

    # プレイヤーがチョキばかり出していた → AIはグーを出す
    recent_moves = ["チョキ", "チョキ", "チョキ", "グー", "チョキ"]
    assert get_ai_choice(recent_moves, hands) == "グー"

    # プレイヤーがパーばかり → AIはチョキ
    recent_moves = ["パー", "パー", "グー", "パー", "チョキ"]
    assert get_ai_choice(recent_moves, hands) == "チョキ"


from zerokara_ai import get_player_choice

def test_get_player_choice_valid(monkeypatch):
    # 有効な入力が1回目で与えられたケース
    monkeypatch.setattr('builtins.input', lambda _: "グー")
    result = get_player_choice(0, ["グー", "チョキ", "パー"])
    assert result == "グー"

def test_get_player_choice_retry(monkeypatch):
    # 最初は無効、次に有効な入力が来た場合
    inputs = iter(["ピカチュウ", "チョキ"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = get_player_choice(1, ["グー", "チョキ", "パー"])
    assert result == "チョキ"


from zerokara_ai import update_recent_moves

def test_update_recent_moves():
    moves = ["グー", "パー", "チョキ", "グー", "チョキ"]
    update_recent_moves(moves, "パー")
    assert moves == ["パー", "チョキ", "グー", "チョキ", "パー"]  # 古い"グー"が消える

    update_recent_moves(moves, "グー")
    assert moves == ["チョキ", "グー", "チョキ", "パー", "グー"]

