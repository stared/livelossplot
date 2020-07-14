git checkout master
pdoc3 --html livelossplot --force --output-dir docs --skip-errors
git checkout gh-pages
git rm *html
git rm -r outputs
git rm -r inputs
mv docs/livelossplot/* .
rm -rf docs/
git add *html
git add outputs
git add inputs
