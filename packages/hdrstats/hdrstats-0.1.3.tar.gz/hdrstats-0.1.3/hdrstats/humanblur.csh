#!/bin/csh -fe
#
# Simulate Lorentzian function with FWHM=11
#
getinfo < $1 | sed 's/^EXPOSURE=.*$/EXPOSURE=1.0/' > myhead$$.txt
set vhoriz=`sed -n 's/^VIEW=.*-vh \([^ ]*\) .*$/\1/p' myhead$$.txt`
set rhoriz=`getinfo -d < $1 | sed 's/^.*+X //'`
set pparcmin=`ev "$rhoriz/(60*$vhoriz)"`
set rad=`ev "5.7*$pparcmin" "22.6*$pparcmin" "42.4*$pparcmin"`
cat myhead$$.txt
rm -f myhead$$.txt
if ( "$rad[2]" !~ [1-9]* ) then
	echo "Input image is too small for this script"
	exit 1
endif
if ( "$rad[1]" !~ [1-9]* ) then
pcomb -s .85 -o $1 -s .11 -o "\!pgblur -r $rad[2] $1" \
		-s .04 -o "\!pgblur -r $rad[3] $1" \
	| getinfo -
else
pgblur -r $rad[1] $1 | pcomb -s .85 -o - -s .11 -o "\!pgblur -r $rad[2] $1" \
		-s .04 -o "\!pgblur -r $rad[3] $1" \
	| getinfo -
endif

