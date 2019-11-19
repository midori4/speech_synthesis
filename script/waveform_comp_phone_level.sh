#!/bin/tcsh -f

set sp = mht # speaker

set natural_wavdir = ../../../../corpus/ATR/B-set/wav/16k/$sp/sd/a/
set world_wavdir = ../out/wav/world/$sp/
set modified_wavdir = ../out/wav/modified_ver/$sp/speech/
set triphone_labdir = ../../../../corpus/ATR/triphone_label/$sp/sd/

foreach wavfile (`ls $modified_wavdir -1`)
  set natural_wavfile = $natural_wavdir/$wavfile
  set world_wavfile = $world_wavdir/$wavfile
  set modified_wavfile = $modified_wavdir/$wavfile
  set base_filename = `echo $wavfile | sed s/.wav//g`
  set triphone_labfile = $triphone_labdir/$base_filename.lab
  set outdir = ../out/analysis/waveform_comp_phone_level/$sp/$base_filename
  
  python ../tool/waveform_comp_phone_level.py \
    -n $natural_wavfile -w $world_wavfile -m $modified_wavfile -l $triphone_labfile -o $outdir
  
  foreach svgfile (`ls $outdir/natural/*.svg -1`)
    set emffile = `echo $svgfile | sed s/.svg/.emf/g`
    inkscape $svgfile -M $emffile
  end
  
  foreach svgfile (`ls $outdir/world/*.svg -1`)
    set emffile = `echo $svgfile | sed s/.svg/.emf/g`
    inkscape $svgfile -M $emffile
  end
  
  foreach svgfile (`ls $outdir/modified/*.svg -1`)
    set emffile = `echo $svgfile | sed s/.svg/.emf/g`
    inkscape $svgfile -M $emffile
  end
end
