#!/bin/bash -e

rm -rf gen
mkdir -p gen/images
cp static/*.html gen/
cp static/*.js gen/ # js minimization can be added here
cp static/*.css gen/
cp static/images/* gen/images/

if convert -version >/dev/null
then
	for f in static/images/background-*
	do
		convert "$f" -resize '64x64>' "gen/${f#static}"
	done
else
	echo "warning: convert not found: backgrounds won't be resized" >&2
fi

zip -r -9 gen/messy-chat.zip *.py README.md gen
