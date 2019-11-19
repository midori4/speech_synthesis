#!/bin/tcsh -f

set sp = mht

set natural_wavdir = ../../../../corpus/ATR/B-set/wav/16k/$sp/sd/a/
set world_wavdir = ../out/world_anasyn_wav/$sp
set modified_wavdir = ../out/synthesis_check/$sp/synthesis/

foreach wavfile (`ls $modified_wavdir -1`)
  set natural_wavfile = $natural_wavdir/$wavfile
  set world_wavfile = $world_wavdir/$wavfile
  set modified_wavfile = $modified_wavdir/$wavfile
  set outdir = `echo ../out/power_comp/scatter/$wavfile | sed s/.wav//g`
  python ../tool/power_scatter.py -n $natural_wavfile -w $world_wavfile -m $modified_wavfile -o $outdir
  
  set svgfile = $outdir/power_comp.svg
  set emffile = `echo $svgfile | sed s/.svg/.emf/g`
  inkscape $svgfile -M $emffile
end
