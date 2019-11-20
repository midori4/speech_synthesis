# 音声パラメータ（基本周波数/スペクトル包絡/非周期性指標）を入力とする音声波形合成処理
音声の生成過程をモデル化したソースフィルタモデルに基づいて、音声波形を合成する。
合成処理は[WORLDボコーダ](https://github.com/mmorise/World)を参考にしたが、自動微分が可能なようにPyTorchを利用して記述してある。

## 処理概要
音声 <img src="https://latex.codecogs.com/gif.latex?x(t)" /> はソースフィルタモデルに倣うと、声帯の振動（音源）が喉や口といった筒（フィルタ）を通って音色付けされることにより生成されるとみなせる。音声パラメータはソースフィルタモデルに基づいており、以下の3種類のパラメータで音声を表現する。

* 基本周波数（F0）
  * 声の高さに相当するパラメータ
  * 声帯振動が伴っている（有声）区間では声帯振動の周波数を表す
  * 声帯振動が伴っていない（無音/無声）区間では値を持たない
  
* スペクトル包絡　<img src="https://latex.codecogs.com/gif.latex?|H(\omega)|" />
  * 音色（音韻/話者性）に関わるパラメータ
  * 喉や口の形状を表しており、声道フィルタに相当する

* 非周期性指標　<img src="https://latex.codecogs.com/gif.latex?A(\omega)" />
  * 音声に含まれるノイズの割合であり、0~1の値をとりうる
  * 0: 完全に周期的な音声、1: 完全に非周期的な音声

最終的には、これらの音声パラメータにより以下の式から音声が合成される。

<img src="https://latex.codecogs.com/gif.latex?x(t)=e(t)*h_p(t)+n(t)*h_a(t){}" />

ただし
* <img src="https://latex.codecogs.com/gif.latex?e(t)" />

  * 基本周期（F0の逆数）間隔のパルス列
  
* <img src="https://latex.codecogs.com/gif.latex?n(t)" />

  * ホワイトノイズ
  
* <img src="https://latex.codecogs.com/gif.latex?h_p(t)" />

  * 周期成分のインパルス応答
  * 振幅スペクトルは <img src="https://latex.codecogs.com/gif.latex?(1-A(\omega))|H(\omega)|" />
  * 位相は最小位相
  
* <img src="https://latex.codecogs.com/gif.latex?h_a(t)" />

  * 非周期成分のインパルス応答
  * 振幅スペクトルは <img src="https://latex.codecogs.com/gif.latex?A(\omega)|H(\omega)|" />
  * 位相は最小位相


## 部分部分の動作チェック
* `script/impulse_train_check.sh`
  * 連続F0からパルス列を生成する確認用
  * `tool/pulse_train_generator.py` を利用

* `script/impulse_responce_check.sh`
  * スペクトル包絡と非周期性指標から、周期・非周期成分のインパルス応答を算出する確認用
  * `tool/impulse_responce_generator.py`を利用

## 合成処理の実行
* `script/synthesis_check.sh`
  * 連続F0、スペクトル包絡、非周期性指標から、音声を合成する動作確認用
  * 音源：`tool/pulse_train_generator.py` で生成されるパルス列 / 平均0、分散1の正規分布に従うホワイトノイズ
  * フィルタ：tool/impulse_responce_generator.pyにより生成される周期・非周期成分のインパルス応答
  * 周期成分：パルス列を周期成分のインパルス応答に畳み込み、非周期成分：ホワイトノイズを非周期成分のインパルス応答に畳み込み
  * 周期成分と非周期成分を加算することで、最終的な合成音声を得る
