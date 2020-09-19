#!/bin/bash

echo "Building website on $(date)"
echo "Python: $(python3 --version)"

user=$GITHUB_ACTOR
pass=$GITHUB_TOKEN
repo_url="https://$user:$pass@github.com/ftc-team-8813/ftc_www"

cd pages
python3 builder.py || exit 1

mv output/ ../../
cd ..
files_to_copy=( .well-known/ assets/ materialize/ .nojekyll CNAME favicon.ico robots.txt)
for f in ${files_to_copy[@]}; do
  mv $f ../output/
done

git checkout deploy

# delete everything EXCEPT .git
rm *
find -type d ! -path './.git' ! -path './.git/*' -exec rm -r {} ';'

# move everything back here
mv ../output/* .
rm -r ../output/

# commit and push
# git add --all
# git commit -m "Deploy website"
# git push
