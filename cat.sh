#!/bin/bash
export TERM=xterm

ncol=$(tput cols)

t[0]='  ∧＿∧  '
t[1]=' ( ･-･) '
t[2]='―∪――――∪―'
t[4]='________'
t[5]=' |    | '
t[6]=' |    | '
t[7]='  U  U  '

#################################

DRAWING_WIDTH=8
OUTPUT_INDEX=3
UPPER_LINE_CHAR="―"
LOWER_LINE_CHAR="_"
UPPER_LINE_INDEX=2
LOWER_LINE_INDEX=4
PADDING=0
DRAWING_POSITION=25

#################################

arrayLen=${#t[@]}
halfDrawingLen=$((DRAWING_WIDTH / 2))

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <string> <number>"
    exit 1
fi

if ! [[ "$2" =~ ^[0-9]+$ ]]; then
    echo "Second argument must be a number"
    exit 1
fi

leadingSpaces=$((($2 - halfDrawingLen)))

if [[ $leadingSpaces -lt 0 ]]; then
  leadingSpaces=0
fi

trailingSpaces=$((ncol - leadingSpaces - DRAWING_WIDTH))
if [[ $leadingSpaces -gt $((ncol - DRAWING_WIDTH)) ]]; then
    leadingSpaces=$((ncol - DRAWING_WIDTH))
    trailingSpaces=0
fi

text_indent=$((leadingSpaces))

echo ""
for i in $(seq 0 $arrayLen); do
  if [[ $i = $OUTPUT_INDEX ]]; then
    for n in $(seq 1 $PADDING); do
      echo ""
    done
    printf "%*s" $text_indent ""
    echo -e "|\033[1m$1\033[0m|"
    for n in $(seq 1 $PADDING); do
      echo ""
    done
  else
    car=""
    if [[ $i = $UPPER_LINE_INDEX ]]; then
      car=$UPPER_LINE_CHAR
    elif [[ $i = $LOWER_LINE_INDEX ]]; then
      car=$LOWER_LINE_CHAR
    else
      car=" "
    fi
    for s in $(seq 1 $leadingSpaces); do
      printf "$car"
    done
    printf "${t[$i]}"
    if [[ $i -eq $LOWER_LINE_INDEX || $i -eq $UPPER_LINE_INDEX ]]; then
      for s in $(seq 1 $trailingSpaces); do
        printf "$car"
      done
      printf "\n"
    else
      printf "\n"
    fi
  fi
done
echo ""