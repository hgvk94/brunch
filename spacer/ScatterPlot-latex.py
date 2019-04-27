import pandas
import pylab as plt
import sys
import os
import os.path
import numpy
def plotScatter(f1,f2,a,log):
		f1Name,ext=os.path.splitext(f1)
		f2Name,ext=os.path.splitext(f2)
		df1=pandas.read_csv(f1);
		df2=pandas.read_csv(f2);
		combinedDF=pandas.merge(df1,df2,how="left",on="index")
		combinedDF.loc[combinedDF["Result_x"]=="UNKNOWN",["run_loop_x"]]=combinedDF["run_loop_x"].max()
		combinedDF.loc[combinedDF["Result_y"]=="UNKNOWN",["run_loop_y"]]=combinedDF["run_loop_x"].max()
		if "execution_time_x" in combinedDF.columns and "execution_time_y" in combinedDF.columns:
			combinedDF.loc[combinedDF["Result_x"]=="UNKNOWN",["execution_time_x"]]=combinedDF["execution_time_x"].max()
			combinedDF.loc[combinedDF["Result_y"]=="UNKNOWN",["execution_time_y"]]=combinedDF["execution_time_x"].max()
		fig = plt.figure ()
		plt.rc('axes', labelsize=20)
		ax = fig.add_subplot (111)
		if log:
			ax.set_xscale('log')
			ax.set_yscale('log')
		solvedInst=combinedDF[ ( ( combinedDF["Result_x"]=="SAT" ) & ( combinedDF["Result_y"]=="SAT" ) ) | ( ( combinedDF["Result_x"]=="UNSAT" ) & ( combinedDF["Result_y"]=="UNSAT" ) ) ]
		ax.scatter (solvedInst[a+"_x"], solvedInst[a+"_y"],c='black')
		x_vals = numpy.array(plt.gca().get_xlim())
		if log:
			pass
			ax.loglog(x_vals, x_vals, '--',c='black')
		else:
			ax.plot(x_vals, x_vals, '--',c='black')
		ax.set_ylabel(f2Name)
		ax.set_xlabel(f1Name)
		# plt.show ()
		plt.savefig("plots/"+f1Name+f2Name+a+".png")

def run (args=None):
        f1=args.f1[0]
        f2=args.f2[0]
        log=args.log
        print(f1)
        print(f2)
        print(args.fields)
        for a in args.fields:
        	print(a)
        	plotScatter(f1,f2,a,log)
        return 0
def main ():
        import argparse

        ap = argparse.ArgumentParser ()
        ap.add_argument ('-f1', dest='f1',metavar='FILE',
                         help='one of the file for comparison', nargs=1)
        ap.add_argument ('-f2', dest='f2', metavar='FILE',
                         help='one of the file for comparison', nargs=1)
        ap.add_argument ('-log', dest='log',
                         help='plot in log scale',action='store_true')
        ap.add_argument ('-a',dest='fields', metavar='STRING',
                         help='the fields to be compared', nargs='+')    
        args = ap.parse_args (sys.argv[1:])
        return run (args)

if __name__ == '__main__':
    sys.exit (main ())
