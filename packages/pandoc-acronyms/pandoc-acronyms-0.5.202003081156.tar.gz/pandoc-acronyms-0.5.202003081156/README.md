# pandoc-acronyms - A Pandoc filter for managing acronyms

## Acronyms? WTF?

There is a convention in more precise writing to provide the full text
of an acronym at first use. This can get difficult for example if the
text of documents is split over multiple files, which makes it hard
for the authors to know where the acronym will be used first. Such a
task is best left to the computer. This is what the `pandoc-acronyms`
filter is for. Authors list acronyms in a data file and then reference
them in the text.

## HOWTO: [`pip install pandoc-acronyms`](https://pypi.org/project/pandoc-acronyms/)

Write a data file that contains your acronyms:

    {
		"aba": {
			"shortform": "ABA",
			"longform": "a better acronym"
		},
		"bba": {
			"shortform": "BBA",
			"longform": "beer brewing attitude"
		}
	}

Then in the text, use the acronym in encoded form like `[!bba]`. The
filter will recognize it. On first use it replaces the marker with
"beer brewing attitude (BBA)".  Any later use will be replaced by
"BBA". The filter will print a notice if an acronym is found in the
text that is not defined in the data file. The keys start with a
character and may consist of letters, numbers, dashes, the plus sign
and underscores ("a-b", "ab", "a_b" or "c++", but not "++c").

The replacements will be made to the text and are independent of the
selected output format. While tools such
as [pandoc-ac](https://github.com/Enet4/pandoc-ac) help users with
generating acronym commands in LaTeX, `pandoc-acronyms` is designed to
work directly on the document text.

## Using acronyms in the input text

The most common way to write an acronym in the text is [!key]. To customize the output, the acronym specification can be made more specific:

* [!+key] selects the plural form of the acronym.
* [!^key] selects the uppercase form of the acronym. This only affects the long form, the abbreviated short form will not be changed.
* [!+^key] For plural uppercase variants, plural must be specified first.

It is also possible to select which form should be inserted into the text (this can be combined with plural or uppercase selection):

* [!key>] inserts the long form ("beer brewing attitude").
* [!key<] inserts the short form ("BBA").
* [!key!] inserts the explained form ("beer brewing attitude (BBA)").

## Using the filter with pandoc

The filter mechanism is a built-in feature of pandoc. The filter is
added to how pandoc is invoked:

	> pandoc --filter pandoc-acronyms document.md

Pandoc does not allow to pass parameters to filters. The
acronym filter needs to load the acronyms from the data file. To work
around this, the parameters to the filter can be passed in environment
variables:

	> pandoc-acronyms --help
	Usage: pandoc-acronyms [OPTIONS] [FORMAT]...

	The pandoc-acronyms filter.

	Options:
		-a, --acronyms TEXT           A file with acronym definitions in JSON
        		                      format.
		-v, --verbose / --no-verbose  Enable verbose output.
		-s, --suggest / --no-suggest  Suggest marking acronyms detected in the text.
		-e, --error / --no-error      Exit with an error if an undefined acronym is
									  used.
		-d, --debug / --no-debug      Enable debug output.
		--version                     Show the version and exit.
		--help                        Show this message and exit.

The environment variable PANDOC_ACRONYMS_ACRONYMS can be used to
replace the --acronyms option. Similarly, the variable
PANDOC_ACRONYMS_VERBOSE enables diagnostic output. All command line options
of `pandoc-acronyms` can be controlled with environment variables the same
way:

* --acronyms: PANDOC_ACRONYMS_ACRONYMS
* --verbose/--no-verbose: PANDOC_ACRONYMS_VERBOSE
* --suggest/--no-suggest': PANDOC_ACRONYMS_SUGGEST
* --error/--no-error: PANDOC_ACRONYMS_ERROR
* --debug/--no-debug: PANDOC_ACRONYMS_DEBUG

## Installation

The `pandoc-acronyms` program is released via the [Python Package Index](https://pypi.org/):

	> pip install pandoc-acronyms
	...

Alternatively, developers can clone
the [main repository](https://gitlab.com/mirkoboehm/pandoc-acronyms)
and install using Python setuptools:

	> python setup.py install
	...

Once installed either way, the filter is available as a stand-alone program in the
installation location used by Python.

## Testing and debugging

The `pandoc-acronyms` code uses the standard Python unittest
framework. Most tests are data-driven in that they use regular
Markdown files and JSON acronym dictionaries as input and test how the
code handles them. To test the filter code as regular Python unit
tests, test Markdown input is first converted into the Pandoc "native
JSON" format in memory and then fed to the filter code by the
tests. This means the unit tests run stand-alone (without the need for
Pandon to invoke them as a filter), making the test code easily
debugable.

## How to contribute

The
[Git repository for the pandoc acronym filter](https://gitlab.com/mirkoboehm/pandoc-acronyms) is
hosted on Gitlab. It uses the Gitlab CI system to ensure quality, also
for development branches and incoming merge requests. Deployment
to [PyPI](https://pypi.org/) is automated. Development branches and
merge requests will be deployed to
the
[PyPI test instance](https://test.pypi.org/project/pandoc-acronyms/)
as development packages. Commits to master will be deployed to regular
PyPI as development packages. Tagged versions on master are deployed
to PyPI
as
[stable releases](https://pypi.org/project/pandoc-acronyms/#history).

To contribute, please submit a merge request. Your merge
request should maintain or increase the test coverage.
