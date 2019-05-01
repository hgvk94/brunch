#!/bin/bash
root=$HOME/tool
bin=$root/bin
bench=$root/bench
run=$root/run

graphs=$root/graphs/shift-exp
mkdir -p $graphs

time=300s
loc="shift"
benchFile=$bench/$loc/benchmarks.txt

f=""
solvers=(kavy avy abcpdr kind)

for sol in "${solvers[@]}"
do
  out=$root/out/shift-exp/$sol
  mkdir -p $out 

  f="$f $graphs/$sol.csv"
  export root bin out bench run time benchFile sol
  $run/run-on-files.sh 
  python $run/brunch/spacer/log_scrab.py -o $graphs/$sol.csv $out

done 
python $run/brunch/spacer/cactusCombine.py -f $f -o $graphs/shift-cactus.png 
