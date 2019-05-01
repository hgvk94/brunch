#!/bin/bash
root="${root-$HOME/tool}"
bin="${bin-$root/bin}"
$bin/avy "$1" --verbose=3 --reset-cover=1 --opt-bmc --kstep=1 --shallow-push=1 --min-suffix=1 --glucose --glucose-inc-mode=1 --sat-simp=0 --glucose_itp=1
