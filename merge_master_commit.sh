#!/bin/bash
set -e

COMMIT_SHA=""
if [[ $COMMIT_SHA == "" ]];then
  echo "[ERROR] enter commit sha from master PX4-Autopilot && git submodule | grep mavlink"
  exit 1
fi

git remote add upstream git@github.com:mavlink/mavlink.git
git fetch upstream
git checkout  -b merge_upstream
git checkout -b upstream_base $COMMIT_SHA

git checkout merge_upstream
git merge upstream_base