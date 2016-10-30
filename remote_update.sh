#!/bin/bash
# This script updates the piWordClock repository from a remote machine.
# It is necessary that you added your SSH Key to the host machine. You can do this via:
# ssh-copy-id user@hostname

echo Connecto to: $1@$2
ssh $1@$2 'bash -s' << END
	git -C ~/piWordClock/ fetch
	git -C ~/piWordClock/ pull
	exit
END
