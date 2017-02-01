[![Build Status](https://travis-ci.org/icgc-dcc/egasub.png)](https://travis-ci.org/icgc-dcc/egasub)

#EGASUB - ICGC EGA Submission CLI

EGASUB is a command line tool assists ICGC members submitting their NGS sequence data to EGA repository.


##Installation

```
# install pipsi
curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | python

# clone the source code
git clone git@github.com:icgc-dcc/egasub.git

# run tests
cd egasub
python setup.py test

# install egasub
pipsi install .
```

## Run

Once installed, you can invoke the tool as follow. This will display information about how to use sub-commands and their options.
```
egasub
```

### Create a workspace for EGA submission

The first thing you need is to create a directory to organize all EGA submission data and metadata. This dirctory is called an EGA submission `workspace`.

You may create an empty directory and initialize it to make it a `workspace` using the following commands:
```
mkdir my_ega_submissions
cd my_ega_submissions
egasub init
```

### Create a submission batch

A submission batch is a directory which contains multiple submission directories with same data types that are intended to be submitted to EGA more or less together in a short period of time.

There are three different submission data types: unaligned, alignment and variation.

The directory name of a submission batch must follow this naming pattern: `{submission_data_type}.*`. For examples, `unaligned.abc`, `alignment.20170201` or `variation.batch_1`.

Submission batch directory must be created directly under an EGA submission `workspace`. The following are good submission batch directories:
```
my_ega_submissions/unaligned.abc
my_ega_submissions/alignment.20170201
my_ega_submissions/variation.batch_1
```
Note that you need to create submission batch directories yourself.

### Create a submission directory

Next step is to create submission directory. A submission directory contains one metadata file and one or more data files (index file such as `.bai` files may be included).

The metadata file is named as `experiment.yaml` for `unaligned` submission data type; `analysis.yaml` for `alignment` and `variation` data types.

A submission directory can be named as whatever is useful and meaningful to you, usually, it may be named as a sample ID for a submission that contains data derived from this sample.

The following command (executed from under `my_ega_submissions/unaligned.abc`) will initialize the directory `sample_x` as a submission directory for submitting unaligned raw sequence data.
```
mkdir sample_x
egasub new sample_x
```

Once done, a metadata template file named `experiment.yaml` will be created under `my_ega_submissions/unaligned.abc/sample_x`.

You may now edit this YAML file to fill out needed metadata information regarding experiment, sample, run and data files.

### Adding data files to a submission directory
Data file, such as, unaligned FASTQ files are usually compressed with gz and placed in a submission directory created in the previous step. Information about the data file(s), such as file name, file md5sum etc, will need to be added in the metadata YAML file. Data files will also need to be encrypted before submitting to EGA. Please refer to EGA documentation for details (added link here).

Naming pattern for data files:
||Data type||File type||Encrypted file||md5sum file for encrypted data file||md5sum file for uncrypted data file||
|Unaligned sequencing reads|FASTQ|{name_of_your_choice}.fq.gz.gpg|{name_of_your_choice}.fq.gz.gpg.md5|{name_of_your_choice}.fq.gz.md5|
|Alinged sequencing reads|BAM|{name_of_your_choice}.bam.gpg|{name_of_your_choice}.bam.gpg.md5|{name_of_your_choice}.bam.md5|
|Aligned sequencing reads|BAI|{name_of_your_choice}.bam.bai.gpg|{name_of_your_choice}.bam.bai.gpg.md5|{name_of_your_choice}.bam.bai.md5|
|Variation calls|VCF|{name_of_your_choice}.vcf.gz.gpg|{name_of_your_choice}.vcf.gz.gpg.md5|{name_of_your_choice}.vcf.gz.md5|
|Variation calls|VCF index|{name_of_your_choice}.vcf.gz.idx.gpg|{name_of_your_choice}.vcf.gz.idx.gpg.md5|{name_of_your_choice}.vcf.gz.idx.md5|

File with `{file_name}.md5` suffix contain the md5sum string for the data file named `{file_name}`

### Transfer data files to the EGA FTP
After encryption, data files can then be transferred to EGA FTP server. This can be done using any FTP transfer tool. EGA also provides high speed upload using the Aspera tool (link to EGA).

The data directory structure on the EGA FTP server must be organized the same way as how we described here under a local EGA submission `workspace`.

Note that the `egasub` client tool does not perform any of the file upload activities although it will verify existence of relevant data files on the FTP server.

### Submit metadata to EGA

Before the actual submission, `dry_run` command can be used to validate metadata first.
```
egasub dry_run sample_x
```
This will report issues that need to be fixed before submitting to EGA.

Finally, we are ready to submit metadata to EGA. To do that for the submission directory created in a previous step, for example, `sample_x`, perform the following command:
```
egasub submit sample_x
```

## Support

Full version of the EGA submission standard operating procedure (SOP) can be found here: (add link). Should you need further assistance, please contact ICGC DCC at `dcc-support@icgc.org`.


