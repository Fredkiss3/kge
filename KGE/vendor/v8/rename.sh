#!/bin/bash

# ls -R . | awk '/:$/&&f{s=$0;f=0} /:$/&&!f{sub(/:$/,"");s=$0;f=1;next} NF&&f{ print s"/"$0 }'

#files=$(ls -R . | awk '/:$/&&f{s=$0;f=0} /:$/&&!f{sub(/:$/,"");s=$0;f=1;next} NF&&f{ print s"/"$0 }')
files=$(find . -type f \( -iname \*.cc -o -iname \*.h \))

for file in $files; do
	echo "Modifying file $file"
	sed -i -E 's/#include "src\/(\/?[a-zA-Z_-]+\/)*([a-zA-Z_1-9-]+\.h)"/#include "\2"/g' $file
done
