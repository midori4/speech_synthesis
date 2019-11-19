#!/bin/tcsh -f

# extract F0 using REAPER algorithm set by /disk/fs1/bigtmp/hayasaka/study/m_thesis/world_anasyn_tool/config.py
set analysis = /disk/fs1/bigtmp/hayasaka/study/m_thesis/world_anasyn_tool/analysis.py

set sp = mht
set natural_wavdir = ../../../../corpus/ATR/B-set/wav/16k/$sp/sd/a/
set world_wavdir = ../out/wav/world/$sp/
set modified_wavdir = ../out/wav/modified_ver/$sp/speech/

set outdir = ../out/analysis/f0_comp/total/$sp/
mkdir -p $outdir/emf # emf file (for powerpoint)
mkdir -p $outdir/natural
mkdir -p $outdir/world
mkdir -p $outdir/modified_ver

# ---- WORLD default param ----
set l_limit = 71.0 # lower limit F0 [Hz]
set u_limit = 800.0 # upper limit F0 [Hz]
# ---- WORLD default param ----

# foreach wavfile (`ls $modified_wavdir -1`)
foreach wavfile (mhtsda01.wav)
  set natural_wavfile = $natural_wavdir/$wavfile
  set world_wavfile = $world_wavdir/$wavfile
  set modified_wavfile = $modified_wavdir/$wavfile
  set natural_lf0 = `echo $outdir/natural/$wavfile | sed s/.wav/.lf0/g`
  set world_lf0 = `echo $outdir/world/$wavfile | sed s/.wav/.lf0/g`
  set modified_lf0 = `echo $outdir/modified_ver/$wavfile | sed s/.wav/.lf0/g`
  # python $analysis -L $l_limit -U $u_limit -f $natural_lf0 -i $natural_wavfile
  # python $analysis -L $l_limit -U $u_limit -f $world_lf0 -i $world_wavfile
  # python $analysis -L $l_limit -U $u_limit -f $modified_lf0 -i $modified_wavfile

  # python ../tool/f0_comp.py -n $natural_lf0 -w $world_lf0 -m $modified_lf0 -o $outdir
  
  set svgfile = `echo $outdir/svg/$wavfile | sed s/.wav/.svg/g`
  set emffile = `echo $outdir/emf/$wavfile | sed s/.wav/.emf/g`
  inkscape $svgfile -M $emffile
end
