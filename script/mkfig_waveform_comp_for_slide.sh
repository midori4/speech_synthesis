#!/bin/tcsh -f

set natural_speech_wavfile = ../../../../corpus/ATR/B-set/wav/16k/mht/sd/a/mhtsda01.wav
set world_anasyn_speech_wavfile = ../out/wav/world/mht/mhtsda01.wav
set modified_anasyn_speech_wavfile = ../out/wav/modified_ver/mht/speech/mhtsda01.wav
set triphone_label_file = ../../../../corpus/ATR/triphone_label/mht/sd/mhtsda01.lab

set outdir = ../out/analysis/waveform_comp_for_document

python ../tool/mkfig_waveform_comp_for_slide.py \
  -n $natural_speech_wavfile -w $world_anasyn_speech_wavfile -m $modified_anasyn_speech_wavfile -l $triphone_label_file -o $outdir

