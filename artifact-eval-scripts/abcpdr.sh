#!/bin/bash
root="${root-$HOME/tool}"
bin="${bin-$root/bin}"

$bin/abcpdr "$1" --verbose=3 
