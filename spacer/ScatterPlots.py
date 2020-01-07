import pandas
import matplotlib
import matplotlib.pyplot as plt
import sys
import os
import os.path
import numpy
import seaborn as sns

# python ScatterPlots.py -f1 file1.csv -f2 file2.csv -a field1 field2 ...

def flt_index(df, s):
    return df[df['index'].str.startswith(s)].copy()

def preprocess(df, a):
        if(a == "time"):
                d = df[["index","result", "time"]].copy()
        else:
                d = df[["index", "result", "time", a]].copy()
        d.loc[d['result'].isna(), ['result']] = "timeout"
        d.loc[d['result'] == "error", ['result']] = "timeout"
        d.loc[d['result'] == "unknown", ['result']] = "timeout"
        d.loc[d['time'].isna(), ['time']] = 900;
        assert(len(d[~d['result'].isin(["sat", "unsat", "timeout"])]) == 0)
        d.loc[d["result"] == "timeout", ["time"]] = 900;
        return d;


def plotScatter(f1, f2, a, bench):
        f1Name, _ = os.path.splitext(f1);
        f2Name, _ = os.path.splitext(f2);
        df1 = pandas.read_csv(f1);
        df1 = flt_index(df1, bench);
        df1 = preprocess(df1, a);
        df2 = pandas.read_csv(f2);
        df2 = flt_index(df2, bench);
        df2 = preprocess(df2, a);
        combinedDF = pandas.merge(df1, df2, how = "inner", on = "index");
        assert(len(combinedDF.query('( (result_x == "sat") & (result_y == "unsat") ) | ((result_x == "unsat") & (result_y == "sat"))')) == 0);
        phi = combinedDF[combinedDF['result_x'].isin(["sat", "unsat"]) | combinedDF['result_y'].isin(["sat", "unsat"])].copy();
        gt=[]
        st=[]
        for n, r in phi.iterrows():
                if(r['result_x'] == "sat" or r['result_y'] == "sat"):
                        gt.append("sat")
                else:
                        gt.append("unsat")
                if(r['result_x'] != "timeout" and r['result_y'] != "timeout"):
                        st.append("both")
                elif(r['result_x'] == "timeout"):
                        st.append("only by " + f2Name)
                else:
                        st.append("only by " + f1Name)
        phi.loc[:, "grnd_trth"] = gt;
        phi.loc[:, "solved_by"] = st;
        fig = plt.figure(figsize=(10,10));
        plt.axis('auto')
        sns.set(style = 'ticks', palette = 'Set2')
        g = sns.scatterplot(x= a + "_x", y= a + "_y", style = "grnd_trth", hue = "solved_by", data = phi);
        sns.despine()
        x = numpy.linspace(0, max(phi[a+"_x"]), 2)
        g.plot(x, x)
        # plt.show()
        plt.xlabel(f1Name + " " + a)
        plt.ylabel(f2Name + " " + a)
        plt.savefig("plots/" + f1Name + f2Name + a + ".svg")
def run (args=None):
        f1 = args.f1[0]
        f2 = args.f2[0]
        bench = args.bench[0]
        print(f1)
        print(f2)
        print(args.fields)
        for a in args.fields:
        	print(a)
        	plotScatter(f1,f2,a, bench)
        return 0

def main ():
        import argparse

        ap = argparse.ArgumentParser ()
        ap.add_argument ('-b', dest='bench',metavar='STRING',
                         help='the list of benchmark families', nargs=1)
        ap.add_argument ('-f1', dest='f1',metavar='FILE',
                         help='one of the file for comparison', nargs=1)
        ap.add_argument ('-f2', dest='f2', metavar='FILE',
                         help='one of the file for comparison', nargs=1)
        ap.add_argument ('-a',dest='fields', metavar='STRING',
                         help='the fields to be compared', nargs='+')
        args = ap.parse_args (sys.argv[1:])
        return run (args)

if __name__ == '__main__':
    sys.exit (main ())
