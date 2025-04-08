#!/usr/bin/env python

import gymnasium as gym

def main():

    env = gym.make("CartPole-v1", render_mode="human")  # ローカルならhumanでOK # window描画の場合
    #env = gym.make("CartPole-v1", render_mode="rgb_array") # Colabで動かす,動画として保存,AIに画像入力したい場合
    obs, info = env.reset()

    for _ in range(1000):
        env.render()
        frame = env.render()
        print(frame) # 画像のピクセル値（整数の配列）# e.g. [[[255 255 255]...] [[255 255 255]...]...]
        #print(frame.shape) # NumPy配列のサイズ（高さ, 幅, 色チャンネル）# e.g. (400, 600, 3)

        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        #print(obs)
        if terminated or truncated:
            obs, info = env.reset()

    env.close()


if __name__ == "__main__":
    main()
