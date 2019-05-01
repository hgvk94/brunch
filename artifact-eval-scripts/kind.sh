#!/bin/bash
root="${root-$HOME/tool}"
bin="${bin-$root/bin}"
#compute the depth of induction based on file name
h=${1%.*}
t=${h#*.}
z="$((t + 2))"
$bin/abc -c "read "$1"; bmc3 -F "$z" -v; ind -F "$z" -u -v; "
