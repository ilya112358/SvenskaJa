# SvenskaJa
tools for learning Swedish (verbs)

Practice to memorize
* main verb forms (presens, preteritum, supinum)
* (russian) translations

Install like a nerd (Windows)
* Install python (3.10+) and git, clone this repo
* Setup virtual environment: py -m venv --upgrade-deps env
* Activate virtual environment: env\scripts\activate.bat
* Install required libs: pip install -r requirements.txt
* To build Windows executables run build.bat
* To play with code from python IDLE run env.bat

Install like a normal person (Windows)
* Download [SveskaJaWin.zip](https://github.com/ilya112358/SvenskaJa/blob/310323ade6cfb334c3b54d505d8d776784c5304f/executable/SvenskaJaWin.zip)
* UnZip to a folder

**Run maintainance (maintain.exe/py) to import the word base from wordbase.txt. SQLite wordbase.db is created on the first run. You can lookup, add, delete, export entries.**

**Run practice.exe (practice.exe/py) to improve your Swedish!**

wordbase.txt is an ever growing list of verbs created with info from [Svenska Akademien's dictionaries](https://svenska.se/). Each line contains 5 comma separated fields in the strict order: Infinitiv, Presens, Preteritum, Supinum, Russian translation. Trailing and leading whitespace is removed. You can omit either three forms or a translation by having just commas. If a verb has multiple sets of forms (e.g., *simma*), only one set is given. Any translation is obviously an approximation, immerse into the language environment to fully grasp the meaning. Feel free to change the word base to your liking.

Verb forms practice has a spaced repetition feature. After successful exercise the verb is pushed down the queue, after failed exercise the verb is brought back ahead.

Translation practice is a choice based test. Try to recall the translation first then call up choices and choose the right one.
