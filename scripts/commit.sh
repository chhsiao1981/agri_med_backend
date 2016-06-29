#!/bin/bash

if [ "${BASH_ARGC}" != 1 ]
then
  echo "usage: commit.sh [comment]"
  exit 0
fi

comment="${BASH_ARGV[0]}"
branch=`git branch|grep '*'|awk '{print $2}'`

git add .; git commit -m "${comment}"; git push origin "${branch}"
