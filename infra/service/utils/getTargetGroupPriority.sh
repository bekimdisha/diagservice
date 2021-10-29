#!/bin/bash

# This file is to generate a random unique number (between 10000 and 25000) using the domain name.
# This is to avoid services being deployed with the same priority 

#=== Script Inputs
SITE=$1
#=================

function add()
{
  result=0
  string=$1
  for (( i=0; i<${#string}; i++ ))
  do
    result=$(( $result+`echo -n "${string:$i:1}" | od -An -tuC` ))
  done
  
  echo $result;
}

echo $(( ($(add `echo "$SITE" | md5sum | cut -d " " -f1`) + $(add `echo "$SITE" | sha1sum | cut -d " " -f1`) + $(add `echo "$SITE" | sha256sum | cut -d " " -f1`) + $(add `echo "$SITE" | sha512sum | cut -d " " -f1`) + $(add "$SITE") + ${#SITE}) % 50000 ))
