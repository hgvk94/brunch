#!/bin/bash
root="${root-$HOME/tool}"
bin="${bin-$root/bin}"

$bin/kavy "$1" --verbose=3 --lemma-abs=1 --kind-pol=3 --min-suffix=1 --abstraction=0 --coi=1 --incr=1 --sat-simp=1 --itp-simp=0 --shallow-push=1 --reset-cover=1 --glucose --glucose_itp --opt-bmc=0 --quip=0
