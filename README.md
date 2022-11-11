# SvenskaJa
tools for learning Swedish (verbs)

Practice to memorize
* main verb forms (presens, preteritum, supinum)
* (russian and english) translations

Install like a nerd (Windows)
* Install python (3.10+), download this repo
* Setup virtual environment: `py -m venv --upgrade-deps env`
* Activate virtual environment: `env\scripts\activate.bat`
* Install required packages: `pip install -r requirements.txt`
* To build Windows executables run `build.bat`
* To play with the code from python IDLE run `env.bat`

Install like a normal person (Windows)
* Download [SvenskaJaWin.zip](https://github.com/ilya112358/SvenskaJa/releases/latest/download/SvenskaJaWin.zip)
* UnZip to a folder

**Run maintainance (`maintain.exe/.py`) to import the word base from wordbase.txt. SQLite wordbase.db is created on the first run. You can list, lookup, delete, export entries. Add and edit entries through import.**

**Run practice.exe (`practice.exe/.py`) to improve your Swedish!**

Verb forms practice has a *spaced repetition* feature. After a successful exercise the verb is pushed down the queue, after a failed exercise the verb is brought back ahead.

Translation practice is a *multiple choice* test. Try to recall the translation first then call up choices and choose the right one.

The word base in [wordbase.txt](wordbase.txt) is an ever growing list of verbs created with info from [Svenska Akademien's dictionaries](https://svenska.se/). The base contains two types of verbs: most common and strong/irregular. Each line contains 6 comma separated fields in the strict order: Infinitive, Present, Past, Supine, Russian translation, English translation. Trailing and leading whitespace is removed. You can omit either three forms or a translation by having just commas. If a verb has multiple sets of forms (e.g., *simma*), only one set is given. Any translation is obviously an approximation, immerse into the language environment to fully grasp the meaning.
