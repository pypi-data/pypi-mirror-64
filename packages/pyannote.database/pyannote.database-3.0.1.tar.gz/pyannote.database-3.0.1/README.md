# pyannote-database

This package provides a common interface to multimedia databases and associated
experimental protocol.

<!-- @import "[TOC]" {cmd="toc" depthFrom=2 depthTo=3 orderedList=false} -->
<!-- code_chunk_output -->

* [Installation](#installation)
* [Databases & tasks](#databases-tasks)
* [Protocols](#protocols)
	* [Speaker diarization](#speaker-diarization)
	* [Collections](#collections)
	* [Speaker spotting](#speaker-spotting)
* [Custom protocols](#custom-protocols)
	* [Generic speaker diarization protocols](#generic-speaker-diarization-protocols)
	* [pyannote.database plugins](#pyannotedatabase-plugins)
	* [Meta protocols](#meta-protocols)
* [Preprocessors](#preprocessors)

<!-- /code_chunk_output -->


## Installation

```bash
$ pip install pyannote.database
```

You can install database plugins separately, for instance, the ETAPE database plugin can be installed like that:

```bash
$ pip install pyannote.db.etape
```

A bunch of `pyannote.database` plugins are already available (search for `pyannote.db` on [pypi](https://pypi.python.org/pypi?%3Aaction=search&term=pyannote.db&submit=search))

However, you might want to add (and contribute) one for your favorite databases. See [Custom protocols](#custom-protocols) for details.

## Databases & tasks

Installed databases can be discovered using `get_databases`:

```python
>>> from pyannote.database import get_databases
>>> get_databases()
['Etape']
```

Any installed database can then be imported using one of the following:

```python
# programmatically using "get_database"
>>> from pyannote.database import get_database
>>> database = get_database('Etape')
```

```python
# directly using "import"
>>> from pyannote.database import Etape
>>> database = Etape()
```

Databases usually provide high level description when printed.

```
>>> print(database)
ETAPE corpus

Reference
---------
"The ETAPE corpus for the evaluation of speech-based TV content processing in the French language"
Guillaume Gravier, Gilles Adda, Niklas Paulson, Matthieu Carré, Aude Giraudel, Olivier Galibert.
Eighth International Conference on Language Resources and Evaluation, 2012.

Citation
--------
@inproceedings{ETAPE,
  title = {{The ETAPE Corpus for the Evaluation of Speech-based TV Content Processing in the French Language}},
  author = {Gravier, Guillaume and Adda, Gilles and Paulson, Niklas and Carr{'e}, Matthieu and Giraudel, Aude and Galibert, Olivier},
  booktitle = {{LREC - Eighth international conference on Language Resources and Evaluation}},
  address = {Turkey},
  year = {2012},
}

Website
-------
http://www.afcp-parole.org/etape-en.html
```

You can also use `help` to get the list of available methods.

```
>>> help(database)
```

Some databases (especially multimodal ones) may be used for several tasks.
One can get a list of tasks using `get_tasks` method:

```python
>>> database.get_tasks()
['SpeakerDiarization']
```

One can also get the overall list of tasks, as well as the list of databases
that implement at least one protocol for a specific task.

```python
>>> from pyannote.database import get_tasks
>>> get_tasks()
['SpeakerDiarization']
>>> get_databases(task='SpeakerDiarization')
['Etape']
```

This might come handy in case you want to automatically benchmark a particular
approach on every database for a given task.

## Protocols
([↑up to table of contents](#table-of-contents))

Once you have settled with a task, a database may implement several experimental protocols for this task.
`get_protocols` can be used to get their list:

```python
>>> database.get_protocols('SpeakerDiarization')
['Full', 'Radio', 'TV']
```

In this example, three speaker diarization protocols are available: 
- one using the complete set of data;
- one using only TV data;
- one using only Radio data.

```python
>>> protocol = database.get_protocol('SpeakerDiarization', 'TV')
```

Protocols usually provide high level description when printed.

```python
>>> print(protocol)
Speaker diarization protocol using TV subset of ETAPE
```

You can also use `help` to get the list of available methods.

```python
>>> help(protocol)
```

A shortcut `get_protocol` function is available if you already know which database, task, and protocol you want to use:

```python
>>> from pyannote.database import get_protocol
>>> protocol = get_protocol('Etape.SpeakerDiarization.TV')
```

### Speaker diarization 
([↑up to table of contents](#table-of-contents))

Speaker diarization protocols implement three methods: `train`, `development` and `test` that provide an iterator over the corresponding subset.

Those methods yield dictionaries (one per file/item) that can be used in the following way:

```python
>>> from pyannote.database import get_annotated
>>> for current_file in protocol.train():
...
...     # get the reference annotation (who speaks when)
...     # as a pyannote.core.Annotation instance
...     reference = current_file['annotation']
...
...     # sometimes, only partial annotations are available
...     # get the annotated region as a pyannote.core.Timeline instance
...     annotated = get_annotated(current_file)
```

### Collections 

Collections protocols simply provide list of files:

```python
>>> protocol = get_protocol('...')
>>> for current_file in protocol.files():
...     pass
```

### Speaker spotting 

TODO


## Custom protocols
([↑up to table of contents](#table-of-contents))


### Generic speaker diarization protocols
([↑up to table of contents](#table-of-contents))

`pyannote.database` supports speaker diarization protocols out-of-the-box through the provision of RTTM (and UEM) annotation files. It relies on the `~/.pyannote/database.yml` with the following format:

```yaml
# ~/.pyannote/database.yml
Protocols:
  DatabaseName:
    SpeakerDiarization:
      ProtocolName:
        train:
            annotation: /path/to/annotation/train/file.rttm
            annotated: /path/to/annotated/train/file.uem
            uris: /path/to/list_of_uris/train/file.lst
        development:
            annotation: /path/to/annotation/dev/file.rttm
        test:
            annotated: /path/to/annotated/test/file.uem
            uris: /path/to/list_of_uris/test/file.lst
```

Path to the files are either absolute, relative to current working directory, or relative to this configuration file. You can place the configuration file anywhere as long as you tell `pyannote.database` where to find it:

```bash
export PYANNOTE_DATABASE_CONFIG="/path/to/database.yml"
```

The above configuration file would automagically make 
`DatabaseName.SpeakerDiarization.ProtocolName` protocol available:

```python
from pyannote.database import get_protocol
protocol = get_protocol('DatabaseName.SpeakerDiarization.ProtocolName')
```

All of `uris`, `annotated` and `annotation` are optional but at least one of 
them must be provided
- `uris` links to a text file containing one line per (train/dev/test) file;
- `annotated` links to an evaluation map file in UEM format;
- `annotation` links to an annotation file in RTTM format.

Though they are optional, some tasks are not possible without some of these files. 
For instance, it would not be possible to train a speech activity detection model with [`pyannote-audio`](https://github.com/pyannote/pyannote-audio) if the `annotation` file is not provided.

When two or more are provided and disagree on the list of files, `uris` will 
be prefered over `annotated`, which will be prefered over `annotation`.

When `annotated` is provided, any annotation which is outside of the `annotated` part will not be considered.

#### Domain

One can also add a `domain` key linking to a text file mapping each file to its *[domain](https://en.wikipedia.org/wiki/Domain_adaptation)*:
```
file1 domain-of-file-1
file2 domain-of-file-2
file3 domain-of-file-3
```
This will end up in the `domain` key of the `current_file` dictionary.

### pyannote.database plugins

More more complex protocols (or if you want to allow other researchers to use your protocols easily), you can create (and share) your own `pyannote.database` plugin.

See [`http://github.com/pyannote/pyannote-db-template`](http://github.com/pyannote/pyannote-db-template).

### Meta protocols
([↑up to table of contents](#table-of-contents))

`pyannote.database` provides a way to combine several protocols (possibly
from different databases) into one.

This is achieved by defining those "meta-protocols" into `~/.pyannote/database.yml`.

```yaml
# ~/.pyannote/database.yml
Protocols:
  X:
    SpeakerDiarization:
      ExtendedEtape:
        train:
          Etape.SpeakerDiarization.TV: [train]
          REPERE.SpeakerDiarization.Phase1: [train, development]
          REPERE.SpeakerDiarization.Phase2: [train, development]
        development:
          Etape.SpeakerDiarization.TV: [development]
        test:
          Etape.SpeakerDiarization.TV: [test]

```

This defines a new speaker diarization protocol called `ExtendedEtape` that is
very similar to the existing `Etape.SpeakerDiarization.TV` protocol except its
training set is augmented with (training and development) data from the
`REPERE` corpus. Obviously, both `ETAPE` and `REPERE` packages need to be
installed first (custom speaker diarization protocols are also supported):

```bash
$ pip install pyannote.db.etape
$ pip install pyannote.db.repere
```

Then, this new "meta-protocol" can be used like any other protocol of the
(fake) `X` database:

```python
>>> from pyannote.database import get_protocol
>>> protocol = get_protocol('X.SpeakerDiarization.ExtendedEtape')
>>> for current_file in protocol.train():
...     pass
```

## Preprocessors
([↑up to table of contents](#table-of-contents))

You may have noticed that the path to the audio file is not provided.
This is because those files are not provided by the `pyannote.database` packages. You have to acquire them, copy them on your hard drive, and tell `pyannote.database` where to find them.

To do that, create a file `database.yml` that describes how your system is setup:

```bash
$ cat database.yml
Databases:
  Etape: /path/where/your/stored/Etape/database/{uri}.wav
```

`{uri}` is a placeholder telling `pyannote.database` to replace it by `item[uri]` before looking for the current file.


```python
>>> from pyannote.database import FileFinder
>>> preprocessors = {'audio': FileFinder(database_yml='database.yml')}
>>> protocol = get_protocol('Etape.SpeakerDiarization.TV', preprocessors=preprocessors)
>>> for item in protocol.train():
...     # now, `item` contains a `wav` key providing the path to the wav file
...     wav = item['audio']
```

`database_yml` parameters defaults, in this order, to `database.yml` in current working directory if it exists, to the content of `PYANNOTE_DATABASE_CONFIG` environment variable when defined, and to `~/.pyannote/database.yml` otherwise, so you can conveniently use this file to provide information about all the available databases, once and for all:

```bash
$ cat ~/.pyannote/database.yml
Databases:
  Etape: /path/where/you/stored/Etape/database/{uri}.wav
  REPERE:
    - /path/where/you/store/REPERE/database/phase1/{uri}.wav
    - /path/where/you/store/REPERE/database/phase2/{uri}.wav
  VoxCeleb:
    - /path/where/you/store/voxceleb1/*/wav/{uri}.wav
    - /path/where/you/store/voxceleb1/*/wav/{uri}.wav
    - /vol/corpora4/voxceleb/voxceleb2/**/{uri}.aac
```

Note that any pattern supported by `pathlib.Path.glob` is supported (but avoid `**` as much as possible).  Paths can also be relative to the location of `database.yml`.

More generally, preprocessors can be used to augment/modify the yielded dictionaries on the fly:

```python
>>> # function that takes a protocol item as input and returns whatever you want/need
>>> def my_preprocessor_func(item):
...     return len(item['uri'])
>>> preprocessors = {'uri_length': my_preprocessor_func}
>>> protocol = get_protocol('Etape.SpeakerDiarization.TV', preprocessors=preprocessors)
>>> for item in protocol.train():
...     # a new key 'uri_length' has been added to the current dictionary
...     assert item['uri_length'] == len(item['uri'])
```
