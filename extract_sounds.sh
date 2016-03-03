#!/bin/bash
cd dump
../custmguisplit.py ../soft/CUSTMGUI.DLL
../hubsplit.py ../soft/DEFAULT.HUB
for f in *.pcm ; do ../pcm2wav.py "$f" "${f%.pcm}.wav" ; done
mv *.wav ../wav/
exit
