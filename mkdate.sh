#!/bin/bash
echo '\date{'$(date -r $(D=0; for i in *.tex; do E=`date -r $i +%s`; [[ $E -gt $D ]] && D=$E && FILE=$i; done; echo $FILE) "+%Y. %B %_d.")'}' >date.tex

