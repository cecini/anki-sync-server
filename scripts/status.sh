#!/bin/bash

#echo "STABLE_BUILDHASH $(git --git-dir /workspaces/anki  rev-parse --short=8 HEAD || echo nogit)"
#echo "STABLE_BUILDHASH $(git --git-dir ../net_ankiweb_anki  rev-parse --short=8 HEAD || echo nogit)"
echo "STABLE_BUILDHASH $(git  rev-parse --short=8 HEAD || echo nogit)"
