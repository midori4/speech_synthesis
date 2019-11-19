
script/impulse_train_check.sh
 - 連続F0からパルス列を生成する確認用
 - tool/pulse_train_generator.py を利用

script/impulse_responce_check.sh
 - スペクトル包絡と非周期性指標から、周期・非周期成分のインパルス応答を算出する確認用
 - tool/impulse_responce_generator.pyを利用

script/synthesis_check.sh
 - 連続F0、スペクトル包絡、非周期性指標から、音声を合成する動作確認用
 - 音源：tool/pulse_train_generator.py で生成されるパルス列 / 平均0、分散1の正規分布に従うホワイトノイズ
 - フィルタ：tool/impulse_responce_generator.pyにより生成される周期・非周期成分のインパルス応答
 - 周期成分：パルス列を周期成分のインパルス応答に畳み込み、非周期成分：ホワイトノイズを非周期成分のインパルス応答に畳み込み
 - 周期成分と非周期成分を加算することで、最終的な合成音声を得る

