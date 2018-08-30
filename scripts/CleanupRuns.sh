#! /bin/bash

# intended to run from dir containing batch_* and 5??????

for i in $( ls -d 5?????? );
do
    echo ${i}
    rm -f ${i}/output/*
    cd $i
    for j in $( ls -d work/* );
    do
	rm -f ${j}/*
    done
    cd ..
done

for i in $( ls -d batch_* );
do
    echo ${i}
    rm -f ${i}/*.error ${i}/*.output ${i}/*.cobaltlog ${i}/host_*.txt
done
