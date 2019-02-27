# binonymizer

Binonymizer is a tool in Python that aims at tagging personal data<sup>1</sup> in a parallel corpus.

For example, for a input like:

```
URL1  URL2  My name is Marta and my email is fake@email.com    Mi nombre es Marta y mi email es fake@email.com
```

Binonymizer's output will be:

```
URL1 URL2 My name is <entity class="PER">Marta</entity> and my email is <entity class="EMAIL">fake@email.com</entity> Mi nombre es <entity class="PER">Marta</entity> y mi email es <entity class="EMAIL">fake@email.com</entity>
```
## Detectable entity tipes

Currently, the Binonymizer is able to detect and tag the following types of entities:

* PER: person names
* ORG: organism and company names
* EMAIL: email addresses
* PHONE: phone numbers
* ADDRESS: addresses
* ID: personal card IDs (such as spanish DNIs)
* MISC: other personal data, or when the type it's uncertain 
* OTHER: other

## Installation & Requirements

Binonymizer works with Python 3.6, and can be installed with `pip`:

```
python3.6 -m pip install binonymizer
```

After installation, two  binary files (`binonymizer` and `binonymizer-lite`) will be located in your `python/installation/prefix`/bin directory.

Language-dependant packages and models are automatically downloaded and installed on runtime, if needed.

### Extra instructions for basque

In case you plan to binonymize basque data, you need to download `binonymizer` from [github](http://github.com/bitextor/binonymizer), and run the following steps:

```bash
cd binonymizer
git submodule sync
git submodule update --init --recursive --remote
cd prompsit_python_bindings
python3.6 setup.py install
```
Please note that you need to have access to Prompsit's private repository. [Contact us](mailto:help@prompsit.com) if you need further details.

## Usage

Binonymizer can be run with:

```bash
binonymizer [-h] --format {tmx,cols} [--tmp_dir TMP_DIR]
                     [-b BLOCK_SIZE] [-p PROCESSES] [-q] [--debug]
                     [--logfile LOGFILE] [-v]
                     input [output] srclang trglang
```


### Parameters
* positional arguments:
  * input: File to be anonymized (See format below)
  * output: File with anonymization annotations (default: standard output)
  * srclang: Source language code of the input
  * trglang: Target language code of the input
* optional arguments:
  * -h, --help: show this help message and exit
* Mandatory:
  * --format {tmx,cols}: Input file format. Values: cols, tmx  ("cols" format: URL1 URL2 SOURCE_SENTENCE TARGET_SENTENCE [extra columns] tab-separated)
* Optional:
  * --tmp_dir TMP_DIR: Temporary directory where creating the temporary files of this program (default: default system temp dir, defined by the environment variable TMPDIR in Unix)
  * -b BLOCK_SIZE, --block_size BLOCK_SIZE: Sentence pairs per block (default: 10000)
  * -p PROCESSES, --processes PROCESSES: Number of processes to use (default: all CPUs minus one)
* Logging:
  * -q, --quiet: Silent logging mode (default: False)
  * --debug: Debug logging mode (default: False)
  * --logfile LOGFILE: Store log to a file (default: standard error output)
  * -v, --version: show version of this script and exit

### Example
```bash
binonymizer corpus.en-es.raw corpus.en-es.anon en es --format cols  --tmp_dir /tmpdir -b50000 -p31 
```
This will read the corpus "corpus.en-es.raw", which is in a column-based format, extracting personal data and writing the tagged output in "corpus.en-es.anon". Binonymizer will run in blocks of 50000 sentences, using 31 cores, and writing temporary files in /tmpdir


## Lite version

Although `binonymizer` makes use of parallelization by distributing workload to the available cores, some users might prefer to implement their own parallelization strategies. For that reason, a single-thread version of the script is provided: `binonymizer_lite`. The usage is exactly the same as for the full version, but omitting the blocksize (-b) and processes (-p) parameter.


## TO DO
* Fully support TMX input/output
* Address recognition
* GPU support
* Automate Prompsit-python-bindings submodule ( git submodule update --remote ,  python3.6 setup.py install)



<sup>1</sup>: See EC definition of "personal information": https://ec.europa.eu/info/law/law-topic/data-protection/reform/what-personal-data_en
