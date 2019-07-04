#!/usr/bin/bash
path=$(pwd)

for java_lib in $(ls $path/libs);do
if [[ libs != "" ]];then
    libs=$libs:$path/libs/$java_lib
else
    libs=$path/libs/$java_lib
fi
done

for java_lib in $(ls $path/libs);do
    libs=$path/libs/$java_lib
done

if ! which java >/dev/null;then
    echo "jdk version error";
    exit
fi


java -Dfile.encoding=utf-8 -Xbootclasspath/a:$libs -jar $path/bin/out.jar
