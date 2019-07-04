path=$(pwd)
dependence(){
for file in `ls $1|grep -v ".bak"`
  do
    if [ -d $1"/"$file ]
    then
      dependence $1"/"$file
    else
      local file_path=$1"/"$file 
      if echo $file_path|grep "MANIFEST.MF">/dev/null;then
      c=c
      else
          echo $file_path >> $path/build/source.txt
      fi
    fi
  done
}

dependence $path/src
libs=""
for java_lib in $(ls $path/web/WEB-INF/lib);do
if [[ libs != "" ]];then
libs=$libs:$path/web/WEB-INF/lib/$java_lib
else
libs=$path/web/WEB-INF/lib/$java_lib
fi
done

javac -encoding utf-8 -Xlint:unchecked -d $path/build -classpath $path/web/WEB-INF/lib @$path/build/source.txt
jar cvf  $path/src/MANIFEST.MF  $path/bin/classdesign.war ./*
