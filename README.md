# open2021-1-phy3

3×3の正方形に並んだ9個の同位相波源による波面の様子が見られるPythonスクリプトです。

波源間の最短距離をdとした時、波長λが

![\lambda=\frac{d}{\sqrt{m^2+n^2}}](https://latex.codecogs.com/gif.latex?\lambda=\frac{d}{\sqrt{m^2+n^2}})

(ただし、m,nは整数)

となれば、中央の波源を通る直線上に全ての波源による波が強め合う部分が現れます。

## 使い方
### 1. セットアップ

- ffmpegをインストール(動画の書き出しに必要)
- Pythonの依存ライブラリをインストール
    ```bash
    (必要なら)
    python3 -m venv env
    . ./env/bin/activate
    
    pip install -r requirements.txt
    ```
    
### 2. 実行
    python3 main.py

## 動作確認環境
- Ubuntu 20.04.2 LTS x86_64
- Python 3.8.10
- ffmpeg 4.2.4-1ubuntu0.1
