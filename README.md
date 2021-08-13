# open2021-1-phy3

3×3の正方形に並んだ9個の同位相波源による波面の様子が見られます。

波源間の最短距離をdとした時、波長λが

![\lambda=\frac{d}{\sqrt{m^2+n^2}}](https://latex.codecogs.com/gif.latex?\lambda=\frac{d}{\sqrt{m^2+n^2}})

(ただし、m,nは整数)

となれば、中央の波源を通る直線上に全ての波源による波が強め合う部分が現れます。

## 使い方
### 1. セットアップ

- ffmpegをインストール(動画の書き出しに必要)
- Pythonの依存ライブラリをインストール
    # 必要なら
    python3 -m venv env
    . ./env/bin/activate
    
    pip install -r requirements.txt
    
### 2. 実行
    python3 main.py
