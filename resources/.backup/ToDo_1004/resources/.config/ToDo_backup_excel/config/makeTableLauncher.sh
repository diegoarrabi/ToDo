#!/bin/zsh

export PYENV_ROOT="$XDG_CONFIG_HOME/pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

cd /Users/diegoibarra/Developer/1_myProjects/Apps/ToDo

python3 makeTable.py