# marytts-cli

A command-line client for the HTTP server of the MaryTTS Text-to-Speech System
implemented in Python 3.

## Table of Contents

* [About](#about)
* [Installation](#installation)
* [Usage](#usage)
* [Author](#author)
* [License](#license)

## About

The `marytts-cli` command-line client for the MaryTTS Text-to-Speech System is
a handy tool for experimenting with the TTS server itself and for simplifying
the automation process of regular TTS tasks.

It performs a query to the HTTP server of MaryTTS with a range of configurable
parameters and returns the server's response. Input data for the query is read
from `stdin` while parameters are set by invoking their corresponding
command-line arguments.

If the query was successful, received output data is written to `stdout` and
the program terminates with exit code *0*. Otherwise, an error message is
written to `stderr` and the program terminates with exit code *1*.

## Installation

To install the required `requests` library for Python 3, run:

```
pip install -r requirements.txt
```

## Usage

```
usage: marytts-cli [-h] [--audio AUDIO] [--input INPUT] [--locale LOCALE]
                   [--output OUTPUT] [--url URL] [--voice VOICE]

A command-line client for the HTTP server of the MaryTTS Text-To-Speech System.

optional arguments:
  -h, --help       show this help message and exit
  --audio AUDIO    set format of MaryTTS audio output
  --input INPUT    set type of MaryTTS input
  --locale LOCALE  set identifier of Locale
  --output OUTPUT  set type of MaryTTS output
  --url URL        set request URL
  --voice VOICE    set name of MaryTTS voice
```

**Example**

```
echo "Hello World!" | ./marytts-cli > output.wav
```

## Contribution

Pull requests, patches and feedback are always welcome. Feel free to use the
issue tracker or to contact the author.

## Author

trevor &lt;trevor@destroyed.today&gt;

## License

Distributed under the MIT License. See `LICENSE` for more information.
