#!/bin/bash
root="${root-$HOME/tool}"
bin="${bin-$root/bin}"
sol="${sol-kavy}"
out="${out-$root/out/$sol}"
benchFile="${benchFile-$root/bench/sample.txt}"
run="${run-$root/run}"

time="${time-30m}"

echo "Running $sol"
while IFS='' read -r f || [[ -n "$f" ]]; do
	fileName=$(basename -- $f)
	echo "processing file "$fileName
	{ time timeout  $time $run/$sol.sh "$f" > $out/$fileName; } 2>$out/$fileName.err
done < $benchFile
