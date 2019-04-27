import math
import sys
import os
import os.path
import re

def processFile (fname):
    '''process a single file'''
    base_name = os.path.basename (fname)
    name, _ext = os.path.splitext (base_name)

    state=0
    k_value=-1
    i_value=-1
    total=0
    maximums=0
    ones=0
    arr=[]
    sum_k_values=0
    sum_i_values=0
    second_print=False
    if base_name.endswith('.aig'):
        with open (fname) as input:
            for line in input:
                l=line.strip ()
                if(l.startswith ('BRUNCH_STAT')):
                    fields = l.split()
                    if( fields[1] == "kInductiveDepth"):
                        #deducing the values from averages
                        #cannot compensate for rounding errors
                        k_value = int(float(fields[2])*total-sum_k_values)
                        state=state+1
                    elif ( fields[1] == "kInductiveSuffix"):
                        state=state+1
                        i_value=math.floor(float(fields[6][:-1]))
                    else:
                        pass
                if(state == 4):
                    state = 0
                    assert(k_value!=-1)
                    assert(i_value!=-1)
                    # print(str(i_value) + " " + str(k_value))
                    assert(k_value<=i_value+1)
                #    if second_print:
                    sum_k_values=sum_k_values+k_value
                    sum_i_values=sum_i_values+i_value
                    #second_print= not second_print
                    if k_value ==1 :
                        ones=ones+1
                    if k_value == i_value+1:
                        maximums=maximums+1
                    if(len(arr)<=k_value):
                        arr.extend([0]*(k_value+1-len(arr)))
                    arr[k_value]=arr[k_value]+1
                    total=total+1
                    k_value=-1
                    i_value=-1
        assert(len(arr)<=1 or arr[1]==ones)
    return maximums, arr, total

def processDir (root):
    print("name,#max,#ones,#two")
    '''Recursively process all files in the root directory'''
    for root, dirs, files in os.walk(root):
        for name in files:
            m,arr,total = processFile (os.path.join(root, name))
            if(total!=0):
                if(len(arr)<=2):
                    arr.extend([0]*(3-len(arr)))
                print(name + ',' + str(m/total) + ',' + str(arr[1]/total)+ ',' + str(arr[2]/total))

def process (name):
    if os.path.isfile (name):
        processFile (name)
    elif os.path.isdir (name):
        processDir (name)
    else:
        assert False


def run(args):
    for f in args.in_files:
       process(f)
def main ():
    import argparse
    ap = argparse.ArgumentParser(sys.argv[1:])
    ap.add_argument ('-o', dest='out_file',
                        metavar='FILE', help='Output file name',
                         default='out.csv')
    ap.add_argument ('in_files',  metavar='FILE',
                         help='Input file', nargs='+')

    args = ap.parse_args(sys.argv[1:])
    return run(args)
if __name__ == '__main__':
    sys.exit(main())
