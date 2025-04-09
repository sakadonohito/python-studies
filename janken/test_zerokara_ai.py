#!/usr/bin/env python

import pytest
from zerokara_ai import judge, get_ai_choice, get_player_choice, update_recent_moves, Hand, Result

# Hand enum のメソッドのテスト

def test_hand_to_str():
    assert Hand.GU.to_str() == "グー"
    assert Hand.CHOKI.to_str() == "チョキ"
    assert Hand.PA.to_str() == "パー"

def test_hand_from_str():
    assert Hand.from_str("グー") == Hand.GU
    assert Hand.from_str("チョキ") == Hand.CHOKI
    assert Hand.from_str("パー") == Hand.PA
    assert Hand.from_str("ピカチュウ") is None

# Result enum のメソッドのテスト

def test_result_to_str():
    assert Result.DRAW.to_str() == "引き分け"
    assert Result.PLAYER_WIN.to_str() == "あなたの勝ち"
    assert Result.AI_WIN.to_str() == "AIの勝ち"


# judge 関数のテスト

def test_judge_draw():
    assert judge(Hand.GU, Hand.GU) == Result.DRAW
    assert judge(Hand.CHOKI, Hand.CHOKI) == Result.DRAW
    assert judge(Hand.PA, Hand.PA) == Result.DRAW

def test_judge_ai_win():
    assert judge(Hand.GU, Hand.CHOKI) == Result.AI_WIN
    assert judge(Hand.CHOKI, Hand.PA) == Result.AI_WIN
    assert judge(Hand.PA, Hand.GU) == Result.AI_WIN

def test_judge_player_win():
    assert judge(Hand.GU, Hand.PA) == Result.PLAYER_WIN
    assert judge(Hand.CHOKI, Hand.GU) == Result.PLAYER_WIN
    assert judge(Hand.PA, Hand.CHOKI) == Result.PLAYER_WIN


# get_ai_choice 関数のテスト

def test_ai_choice_random_for_few_moves():
    for _ in range(10):
        choice = get_ai_choice([Hand.GU, Hand.CHOKI])
        assert choice in list(Hand)

def test_ai_choice_learns_most_common():
    # プレイヤーがチョキばかり出していた → AIはグーを出す
    recent_moves = [Hand.CHOKI, Hand.CHOKI, Hand.CHOKI, Hand.GU, Hand.CHOKI]
    assert get_ai_choice(recent_moves) == Hand.GU

    # プレイヤーがパーばかり → AIはチョキ
    recent_moves = [Hand.PA, Hand.PA, Hand.GU, Hand.PA, Hand.CHOKI]
    assert get_ai_choice(recent_moves) == Hand.CHOKI


# get_player_choice 関数のテスト

def test_get_player_choice_valid(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "グー")
    result = get_player_choice(0)
    assert result == Hand.GU

def test_get_player_choice_retry(monkeypatch):
    inputs = iter(["ピカチュウ", "チョキ"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = get_player_choice(1)
    assert result == Hand.CHOKI


# update_recent_moves 関数のテスト

def test_update_recent_moves():
    moves = [Hand.GU, Hand.PA, Hand.CHOKI, Hand.GU, Hand.CHOKI]
    update_recent_moves(moves, Hand.PA)
    assert moves == [Hand.PA, Hand.CHOKI, Hand.GU, Hand.CHOKI, Hand.PA]

    update_recent_moves(moves, Hand.GU)
    assert moves == [Hand.CHOKI, Hand.GU, Hand.CHOKI, Hand.PA, Hand.GU]
