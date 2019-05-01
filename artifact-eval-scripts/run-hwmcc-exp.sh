#!/bin/bash
root=$HOME/tool
bin=$root/bin
bench=$root/bench
run=$root/run
graphs=$root/graphs/hwmcc-exp
mkdir -p $graphs

time=30m
years=(14 15 17)
f=""

solvers=(kavy avy vanilla abcpdr)

for y in "${years[@]}"
do
  benchFile=$bench/$y/benchmarks.txt
  for sol in "${solvers[@]}"
  do
  
     out=$root/out/hwmcc-exp/$sol/$y
     mkdir -p $out
     
     export bin out bench run time benchFile sol
          
     $run/run-on-files.sh
     python $run/brunch/spacer/log_scrab.py -o $graphs/$sol-$y.csv $out
  
  done
done

for sol in "${solvers[@]}"
do
  out=$root/out/hwmcc-exp/$sol
  f="$f $graphs/$sol.csv"
  python $run/brunch/spacer/log_scrab.py -o $graphs/$sol.csv $out
done
python $run/brunch/spacer/cactusCombine.py -f $f -o $graphs/hwmcc-cactus.png
python $un/brunch/spacer/ScatterPlots-ae.py -f1 $graphs/kavy.csv -f2 $graphs/avy.csv -o $graphs
python $un/brunch/spacer/ScatterPlots-ae.py -f1 $graphs/kavy.csv -f2 $graphs/abcpdr.csv -o $graphs
python $un/brunch/spacer/ScatterPlots-ae.py -f1 $graphs/kavy.csv -f2 $graphs/vanilla.csv -o $graphs

classes=('intel' '6s' 'nusmv' 'bob' 'pdt' 'oski' 'beem'  'oc8051' 'power' 'shift' 'necla' 'kenflash' 'bj' 'vis' 'prodcell' 'bc57')
c_text=""
for sol in "${solvers[@]}"
do
 out="$root"/out/hwmcc-exp/"$sol"
 for c in "${classes[@]}"
 do
  c_text="$c_text $c"
  class_out="$out"/"$c"
  mkdir -p "$class_out"
  for d in "$out"/1*/"$c"*.aig*
  do
    cp "$d" "$out"/"$c"/.
  done
  python "$run"/brunch/spacer/log_scrab.py -o "$graphs"/"$sol"-"$c".csv "$out"/"$c"
 done
done
python "$run"/brunch/spacer/createTable.py -f1 "$graphs"/kavy -f2 "$graphs"/avy -f3 "$graphs"/abcpdr -a $c_text
