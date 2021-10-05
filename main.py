import csv
import re
import argparse


def main(in_file,out_file):
    print("starting parsing")
    f = open(in_file)
    out_csv = open(out_file,'w')
    headers = ['time','application','query','query_time','lock_time','rows_sent','rows_examined']
    csv_writer = csv.DictWriter(out_csv,fieldnames=headers)
    csv_writer.writeheader()
    started = False
    query = ""
    for l in f.readlines():
        l = l.strip()
        if l.startswith("# Time:"):
            if started:
                row['query'] = query
                csv_writer.writerow(row)
            started = True
            row = {}
            row['time'] = l.split(" ")[2] 
            query = ""
        else:
            if l.startswith('# User@Host:'):
                row['application'] = l.split(" ")[2]
            elif l.startswith("# Query_time:"):
                params = re.findall(r"[-+]?\d*\.\d+|\d+",l)
                row['query_time'] = params[0]
                row['lock_time'] = params[1]
                row['rows_sent'] = params[2]
                row['rows_examined'] = params[3]
            else:
                if started:
                    if l.startswith("SET"):
                        pass
                    elif l.startswith("use"):
                        pass
                    else:
                        query = query+" "+l.strip()
    out_csv.close()
    print("output csv generated")

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sqllogs', help='path to sql logs',required=True)
    parser.add_argument('--out_csv',help="path to the outputfile",required=True)
    args = parser.parse_args()
    main(args.sqllogs,args.out_csv)