#!/bin/bash

echo "Building website on $(date)"
echo "Python: $(python3 --version)"

user=$GITHUB_ACTOR
pass=$GITHUB_TOKEN
repo_url="https://$user:$pass@github.com/ftc-team-8813/website"
git config user.name "$user"
git config user.email "$user@users.noreply.github.com"
echo "Committing as $user ($user@users.noreply.github.com)"

cd pages
python3 builder.py -v || exit 1

mv output/ ../../
cd ..

git checkout deploy

# delete everything EXCEPT .git
find -maxdepth 1 -type f -exec rm {} ';'
find -maxdepth 1 -type d ! -path './.git' ! -path './.git/*' ! -path '.' -exec rm -r {} ';'

# move everything back here INCLUDING dotfiles
mv ../output/.[^.]* ../output/* .
rm -r ../output/

# commit and push
git add --all
git commit -m "Deploy website"
git push "$repo_url"
