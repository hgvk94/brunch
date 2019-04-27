import pandas
import matplotlib
import matplotlib.pyplot
import sys
import os
import os.path
import numpy
# assumes that Result is the field that represents SAT/UNSAT
# assumes that run_loop and execution_time are the fields that corresponds to running time of the solver. run_loop is what is returned by the solver and execution_time is returned by an external tool like time
# usage
# make a directory called plots and then run
# python ScatterPlots.py -f1 file1.csv -f2 file2.csv -a field1 field2 ...
# will create many plots under the plots directory. Each of them will be named file1file2-fieldx-[safe/unsafe/solved/solved-both/log].png

def plotRatioScatter(f1,f2,a,b):
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
		mapping={'SAT': 1, 'UNSAT': 2, 'UNKNOWN': 4}
		color={-3:'orange', -2:'yellow',  -1: 'red', 0: 'blue', 1: 'red', 2: 'green', 3: 'violet'}
		combinedDF["color"]=(combinedDF["Result_x"].apply(lambda x:mapping[x]) -combinedDF["Result_y"].apply(lambda x:mapping[x])).apply(lambda x:color[x])
		assert ( not ( "red" in combinedDF["color"]) )
		matplotlib.pyplot.axis('auto')
		combinedDF=combinedDF[ (combinedDF[b+"_x"]!=0) & (combinedDF[b+"_y"]!=0) & ( ( combinedDF["Result_x"]=="UNSAT") | ( combinedDF["Result_y"]=="UNSAT" ) )]
		assert(not ((combinedDF[b+"_x"]==0).any()))
		assert(not ((combinedDF[b+"_y"]==0).any()))
		matplotlib.pyplot.scatter(x=combinedDF[a+"_x"]/combinedDF[b+"_x"],y=combinedDF[a+"_y"]/combinedDF[b+"_y"],c=combinedDF["color"])
		x_vals = numpy.array(matplotlib.pyplot.gca().get_xlim())
		matplotlib.pyplot.plot(x_vals, x_vals, '--',c='black')
		matplotlib.pyplot.ylabel(f2Name+" : "+a+ " / " + b)
		matplotlib.pyplot.xlabel(f1Name+" : "+a+ " / " + b)
		matplotlib.pyplot.title(f1Name+" and "+f2Name+" on "+a+" / "+b + " SAFE instances")
		# matplotlib.pyplot.show()
		matplotlib.pyplot.savefig("plots/"+f1Name+f2Name+a+b+".png")
		matplotlib.pyplot.cla()
		matplotlib.pyplot.clf()
		print(combinedDF[combinedDF["Result_x"]!= combinedDF["Result_y"]][["index","Result_x","Result_y",a+"_x",a+"_y",b+"_x",b+"_y"]])


def plotScatter(f1,f2,a):
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

		#SAFE instances
		matplotlib.pyplot.axis('auto')
		safeInst=combinedDF[ ( combinedDF["Result_x"]=="UNSAT" ) | ( combinedDF["Result_y"]=="UNSAT" ) ]
		matplotlib.pyplot.scatter(x= safeInst[a+"_x"],y=safeInst[a+"_y"],c=safeInst["color"])
		x_vals = numpy.array(matplotlib.pyplot.gca().get_xlim())
		matplotlib.pyplot.plot(x_vals, x_vals, '--',c='black')
		matplotlib.pyplot.ylabel(f2Name+" : "+a)
		matplotlib.pyplot.xlabel(f1Name+" : "+a)
		matplotlib.pyplot.title(f1Name+" and "+f2Name+" on "+a + " SAFE instances")
		# matplotlib.pyplot.show()
		matplotlib.pyplot.savefig("plots/"+f1Name+f2Name+a+"-safe.png")
		matplotlib.pyplot.cla()
		matplotlib.pyplot.clf()

		#UNSAFE instances
		matplotlib.pyplot.axis('auto')
		unsafeInst=combinedDF[ ( combinedDF["Result_x"]=="SAT" ) | ( combinedDF["Result_y"]=="SAT" ) ]
		matplotlib.pyplot.scatter(x= unsafeInst[a+"_x"],y=unsafeInst[a+"_y"],c=unsafeInst["color"])
		x_vals = numpy.array(matplotlib.pyplot.gca().get_xlim())
		matplotlib.pyplot.plot(x_vals, x_vals, '--',c='black')
		matplotlib.pyplot.ylabel(f2Name+" : "+a)
		matplotlib.pyplot.xlabel(f1Name+" : "+a)
		matplotlib.pyplot.title(f1Name+" and "+f2Name+" on "+a + " UNSAFE instances")
		# matplotlib.pyplot.show()
		matplotlib.pyplot.savefig("plots/"+f1Name+f2Name+a+"-unsafe.png")
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
		matplotlib.pyplot.savefig("plots/"+f1Name+f2Name+a+"-solved.png")
		matplotlib.pyplot.cla()
		matplotlib.pyplot.clf()

		#SOLVED by both
		matplotlib.pyplot.axis('auto')
		solvedInst=combinedDF[ ( ( combinedDF["Result_x"]=="SAT" ) & ( combinedDF["Result_y"]=="SAT" ) ) | ( ( combinedDF["Result_x"]=="UNSAT" ) & ( combinedDF["Result_y"]=="UNSAT" ) ) ]
		matplotlib.pyplot.scatter(x= solvedInst[a+"_x"],y=solvedInst[a+"_y"],c=solvedInst["color"])
		x_vals = numpy.array(matplotlib.pyplot.gca().get_xlim())
		matplotlib.pyplot.plot(x_vals, x_vals, '--',c='black')
		matplotlib.pyplot.ylabel(f2Name+" : "+a)
		matplotlib.pyplot.xlabel(f1Name+" : "+a)
		matplotlib.pyplot.title(f1Name+" and "+f2Name+" on "+a + " instances SOLVED by BOTH")
		# matplotlib.pyplot.show()
		matplotlib.pyplot.savefig("plots/"+f1Name+f2Name+a+"-solved-both.png")
		matplotlib.pyplot.cla()
		matplotlib.pyplot.clf()

		#loglog plot
		matplotlib.pyplot.xscale('log')
		matplotlib.pyplot.yscale('log')
		solvedInst=combinedDF[ ( combinedDF["Result_x"]=="SAT" ) | ( combinedDF["Result_y"]=="SAT" ) | ( combinedDF["Result_x"]=="UNSAT" ) | ( combinedDF["Result_y"]=="UNSAT" ) ]
		matplotlib.pyplot.scatter(x= solvedInst[a+"_x"],y=solvedInst[a+"_y"],c=solvedInst["color"])
		x_vals = numpy.array(matplotlib.pyplot.gca().get_xlim())
		matplotlib.pyplot.loglog(x_vals, x_vals, '--',c='black')
		matplotlib.pyplot.ylabel(f2Name+" : "+a)
		matplotlib.pyplot.xlabel(f1Name+" : "+a)
		matplotlib.pyplot.title(f1Name+" and "+f2Name+" on "+a + " log plot")
		# matplotlib.pyplot.show()
		matplotlib.pyplot.savefig("plots/"+f1Name+f2Name+a+"-log.png")
		matplotlib.pyplot.cla()
		matplotlib.pyplot.clf()

		print(combinedDF[combinedDF["Result_x"]!= combinedDF["Result_y"]][["index","run_loop_x","run_loop_y","Result_x","Result_y","Depth_x","Depth_y",a+"_x",a+"_y"]])
		print("SAFE")
		print(f1+" : "+str(len(combinedDF[combinedDF["Result_x"]=="UNSAT"])))
		print(f2+" : "+str(len(combinedDF[combinedDF["Result_y"]=="UNSAT"])))
		print("virtual best : "+str(len(combinedDF[(combinedDF["Result_y"]=="UNSAT")|(combinedDF["Result_x"]=="UNSAT")])))
		print("\n\nUNSAFE")
		print(f1+" : "+str(len(combinedDF[combinedDF["Result_x"]=="SAT"])))
		print(f2+" : "+str(len(combinedDF[combinedDF["Result_y"]=="SAT"])))
		print("virtual best : "+str(len(combinedDF[(combinedDF["Result_y"]=="SAT")|(combinedDF["Result_x"]=="SAT")])))

def run (args=None):
		f1=args.f1[0]
		f2=args.f2[0]
		print(f1)
		print(f2)
		print(args.fields)
		if args.fields is not None:
			for a in args.fields:
				print(a)
				plotScatter(f1,f2,a)
		if args.ratio is not None:
			i=iter(args.ratio)
			ratioMap = dict(zip(i,i))
			print(ratioMap)
			for k,v in ratioMap.items():
				plotRatioScatter(f1,f2,k,v)
		return 0
def main ():
		import argparse

		ap = argparse.ArgumentParser ()
		ap.add_argument ('-f1', dest='f1',metavar='FILE',
		                 help='one of the file for comparison', nargs=1)
		ap.add_argument ('-f2', dest='f2', metavar='FILE',
		                 help='one of the file for comparison', nargs=1)
		ap.add_argument ('-a',dest='fields', metavar='STRING',
		                 help='the fields to be compared', nargs='+')
		ap.add_argument ('-r',dest='ratio', metavar='STRING',
		                 help='list fields compared together as a ratio', nargs='+')    
		args = ap.parse_args (sys.argv[1:])
		return run (args)

if __name__ == '__main__':
    sys.exit (main ())
