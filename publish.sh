# build and publish to
# https://pypi.org/project/livelossplot/
rm -r dist/
python setup.py sdist bdist_wheel
twine upload dist/*
