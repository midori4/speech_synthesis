#!/bin/tcsh -f

set sp = mht

set natural_wavdir = ../../../../corpus/ATR/B-set/wav/16k/$sp/sd/a/
set world_wavdir = ../out/wav/world/$sp/
set modified_wavdir = ../out/wav/modified_ver/$sp/speech/

set outdir = ../out/analysis/power_comp/total
mkdir -p $outdir/emf # emf file (for powerpoint)

# foreach wavfile (`ls $modified_wavdir -1`)
foreach wavfile (mhtsda01.wav)
  set natural_wavfile = $natural_wavdir/$wavfile
  set world_wavfile = $world_wavdir/$wavfile
  set modified_wavfile = $modified_wavdir/$wavfile
  # python ../tool/power_comp.py -n $natural_wavfile -w $world_wavfile -m $modified_wavfile -o $outdir
  
  set svgfile = `echo $outdir/svg/$wavfile | sed s/.wav/.svg/g`
  set emffile = `echo $outdir/emf/$wavfile | sed s/.wav/.emf/g`
  inkscape $svgfile -M $emffile
end
