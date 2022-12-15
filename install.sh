#!/bin/bash

CONFIGDIR=~/.github_tracker


if [ -d $CONFIGDIR ]; then
	echo "$CONFIGDIR already exists!"
	exit
fi


mkdir $CONFIGDIR
mkdir $CONFIGDIR/avatars
echo "" > $CONFIGDIR/accounts.txt
mkdir $CONFIGDIR/res


