#!/bin/tcsh -f

set interp_lf0 = /disk/fs1/bigtmp/nose/Demo/F0_interp/linear/tool/interp_lf0.pl
# extract F0 using REAPER algorithm set by /disk/fs1/bigtmp/hayasaka/study/m_thesis/world_anasyn_tool/config.py
set analysis = /disk/fs1/bigtmp/hayasaka/study/m_thesis/PyWorld_anasyn_demo/tool/analysis.py
set synthesis = /disk/fs1/bigtmp/hayasaka/study/m_thesis/PyWorld_anasyn_demo/tool/synthesis.py

set sp = mht
set subset = a
set natural_wav_dir = ../../../../corpus/ATR/B-set/wav/16k/$sp/sd/$subset/

set speech_param_dir = ../data/acoustic_feature/$sp/$subset
mkdir -p $speech_param_dir
 
set outdir = ../out/wav/modified_ver/$sp
set world_wavdir = ../out/wav/world/$sp/
mkdir -p $world_wavdir


set gpu_id = 0
# ----------------------------------------------------

# ---- WORLD default param ----
set l_limit = 71.0 # lower limit F0 [Hz]
set u_limit = 800.0 # upper limit F0 [Hz]
# ---- WORLD default param ----

# Threshold for aperiodicity-based voiced/unvoiced decision, in range 0 to 1.
# WORLD default: 0.85
set ap_threshold = 0.0

set sampling_freq = 16000 # [Hz]
set frame_period = 5 # [ms]

foreach wavfilename (`ls $natural_wav_dir -1`)
# foreach wavfilename (mhtsda01.wav)
  set wavfile = $natural_wav_dir/$wavfilename
  
  set f0 = `echo $speech_param_dir/$wavfilename | sed s/.wav/.f0/g`
  set sp = `echo $speech_param_dir/$wavfilename | sed s/.wav/.sp/g`
  set ap = `echo $speech_param_dir/$wavfilename | sed s/.wav/.ap/g`
  set lf0 = `echo $speech_param_dir/$wavfilename | sed s/.wav/.lf0/g`
  set ilf0 = `echo $speech_param_dir/$wavfilename | sed s/.wav/.ilf0/g`
  set world_anasyn_wav = $world_wavdir/$wavfilename
  
  python $analysis -L $l_limit -U $u_limit -t $ap_threshold -s $sp -a $ap -f $f0 -i $wavfile --world
  python $synthesis -s $sp -a $ap -f $f0 -o $world_anasyn_wav --world
  python $analysis -L $l_limit -U $u_limit -t $ap_threshold -f $lf0 -i $wavfile
  
  $interp_lf0 $lf0 | x2x +af > $ilf0
  
  set PYTHONPATH = ../tool 
  python ../tool/synthesis_check.py -f $sampling_freq -p $frame_period -l $l_limit -i $ilf0 -s $sp -a $ap -o $outdir -g $gpu_id
end
# ----------------------------------------------------
