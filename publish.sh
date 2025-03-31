# build and publish to
# https://pypi.org/project/livelossplot/
rm -rf dist/
python -m build
twine upload dist/*
