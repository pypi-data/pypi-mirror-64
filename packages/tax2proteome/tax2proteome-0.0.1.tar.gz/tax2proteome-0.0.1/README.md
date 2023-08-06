# tax2proteome

tax2proteome creates based on given taxon IDs and a reference database a taxon specific database in fasta format. This taxon specific database contains according to the selected options all fasta entries of:
* given taxon IDs and their descendant taxon IDs in the phylogenetic tree
* given taxon IDs (option --no_descendants)
* given taxon IDs adapted to specified level up in the phylogenetic tree and their descendant taxon IDs (option --level)
* given taxon IDs and their descendant taxon IDs in the phylogenetic tree until level species, taxonIDs with lower level are not included (option --species)

Databases from which the matching entries are read out are: the NCBI non-redundant peptide database, swissprot, uniprot or trembl database. Also user-defined databases are possible as long as the header of the database contains taxonIDs in form of "OX=NUMBER" or contains NCBI/uniprot accession numbers.
Using uncompressed databases speed up the program considerably.

## Getting Started

tax2proteome is a python3 command line tool. It can be installed as pypi-package or as conda-package (https.anaconda.org/jschmacht/tax2proteome).

### Prerequisites

Python3


### Installing
```
pip install tax2proteome
```
or
```
pip install -i https://pypi.org/simple/tax2proteome-jschmacht 
```

## Deployment

tax2proteome is a command line tool and starts with: 
```
python -m tax2proteome [options]
```

### Options:
|   | option         | description
|---|----------------|---------------------------------------------------------------------------------------------------------------------------|
|-i |--input         | TaxID input file: tabular file containing a column of NCBI taxon IDs. Columns tab separated.
|-c |--column        | The column (zero-based) in the tabular file that contains Taxon IDs. Default = 0.
|-t |--taxon         | NCBI taxon ID/s for database extraction. Multiple taxonIDs seperated by space.
|-d |--database      | Database choice for analysis or for download. Choices: ncbi, uniprot, tremble, swissprot.
|-p |--path          | Path to folder with all required databases: taxdump.tar.gz (for all databases), prot.accession2taxid or prot.accession2taxid.gz and pdb.accession2taxid.gz (for ncbi databases). Optional: peptide_database named: nr/nr.gz or uniprot_trembl.fasta/uniprot_trembl.fasta.gz or uniprot_sprot.fasta/uniprot_sprot.fasta.gz or uniprot.fasta./uniprot.fasta.gz
|-o |--out           | File name and direction of the result taxon specified peptide database. Default = /taxon_specified_db_DATE/taxon_database.fasta
|-n |--dbname        | Database name and direction. If database is in other folder than --path or name deviates from standard names
|-l |--level         | Hierarchy level up in anchestral tree. Choices: species, section, genus, tribe, subfamily, family, superfamily, order, superorder, class, phylum, kingdom, superkingdom
|-r |--non_redundant | Makes the final database non redundant in regard to sequences, headers are concatenated.
|-z |--no_descendants| Select peptide database only by given taxon IDs, descendant taxons are excluded.
|-s |--species       | Select peptide database only until taxonomic level "species", descendants from species are excluded.
|-u |--threads       | Number of threads for using multiprocessing. Default = number of cores.
|-x |--reduce_header | Reduce the long headers of NCBI entries to accession IDs. Use only for NCBI databases.

### Dependencies:
Required databases for generation of taxon specific databases from NCBI reference database 
* protaccession2tax.gz / protaccession2tax
* pdbaccession2tax.gz
* taxdump.tar.gz
* nr.gz / nr

Required databases for generation of taxon specific databases from uniprot/swissprot/trembl reference database: 
* taxdump.tar.gz
* uniprot.fasta.gz / uniprot.fasta / uniprot_sprot.fasta.gz / uniprot_sprot.fasta / uniprot_trembl.fasta.gz / uniprot_trembl.fasta

All database files should be downloaded the same day and stored in the same folder.

#### Databases
All databases should be downloaded at the same date as the peptide database to ensure successful accession matching.
The database can be downloaded manually or downloaded by tax2proteome with option --database {ncbi, uniprot, trembl, swissprot}


| database name       | description                                                         |source | adress
| ------------------- |---------------------------------------------------------------------|-------| --------------------------------------------------------------------------------------------------------------------|
| NCBI                | non redundant peptide database                                      |NCBI   | ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nr.gz                                                                     |
| Swissprot           | curated peptide database                                            |Uniprot| ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz           |
| Trembl              | peptide database                                                    |Uniprot| ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.fasta.gz          |
| Uniprot             | concatenated swissprot and trembl database                          |Uniprot|                                                                                                                     |
| prot.accession2taxid|contain links between accession IDs and taxonomic lineage (taxon IDs)|NCBI   | ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz                                           |
| pdb.accession2taxid |contain links between accession IDs and taxonomic lineage (taxon IDs)|NCBI   | ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/pdb.accession2taxid.gz                                            |
| taxdump             |tar-gz-compressed taxdump file containing information about the phylogenetic lineage and links between taxIDs and scientific names etc.|NCBI   |ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz            |

#### Usage of tax2proteome with database download: 
All needed databases will be downloaded to specified path (option --path). If not specified a folder with name databases_DATE will be used as default.

Examples of usage:

```
python -m tax2proteome -d uniprot -i path/to/input/taxon_ID_file  -> new Folder databases_DATE with: taxdump.tar.gz, uniprot.fasta
```
```
python -m tax2proteome -i path/to/input/taxon_ID_file  -> new Folder databases_DATE with: taxdump.tar.gz, uniprot.fasta
```
```
python -m tax2proteome -d ncbi -p path/to/my_new_databases -i path/to/input/taxon_ID_file  -> new Folder/used Folder my_new_databases with: protaccession2tax.gz, pdbaccession2tax.gz, taxdump.tar.gz, nr.gz
```
#### Usage of tax2proteome if all database files are already downloaded:
positional arguments:  --path                 determines folder with all needed databases
positional arguments:  --taxon AND/OR --input at least one taxon ID or taxon ID input file must be provided
optional arguments:    --dbname               determines location/name of database (if reference database is not in --path or have different name (see table for standard names)

--path is beeing checked for all required database files and missing databases are downloaded.

Examples of usage:
```
python -m tax2proteome -p path/to/folder -n path/to/reference_database -t 11111 22222 -o path/my_taxon_specified_database.fasta
```
```
python -m tax2proteome -p path/to/folder -n path/ to/ uniprot.fasta -t 11111 22222 -i path/to/input
```
```
python -m tax2proteome -d ncbi -p path/to/folder -i path/to/input
```
```
python -m tax2proteome -d uniprot -p path/to/folder -i path/to/input -o path/to/user_specified_db.fasta
```
If path is once determined, it must not be specified again, as long as the same folder shell be used.


## Authors

* **Juliane Schmachtenberg** 

[project_on_github](https://github.com/jschmacht/tax2proteome)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
