#!/bin/zsh
rm -rf "$(dirname -- "$0")/taquin_*.txt"
for ((i=3;i<=8;i++));do
	N="$(shuf -i 5-100 -n 1)"
	python3 "$(dirname -- "$0")/../npuzzle-gen.py" -s $i -i "$N" |sed -e '/^[ \t]*#/d'|tr '\n' '-'|tr -d ' '|sed "s/--/+/g"|tr '+' '\n'|tr '-' ' '|sed '0,/ /s//\n/' > "$(dirname -- "$0")/taquin_$i.txt"
	CMP="$(python3 "$(dirname -- "$0")/../../src/npuzzle.py" "$(dirname -- "$0")/taquin_$i.txt" -c)" 
	if [ "$CMP" =  "$N" ]; then
		echo "$(dirname -- "$0")/taquin_$i.txt : \033[1;32mOK\033[0m ($CMP coups)"
	else
		echo "\033[0;31m$(dirname -- "$0")/taquin_$i.txt : KO : $CMP moves found instead of $N moves\033[0m"
	fi
done