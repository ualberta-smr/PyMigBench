cp ../LICENSE .
cp ../version ./.publish/

rm -r dist
py -m build

