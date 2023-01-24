# SvenskaJa
tools for learning Swedish *verbs*

Practice to memorize:
* main verb forms: *presens, preteritum, supinum*
* *russian and english* translations

Install like a nerd (Windows):
* Install python (3.8.10+), download this repo
* Setup virtual environment: `py -m venv --upgrade-deps env`
* Activate virtual environment: `env.bat`
* Install required packages: `pip install -r requirements.txt` ([PyInputPlus](https://github.com/asweigart/pyinputplus) for input, [tabulate](https://github.com/astanin/python-tabulate) for output)

Install like a normal person (Windows):
* Download [SvenskaJaWin.zip](https://github.com/ilya112358/SvenskaJa/releases/latest/download/SvenskaJaWin.zip)
* UnZip to a folder

Run `maintain` to import the word base from wordbase.txt. SQLite wordbase.db is created on the first run. You can list, lookup, delete, export entries. Add and edit entries through import.

Run `practice` to improve your Swedish!

Verb forms practice has a **spaced repetition** feature. After a successful exercise the verb is pushed down the queue, after a failed exercise the verb is brought back ahead. You have an option to practice forms of non-trivial (not group-1) verbs only.
![2023-01-24 174216](https://user-images.githubusercontent.com/9436418/214324694-b00d7aee-39d4-4b5c-9e54-ffc51839d0c7.png)

Translation practice is of two types: a **multiple choice** test and a **flashcard** test with spaced repetition. Try to recall the translation first then either call up choices and choose the right one (multiple choice), or input whether or not you remembered correctly (flashcard).
![2023-01-24 174607](https://user-images.githubusercontent.com/9436418/214325525-12e9b678-0f6f-4156-a0b7-ccd77f7e9594.png)

[The word base](wordbase.txt) is an ever growing list of verbs, their conjugations and translations. The base aims to contain verbs which are common (A1, A2) or difficult (strong, irregular) with easiest group-1 English cognates (e.g., *kommentera*) excluded. 

Each line contains 6 comma separated fields in the strict order: Infinitive form, Present form, Past form, Supine form, Russian translation, English translation. Trailing and leading whitespace is removed. You can omit either three forms or a translation by having just commas. If a verb has multiple sets of forms (e.g., *simma*), only one set is given. Any translation is obviously an approximation, immerse into the language environment to fully grasp the meaning.

Add the verbs which you manually deleted or changed into `ignore.txt` to prevent updating during the next import.
