@echo *** SvenskaJa ***
@echo Run `maintain` for the word base maintenance, `practice` to exercise.
@echo off
doskey maintain=py -m maintain
doskey practice=py -m practice
cmd /k env\scripts\activate.bat
