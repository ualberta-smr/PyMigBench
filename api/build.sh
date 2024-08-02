cp ../LICENSE .
cp ../README.md ./.publish/
cp ../version ./.publish/

rm -r dist
py -m build

