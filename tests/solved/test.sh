#!/bin/zsh
rm -rf "$(dirname -- "$0")/taquin_*.txt"
for ((i=3;i<=9;i++));do 
   python3 "$(dirname -- "$0")/../npuzzle-gen.py" -s $i -i 0 |sed -e '/^[ \t]*#/d'|tr '\n' '-'|tr -d ' '|sed "s/--/+/g"|tr '+' '\n'|tr '-' ' '|sed '0,/ /s//\n/' > "$(dirname -- "$0")/taquin_$i.txt"
   CMP="$(python3 "$(dirname -- "$0")/../../src/npuzzle.py" "$(dirname -- "$0")/taquin_$i.txt")" 
   if [ "$CMP" = "Already solved" ]; then
    	echo "$(dirname -- "$0")/taquin_$i.txt : \033[1;32mOK\033[0m"
	else
    	echo "\033[0;31m$(dirname -- "$0")/taquin_$i.txt : KO\033[0m"
	fi
done