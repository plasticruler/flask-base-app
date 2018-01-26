#!/usr/bin/env bash


 say() {
     echo "$@" | sed \
             -e "s/\(\(@\(red\|green\|yellow\|blue\|magenta\|cyan\|white\|reset\|b\|u\)\)\+\)[[]\{2\}\(.*\)[]]\{2\}/\1\4@reset/g" \
             -e "s/@red/$(tput setaf 1)/g" \
             -e "s/@green/$(tput setaf 2)/g" \
             -e "s/@yellow/$(tput setaf 3)/g" \
             -e "s/@blue/$(tput setaf 4)/g" \
             -e "s/@magenta/$(tput setaf 5)/g" \
             -e "s/@cyan/$(tput setaf 6)/g" \
             -e "s/@white/$(tput setaf 7)/g" \
             -e "s/@reset/$(tput sgr0)/g" \
             -e "s/@b/$(tput bold)/g" \
             -e "s/@u/$(tput sgr 0 1)/g"
  }

say @b@green[[Activating virtualenv]]
source .venv/bin/activate
say @b@green[[Set environment variables]]
export FLASK_APP="run.py"
export FLASK_DEBUG=1
say @b@green[[Start job download-data]]
flask download-data
say @b@green[[Start job get-latest-prices]]
flask get-latest-prices
say @b@green[[Start job process-data]]
flask process-data
say @b@green[[Job run complete...]]