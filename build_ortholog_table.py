import csv
import os
import re
import argparse

def makeorth():

    parser = argparse.ArgumentParser(description='Take a list of IDs and generate a CSV of orthologs for use in a database')
    parser.add_argument('output', help="A file to output the orthologs to") 
    parser.add_argument('annotations', help="A directory containing annotated ortholog CSV files") 
    parser.add_argument('--idlist', help="A file containing a list of entrez ids to use") 
    parser.add_argument('-s', metavar='SPECIES', nargs="*", help="Species to use e.g. M.musculus") 
    parser.add_argument('-a', action='store_true', default=False, help="Ignore idlist and simply produce a massive table of orthologs")
    args = parser.parse_args()

    if not args.a:
        ids = []
        with open(args.idlist) as f:
            for line in f.readlines():
                if line != '"NULL"' or line != '':
                    if line.strip() not in ids:
                        ids.append(line.strip())
    orths = []
    for file in os.listdir(args.annotations):
        sf = re.findall(r'sqltable.(.*).fa-(.*).fa', file)
        if sf[0][0] in args.s and sf[0][1] in args.s:
            print file
            orth = csv.reader(open(args.annotations+'/'+file), delimiter="\t")
            cur_orths = []
            entrez_orths = []
            for line in orth:
                cur_orths.append(line)
                entrez_orths.append(line[3])
            if args.a:
                orths.extend(cur_orths) 
            else:
                for i in ids:
                    try:
                        pos = entrez_orths.index(i)
                        group = cur_orths[pos][0]
                        grouped = [x for x in cur_orths if x[0] == group and x[3] != '']
                        orths.extend(grouped)
                    except ValueError:
                        pass

    writer = csv.writer(open(args.output, 'w'), delimiter="\t")
    writer.writerows(orths)

if __name__ == '__main__':
    makeorth()
