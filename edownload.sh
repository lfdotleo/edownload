#!/bin/bash

# ./edownload.sh <referer> <m3u8_url> <ts_url> <filename>

out_dir="./out"
mkdir $out_dir
referer=$1
referer=$(echo $referer | sed "s/\\\\//g")
m3u8_url=$2
m3u8_url=$(echo $m3u8_url | sed "s/\\\\//g")
ts_url=$3
ts_url=$(echo $ts_url | sed "s/\\\\//g")
file_name=$4
file_name=${file_name// /}
m3u8_file="$file_name.m3u8"
ts_file="pwd_$file_name.ts"
key_file="$file_name.KEY"
final_file="$out_dir/$file_name.ts"

wget -E --referer "$referer" -r -m "$m3u8_url" -O "$m3u8_file"

start=0
end=$(tail -2 $m3u8_file | grep 'end' | awk -F 'end=|&type' '{print $2}')
ts_url=$(echo $ts_url | sed "s/\(start=\).*\(&end\)/\1${start}\2/g")
ts_url=$(echo $ts_url | sed "s/\(end=\).*\(&type\)/\1${end}\2/g")
wget -E --referer "$referer" -r -m "$ts_url" -O "$ts_file"

wget $(grep -m 1 'EXT-X-KEY' $m3u8_file | awk -F "URI=\"|\",IV" '{print $2}') -O $key_file

php -f decode.php $ts_file $key_file $final_file

rm -f $m3u8_file
rm -f $ts_file
rm -f $key_file

