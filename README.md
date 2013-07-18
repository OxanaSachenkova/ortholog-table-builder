# Ortholog Generator

This will generate a CSV file that can be used to generate an orthologs table in a database. It gets all of its data from the InParanoid database.

## Using the scripts

### Prerequisites

For each species that you intend to create orthologs for you must create a tab separated file based around the following format:

| Ensembl Protein ID | EntrezGene ID | Associated Gene Name |
|--------------------|---------------|----------------------|
| ENSPTRP00000052888 | 465864        | PARK7                |

These need to be named with the scientific name of the species and the extension `.txt` e.g. `musculus.txt`. They also need to be stored in a directory named `annotations` in the same location as the script files.

### download_and_annotate.py

This script will take a list of species, download the necessary files from InParanoid and annotate them with the necessary Entrez Gene ID's. It should not be hard to adapt this to suit another identifier if required.

This script only needs to be run once, or when new species are added.

#### Running

You may need to edit the file to add or remove species you do not require. All the species are stored in a list called `species`.

Simply run with `python download_and_annotate.py`

### build_ortholog_table.py

This script will either limit the orthologs to the given species or create a list containing all species. This can then be imported straight into a database using the CSV option possessed by most databases.

#### Arguments

- **output:** A file to output the orthologs to
- **annotations:** A directory containing annotated ortholog txt files (usually called ortholog_annot)
- **--idlist:** A file containing a list of entrez ids to use
- **-s:** Species to use e.g. M.musculus. You can use more than one species e.g. `-s M.musculus H.sapiens D.melangastor`. Either this or `-a` is required.
- **-a:** Ignore idlist and simply produce a massive table of orthologs. Note: CANNOT be used with the `-s` option.

## File structure

| ID | Group    | File from    | Entrez Gene ID | Gene Symbol | Species                | Unique grouping ID   | Score | Identifier | Percentage |
|----|----------|--------------|----------------|-------------|------------------------|------------------------|-------|------------|------------|
| 1  | 5082     | C.elegans.fa | 172041         | dhc-1       | Caenorhabditis elegans | 1-elegans:melanogaster | 1.000 | CE23997    | 100%       |

## Table Structure

NOTE: This is for MySQL but can easily be adapted to any other database engine.

```
CREATE TABLE `orthologs` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `species` varchar(25) DEFAULT NULL,
  `group` int(11) DEFAULT NULL,
  `identifier` varchar(50) DEFAULT NULL,
  `symbol` varchar(10) DEFAULT NULL,
  `entrez_id` int(11) DEFAULT NULL,
  `percentage` varchar(4) DEFAULT NULL,
  `score` float DEFAULT NULL,
  `unique_grouping` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrez_id` (`entrez_id`),
  KEY `unique_grouping` (`unique_grouping`),
  KEY `species` (`species`),
  KEY `symbol` (`symbol`),
  KEY `unique_grouping_2` (`unique_grouping`,`species`)
) DEFAULT CHARSET=utf8;
```
