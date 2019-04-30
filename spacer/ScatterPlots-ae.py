import pandas
import matplotlib
import matplotlib.pyplot
import sys
import os
import os.path
import numpy
# assumes that Result is the field that represents SAT/UNSAT
# assumes that execution_time is the field that corresponds to running time of the solver.
# usage
# python ScatterPlots.py -f1 file1.csv -f2 file2.csv -o dir
# will create 2 plots under the out directory. They will be named file1-file2-Depth/execution-time.png
# compares instances solved by atleast one of the solvers

def plotScatter(f1, f2, a, out):
		f1Name,ext=os.path.splitext(f1)
		f2Name,ext=os.path.splitext(f2)
		df1=pandas.read_csv(f1);
		df2=pandas.read_csv(f2);
		combinedDF=pandas.merge(df1,df2,how="left",on="index")
		combinedDF.loc[combinedDF["Result_x"]=="UNKNOWN",["execution_time_x"]]=combinedDF["execution_time_x"].max()
		combinedDF.loc[combinedDF["Result_y"]=="UNKNOWN",["execution_time_y"]]=combinedDF["execution_time_x"].max()
		mapping={'SAT': 1, 'UNSAT': 2, 'UNKNOWN': 4}
		color={-3:'orange', -2:'yellow',  -1: 'red', 0: 'blue', 1: 'red', 2: 'green', 3: 'violet'}
		combinedDF["color"]=(combinedDF["Result_x"].apply(lambda x:mapping[x]) -combinedDF["Result_y"].apply(lambda x:mapping[x])).apply(lambda x:color[x])
		assert ( not ( "red" in combinedDF["color"]) )
		matplotlib.pyplot.axis('auto')
		matplotlib.pyplot.scatter(x=combinedDF[a+"_x"],y=combinedDF[a+"_y"],c=combinedDF["color"])
		x_vals = numpy.array(matplotlib.pyplot.gca().get_xlim())
		matplotlib.pyplot.plot(x_vals, x_vals, '--',c='black')
		matplotlib.pyplot.ylabel(f2Name+" : "+a)
		matplotlib.pyplot.xlabel(f1Name+" : "+a)
		matplotlib.pyplot.title(f1Name+" and "+f2Name+" on "+a + " ALL instances")
		# matplotlib.pyplot.show()
		matplotlib.pyplot.savefig("plots/"+f1Name+f2Name+a+".png")
		matplotlib.pyplot.cla()
		matplotlib.pyplot.clf()

		#SOLVED instances
		matplotlib.pyplot.axis('auto')
		solvedInst=combinedDF[ ( combinedDF["Result_x"]=="SAT" ) | ( combinedDF["Result_y"]=="SAT" ) | ( combinedDF["Result_x"]=="UNSAT" ) | ( combinedDF["Result_y"]=="UNSAT" ) ]
		matplotlib.pyplot.scatter(x= solvedInst[a+"_x"],y=solvedInst[a+"_y"],c=solvedInst["color"])
		x_vals = numpy.array(matplotlib.pyplot.gca().get_xlim())
		matplotlib.pyplot.plot(x_vals, x_vals, '--',c='black')
		matplotlib.pyplot.ylabel(f2Name+" : "+a)
		matplotlib.pyplot.xlabel(f1Name+" : "+a)
		matplotlib.pyplot.title(f1Name+" and "+f2Name+" on "+a + " SOLVED instances")
		# matplotlib.pyplot.show()
		matplotlib.pyplot.savefig(out+"/"+f1Name+"-"+f2Name+"-"+a+".png")
		matplotlib.pyplot.cla()
		matplotlib.pyplot.clf()


def run (args=None):
    f1=args.f1[0]
    f2=args.f2[0]
    out=args.out[0]
    for a in ["execution_time, Depth"]:
		plotScatter(f1, f2, a, out)
    return 0
def main ():
		import argparse

		ap = argparse.ArgumentParser ()
		ap.add_argument ('-f1', dest='f1',metavar='FILE',
		                 help='one of the file for comparison', nargs=1)
		ap.add_argument ('-f2', dest='f2', metavar='FILE',
		                 help='one of the file for comparison', nargs=1)
        ap.add_argument ('-o', dest='out', metavar='DIR',
		                 help='destination dir of outputs', nargs=1)
        args = ap.parse_args (sys.argv[1:])
		return run (args)

if __name__ == '__main__':
    sys.exit (main ())
