#!/bin/bash

set -e

BASE_BRANCH="main"
git fetch origin $BASE_BRANCH

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" == "$BASE_BRANCH" ]; then
  echo "You are on the base branch ($BASE_BRANCH). Exiting..."
  exit 0
fi

COMMITS=$(git log origin/$BASE_BRANCH..HEAD --no-merges --pretty=format:'%H')

if [ -z "$COMMITS" ]; then
  echo "No new commits to check."
  exit 0
fi

unsigned_commits_found=false

for commit_hash in $COMMITS; do
  commit_message=$(git log -1 --pretty=format:'%s' $commit_hash)
  if ! git show -s --format=%B $commit_hash | grep -q "Signed-off-by:"; then
    echo "Commit $commit_hash is not signed off"
    echo "Commit message: $commit_message"
    echo "-------------------------------"
    unsigned_commits_found=true
  fi
done

if $unsigned_commits_found; then
  echo "One or more commits are not signed off. Failing the check."
  exit 1
else
  echo "All commits are signed off."
  exit 0
fi
