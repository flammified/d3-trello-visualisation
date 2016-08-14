#!/usr/local/bin/bash
#@Author Dimitry Volker
declare -A contrArray
usage="$(basename "$0") path -- program to get the authors and how many lines he changed in the git project"


#Getting the contributors form repo's
while read line; do
  #clone the repository
  REPO="$line";A=($REPO);FOLDER=$(basename ${A[1]});FOLDER=${FOLDER%%.*};
  git clone -b $line $FOLDER; printf "\n"; CRWRD=$(pwd); cd $FOLDER;

  echo "$(git log --format='%aN' | sort -u)" > authors.txt;
  GITREP=$(git remote show origin -n | grep h.URL | sed 's/.*://;s/.git$//')
  FILENAME=contribution_$(basename $GITREP)

  touch FILENAME.txt

  while read author_line; do
       echo $author_line >> $FILENAME.txt
       git log --author="$author_line" --pretty=tformat: --numstat | awk '{ add += $1; subs += $2; loc += $1 - $2 } END { printf "  added lines: %s, removed lines: %s, total lines: %s\n": add, subs, loc }' - >> $FILENAME.txt
  done < authors.txt
  mv $FILENAME.txt $CRWRD/$FILENAME.txt; cd $CRWRD; rm -rf $FOLDER;
done < repo.txt


#Get every lines edited and created
LINE_COUNT="0";INT_COUNT="0";
for f in contribution_*.txt; do
    echo "Processing $f file..";
    while read line; do
        if [[ $LINE_COUNT = "0" ]]; then
             AUTHOR=$line; ADD_C="0"; DEL_C="0";
        fi
        for a in $(echo $line | grep -o -E '[0-9]+' | head -2 | sed -e 's/^0\+//'); do
            if [[ $INT_COUNT = "0" ]]; then
                 ADD_C=$(($ADD_C+$a)); INT_COUNT="1";
            elif [[ $INT_COUNT = "1" ]]; then
                 DEL_C=$(($DEL_C+$a)); INT_COUNT="0";
            fi
        done;

        if [[ $LINE_COUNT = "1" ]]; then
            LINE_COUNT="0"
            AUTHOR=$(echo $AUTHOR | tr -d ' ')
            if [[ ${contrArray[$AUTHOR] } ]]; then
                IFS=', ' read -r -a tmpArray <<< "${contrArray[$AUTHOR]}"
                ADD_C2=${tmpArray[0]}; DEL_C2=${tmpArray[1]};
                ADD_C=$(($ADD_C+$ADD_C2)); DEL_C=$(($DEL_C+$DEL_C2));
            fi
            contrArray[$AUTHOR]="$ADD_C,$DEL_C"
        elif [[ $LINE_COUNT = "0" ]]; then
             LINE_COUNT=$(($LINE_COUNT+1))
        fi
    done < $f;
done
touch sum.txt

for i in "${!contrArray[@]}"; do
  echo "$i ${contrArray[$i]}" >> sum.txt
done
