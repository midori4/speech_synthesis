#!/bin/tcsh -f

set sp = mht

set natural_wavdir = ../../../../corpus/ATR/B-set/wav/16k/$sp/sd/a/
set world_wavdir = ../out/wav/world/$sp/
set modified_wavdir = ../out/wav/modified_ver/$sp/speech/

foreach wavfile (`ls $modified_wavdir -1`)
  set natural_wavfile = $natural_wavdir/$wavfile
  set world_wavfile = $world_wavdir/$wavfile
  set modified_wavfile = $modified_wavdir/$wavfile
  set outdir = ../out/analysis/power_comp/rmse
  python ../tool/power_rmse.py -n $natural_wavfile -w $world_wavfile -m $modified_wavfile -o $outdir
  
end
