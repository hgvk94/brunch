#!/bin/bash
root=$HOME/tool
bin=$root/bin
bench=$root/bench
run=$root/run
class=$1
dry_run=$2
if [ -z $class ]
then 
 echo "USAGE ./run-class.sh CLASS. CLASS is a prefix for the type of benchmark. e.g ./run-class intel"
 exit 1
fi

graphs=$root/graphs/$class
mkdir -p $graphs

time=3m
years=(14 15 17)
f=""

benchFile=$root/benchmarks-$class.txt
touch $benchFile
find $bench -name $class*.aig > $benchFile
if [ ! -s "$benchFile" ]
then
   echo "No benchmarks with this prefix"
   exit 1
fi
n=$(cat $benchFile | wc -l)
t=$(expr 120 \* $n)
echo "Will take atmost : $t minutes to run"
if [ ! -z $dry_run ] && [ $dry_run == "-n" ];
then 
   exit 0
fi
solvers=(kavy avy vanilla abcpdr)
for sol in "${solvers[@]}"
do
  f="$f $graphs/$sol-$class.csv"
  out=$root/out/$class/$sol
  mkdir -p $out 
  export bin out bench run time benchFile sol       
  $run/run-on-files.sh
  python $run/brunch/spacer/log_scrab.py -o $graphs/$sol-$class.csv $out
done

python $run/brunch/spacer/cactusCombine.py -f $f -o $graphs/$class.png
python $run/brunch/spacer/ScatterPlots-ae.py -f1 $graphs/kavy-$class.csv -f2 $graphs/avy-$class.csv -o $graphs
python $run/brunch/spacer/ScatterPlots-ae.py -f1 $graphs/kavy-$class.csv -f2 $graphs/abcpdr-$class.csv -o $graphs
python $run/brunch/spacer/ScatterPlots-ae.py -f1 $graphs/kavy-$class.csv -f2 $graphs/vanilla-$class.csv -o $graphs

python "$run"/brunch/spacer/createTable.py -f1 "$graphs"/kavy -f2 "$graphs"/avy -f3 "$graphs"/abcpdr -a $class
rm $benchFile
