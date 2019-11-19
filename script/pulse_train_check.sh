#!/bin/tcsh -f

# F0：REAPERにより抽出

set interp_lf0 = /disk/fs1/bigtmp/nose/Demo/F0_interp/linear/tool/interp_lf0.pl
set analysis = /disk/fs1/bigtmp/hayasaka/anasyn_wav/tool/analysis.py

set wavfile = ../data/phone_a/hayasaka.wav
set acoustic_feature_dir = ../data/phone_a/acoustic_feature
mkdir -p $acoustic_feature_dir

# 特に意味はない（中間ファイルとして抽出されてしまうだけで使わない）
set lf0 = $acoustic_feature_dir/hayasaka.lf0
set mcep = $acoustic_feature_dir/hayasaka.mcep
set bap = $acoustic_feature_dir/hayasaka.bap
set mcep_order = 24 
# ------------------------------------------------------------------

# interpolated log-F0 save file
set ilf0 = $acoustic_feature_dir/hayasaka.ilf0

python $analysis -m $mcep_order  -s $mcep -a $bap -f $lf0 -i $wavfile

$interp_lf0 $lf0 | x2x +af > $ilf0

set outdir = ../out/pre_check/pulse_train
python ../tool/pulse_train_check.py -i $ilf0 -o $outdir
