#!/bin/bash


# bash <(curl https://raw.githubusercontent.com/KittKat7/weavedown/main/update.sh)
TEXT="
Weavedown Updater
-----------------
This will install files into ~/.local/opt/weavedown/ and will add a file in ~/.local/bin to start the program.

i: install/update
r: remove from system
c: cancel
"
echo "$TEXT"

read -p "Confirm? [I/r/c]: " CONFIRM
if [ -z $CONFIRM ] || [ $CONFIRM == "i" ];
then
	if [ ! -d ~/.local/bin ]; then mkdir -p ~/.local/bin; fi;
	
	if [ ! -d ~/.local/opt/weavedown ]; then
		mkdir -p ~/.local/opt/weavedown;
		git clone https://github.com/KittKat7/weavedown.git ~/.local/opt/weavedown;
	else
		cd ~/.local/opt/weavedown;
		git pull;
	fi;

	if [ ! -f ~/.local/bin/weavedown ]; then printf '#!/bin/bash\npython ~/.local/opt/weavedown/main.py $@' > ~/.local/bin/weavedown; fi;

	chmod +x ~/.local/bin/weavedown

	echo "COMPLETE"
elif [ $CONFIRM == "r" ]
then
	rm -fr ~/.local/opt/weavedown
	unlink ~/.local/bin/weavedown
fi

