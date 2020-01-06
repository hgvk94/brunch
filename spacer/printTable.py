import sys
import os
import pandas
import pytabular as pytab
#input a list of solvers to compare
#input benchmark string
#output latex table containing the performance of the solvers on the benchmarks
def flt_index(df, s):
    return df[df['index'].str.startswith(s)]

def preprocess(df):
        d = df[["index","result"]]
        d['result'].fillna(value="timeout", inplace=True)
        d.replace(["unknown, error"], "timeout", inplace = True)
        return d;

def run (args=None):
    print("Comparing ");
    dfs=[];
    hdr_s=[""];
    hdr_f=["class"];
    for a in args.files:
        print(a + ", ");
        df = pandas.read_csv(a);
        df = preprocess(df);
        dfs.append(df)
        hdr_f.append(os.path.splitext(a)[0])
        hdr_f.append("")
        hdr_s.append("sat")
        hdr_s.append("unsat")
    hdr = [hdr_f, hdr_s]
    bold = [];
    tabular = pytab.Tabular(hdr)
    print("on benchmarks ")
    for a in args.bench:
        row = []
        b_row = []
        row.append(a)
        df_flts = []
        print(a + ", ")
        sats = [];
        unsats = [];
        for df in dfs:
            df_flt = flt_index(df, a)
            df_flts.append(df_flt)
            sat = len(df_flt.query('result == "sat"'))
            unsat = len(df_flt.query('result == "unsat"'))
            sats.append(sat)
            unsats.append(unsat)
            row.append(str(sat))
            row.append(str(unsat))
        max_sat = max(sats);
        max_unsat = max(unsats);
        t_row = pytab.Tabular(row);
        for i in range(0, len(sats)):
            if sats[i] == max_sat:
                b_row.append(2*i + 1);
        for i in range(0, len(unsats)):
            if unsats[i] == max_unsat:
                b_row.append(2*i + 2);
        bold.append(b_row)
        print(b_row)
        tabular = pytab.vstack(tabular, t_row)
    #set bold
    for r in range(len(bold)):
        for j in bold[r]:
            print(j)
            tabular[r + len(hdr), j].set_bold();
    print("\n\n")
    tabular[0].set_lines(1)
    tabular[-1].set_lines(1)
    for i in range(1 , len(hdr_f), 2):
        tabular[0, i:i+2].merge(force = True);
    print(tabular)

def main ():
        import argparse

        ap = argparse.ArgumentParser ()
        ap.add_argument ('-b', dest='bench',metavar='STRING',
                         help='the list of benchmark families', nargs='+')
        ap.add_argument ('-f',dest='files', metavar='STRING',
                         help='the solvers to be compared', nargs='+')
        args = ap.parse_args (sys.argv[1:])
        return run (args)

if __name__ == '__main__':
    sys.exit (main ())
