from functools import reduce
import pandas
import sys
import os
import os.path

#prints number of solved instances and number of instances that are uniquely solved for f1
def printSATColumn(f1,f2,f3,a):
	cdf=pandas.DataFrame()
	cdf=reduce(lambda first,second: pandas.merge(first,second,how="left",on="index"),[pandas.read_csv(f+'-'+a+'.csv') for f in [f1,f2,f3]])
	unsat=len(cdf[cdf["Result_x"]=="UNSAT"])
	sat=len(cdf[cdf["Result_x"]=="SAT"])
	unsatUnique=len(cdf[(cdf["Result_x"]=="UNSAT") & (cdf["Result_y"]=="UNKNOWN") & (cdf["Result"]=="UNKNOWN")])
	satUnique=len(cdf[(cdf["Result_x"]=="SAT") & (cdf["Result_y"]=="UNKNOWN") & (cdf["Result"]=="UNKNOWN")])
	print("&${:s}$".format(str(unsat)),end="")
	if unsatUnique>0:
		print("~(${:s}$)".format(str(unsatUnique)),end="")
	print("&${:s}$".format(str(sat)),end="")
	if satUnique >0:
		print("~(${:s}$)".format(str(satUnique)),end="")
	print(" ",end="")

def printRunningTime(f,a):
	df=pandas.read_csv(f+'-'+a+'.csv')
	ctime=df[(df["Result"]=="UNSAT") | (df["Result"]=="SAT")]["execution_time"].sum()/60
	if ctime<1 and ctime > 0:
		print("& $1$",end=" ")
	else :	
		print("&${:d}$".format(int(round(ctime))),end=" ")

def printRow(f1,f2,f3,a):
		files = [f1,f2,f3];
		print("%s"%(a),end =" ");
		# for f in files:
		# 	df=pandas.read_csv(f+'-'+a+'.csv');
		# 	print("&{:s}&{:s}".format(str(len(df[df["Result"]=="UNSAT"])),str(len(df[df["Result"]=="SAT"]))),end =" ")
			# print("&{:.2f}/{:.2f}".format(((df[ (df["Result"]=="UNSAT")]["execution_time"].sum())),((df[df["Result"]=="SAT"]["execution_time"].sum()))),end =" ")
		printSATColumn(f1,f2,f3,a)
		printRunningTime(f1,a)
		printSATColumn(f2,f3,f1,a)
		printRunningTime(f2,a)
		printSATColumn(f3,f1,f2,a)
		printRunningTime(f3,a)
		cdf=pandas.DataFrame()
		cdf=reduce(lambda first,second: pandas.merge(first,second,how="left",on="index"),[pandas.read_csv(f+'-'+a+'.csv') for f in [f1,f2,f3]])
		vbsSafe=cdf[ (cdf["Result"]=="UNSAT") | (cdf["Result_y"]=="UNSAT") | (cdf["Result_x"]=="UNSAT") ]
		vbsUnSafe=cdf[(cdf["Result"]=="SAT") | (cdf["Result_y"]=="SAT") | (cdf["Result_x"]=="SAT") ]
		vbsSafeSolved=str(len(vbsSafe))
		vbsUnSafeSolved=str(len(vbsUnSafe))
		# rt=0
		# for i,f in vbsSafe.iterrows():
		# 	rt=rt+min(f["execution_time_x"],f["execution_time_y"],f["execution_time"])
		# for i,f in vbsUnSafe.iterrows():
		# 	rt=rt+min(f["execution_time_x"],f["execution_time_y"],f["execution_time"])
		# rt=rt/60
		# print("&${:s}$&${:s}$&${:d}$\\\\".format(vbsSafeSolved,vbsUnSafeSolved,int(round(rt))))
		print("&${:s}$&${:s}$\\\\".format(vbsSafeSolved,vbsUnSafeSolved))

def run (args=None):
        f1=args.f1[0]
        f2=args.f2[0]
        f3=args.f3[0]
        for a in args.classes:
        	print("\\hline")
        	printRow(f1,f2,f3,a)
        print("\\hline")
        return 0
def main ():
        import argparse

        ap = argparse.ArgumentParser ()
        ap.add_argument ('-f1', dest='f1',metavar='FILE',
                         help='one of the file for comparison', nargs=1)
        ap.add_argument ('-f2', dest='f2', metavar='FILE',
                         help='one of the file for comparison', nargs=1)
        ap.add_argument ('-f3', dest='f3', metavar='FILE',
                         help='one of the file for comparison', nargs=1)
        ap.add_argument ('-a',dest='classes', metavar='STRING',
                         help='the classes to be compared', nargs='+')    
        args = ap.parse_args (sys.argv[1:])
        return run (args)

if __name__ == '__main__':
    sys.exit (main ())
