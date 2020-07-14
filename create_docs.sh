git checkout master
pdoc3 --html livelossplot --force --output-dir docs --skip-errors
git checkout gh-pages

echo "Remove old docs"
git rm *html
git rm -r outputs
git rm -r inputs

echo "Move new docs and stage it"
mv docs/livelossplot/* .
rm -rf docs/
git add *html
git add outputs
git add inputs

echo "Please check staged docks and commit it if everything looks good"
