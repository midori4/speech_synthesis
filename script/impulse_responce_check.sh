#!/bin/tcsh -f

set analysis = /disk/fs1/bigtmp/hayasaka/anasyn_wav/tool/analysis.py

set wavfile = ../data/phone_a/hayasaka.wav
set acoustic_feature_dir = ../data/phone_a/acoustic_feature
mkdir -p $acoustic_feature_dir

# 特に意味はない（中間ファイルとして抽出されてしまうだけで使わない）
set f0 = $acoustic_feature_dir/hayasaka.f0
# ------------------------------------------------------------------

set sp = $acoustic_feature_dir/hayasaka.sp
set ap = $acoustic_feature_dir/hayasaka.ap

python $analysis -s $sp -a $ap -f $f0 -i $wavfile -world

set outdir = ../out/pre_check/impulse_responce
set gpu_id = 1
python ../tool/impulse_responce_check.py -s $sp -a $ap -o $outdir -g $gpu_id
