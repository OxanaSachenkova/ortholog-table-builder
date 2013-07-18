import csv
import urllib2

species = ['Homo sapiens', 'Caenorhabditis elegans', 'Drosophila melanogaster', 'Mus musculus', 'Saccharomyces cerevisiae', 'Rattus norvegicus', 'Danio rerio', 'Canis lupus familiaris', 'Bos taurus', 'Pan troglodytes', 'Gallus gallus']
species.sort()

def annotate_files(f, file_name, s1, s2):
    "Take a file and annotate using species 1 (s1) and species 2 (s2) files"
    annot = {}
    s1_annot_file = csv.DictReader(open('annotations/'+s1+'.txt'), delimiter="\t")
    annot[s1] = {}
    for l in s1_annot_file:
        annot[s1][l['Ensembl Protein ID']] = [l['EntrezGene ID'], l['Associated Gene Name']]
    s2_annot_file = csv.DictReader(open('annotations/'+s2+'.txt'), delimiter="\t")
    annot[s2] = {}
    for l in s2_annot_file:
        annot[s2][l['Ensembl Protein ID']] = [l['EntrezGene ID'], l['Associated Gene Name']]

    orthologs_out = []
    orthologs = csv.reader(f, delimiter="\t")
    for line in orthologs:
        new_group_id = "{0}-{1}:{2}".format(line[0],s1,s2)
        sspecies = line[2].split('.')
        fsn = [s for s in species if s.endswith(sspecies[1])]
        fsn.extend([new_group_id])
        if line[4] in annot[sspecies[-2]]:
            annot[sspecies[-2]][line[4]].extend(fsn)
            line[3:3] = annot[sspecies[-2]][line[4]]
        else:
            line[3:3] = ['','','']
        orthologs_out.append(line)

    with open('ortholog_annot/'+file_name, 'w') as orthout:
        writer = csv.writer(orthout, delimiter="\t")
        writer.writerows(orthologs_out)

for s in species:
    for ss in species:
        if s != ss:
            if species.index(s) < species.index(ss):
                s_split = s.split()
                ss_split = ss.split()
                file_name = 'sqltable.{0}.{1}.fa-{2}.{3}.fa'.format(s_split[0][0], s_split[1], ss_split[0][0], ss_split[1])
                try:
                    with open('ortholog_files/'+file_name) as f:
                        print 'A file named {0} already exists locally, using this'.format(file_name)
                        annotate_files(f, file_name, s_split[1], ss_split[1])
                except IOError as e:
                    url = 'http://inparanoid.sbc.su.se/download/current/sqltables/'
                    try:
                        print 'Attempting to download {0} from {1}'.format(file_name, url)
                        f = urllib2.urlopen(url+file_name)
                        with open('ortholog_files/'+file_name, 'w') as out:
                            out.write(f.read())
                        annotate_files(f, file_name, s_split[1], ss_split[1])
                    except urllib2.URLError as e:
                        print e
