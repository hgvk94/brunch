import pandas
import matplotlib.pyplot
import numpy as np
import sys
import os
import os.path
def plotCactus(files):
	matplotlib.pyplot.axis('auto')
	matplotlib.pyplot.xlabel("Instances")
	matplotlib.pyplot.ylabel("Time taken (s)")
	markers=['p','s','o','*','v']
	for i,f in enumerate(files):
		df=pandas.read_csv(f);
		fName,ext=os.path.splitext(f)
		col=df[df["Result"]=="UNSAT"]["execution_time"]
		matplotlib.pyplot.plot(np.array(sorted(col)),label=fName,marker=markers[i%len(markers)])

	matplotlib.pyplot.legend()
	matplotlib.pyplot.savefig("cactus.png")

def run (args=None):
        plotCactus(args.files)
        return 0
def main ():
        import argparse

        ap = argparse.ArgumentParser ()
        ap.add_argument ('-f',dest='files', metavar='FILE',
                         help='the files to be compared', nargs='+')
        args = ap.parse_args (sys.argv[1:])
        return run (args)

if __name__ == '__main__':
    sys.exit (main ())