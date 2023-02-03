# SvenskaJa
tools for learning Swedish *verbs*

Practice to memorize:
* main verb forms: *presens, preteritum, supinum*
* *russian and english* translations

Install like a nerd (Windows):
* Install python (3.8.10+), download this repo
* Setup virtual environment: `py -m venv --upgrade-deps env`
* Activate virtual environment: `env.bat`
* Install required packages: `pip install -r requirements.txt` ([PyInputPlus](https://github.com/asweigart/pyinputplus) for input, [tabulate](https://github.com/astanin/python-tabulate), [colorama](https://github.com/tartley/colorama) for output)

Install like a normal person (Windows):
* Download [SvenskaJaWin.zip](https://github.com/ilya112358/SvenskaJa/releases/latest/download/SvenskaJaWin.zip)
* UnZip to a folder

Run `maintain` to import the word base from wordbase.txt. SQLite wordbase.db is created on the first run. You can list, lookup, delete, export entries. Add and edit entries through import.

Run `practice` to improve your Swedish!

Verb forms practice has a **spaced repetition** feature. After a successful exercise the verb is pushed down the queue, after a failed exercise the verb is brought back ahead. For group 1 verbs you can substitute past and supine forms with _ade_ and _at_.

![2023-02-03 160511](https://user-images.githubusercontent.com/9436418/216610669-dd2c9b4c-1cc1-4d75-ac12-b8d1627e82ac.png)

Translation practice is of two types: **multiple choice** test and **flashcard** test with spaced repetition. Try to recall the translation first then either call up choices and choose the right one (multiple choice), or input whether or not you remembered correctly (flashcard).

![2023-01-24 174607](https://user-images.githubusercontent.com/9436418/214325525-12e9b678-0f6f-4156-a0b7-ccd77f7e9594.png)

[The word base](wordbase.txt) is an ever growing list of verbs, their conjugations and translations. The base aims to contain verbs which are common (A1, A2) or difficult (non group 1).

Each line contains 6 comma separated fields in the strict order: Infinitive form, Present form, Past form, Supine form, Russian translation, English translation. Trailing and leading whitespace is removed. You can omit either three forms or a translation by having just commas. If a verb has multiple sets of forms (e.g., *simma*), only one set is given. Any translation is obviously an approximation, immerse into the language environment to fully grasp the meaning.

Add the verbs which you manually deleted or changed into `ignore.txt` to prevent updating during the next import.
