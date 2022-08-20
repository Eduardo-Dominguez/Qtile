 #!/bin/bash
 nombre="cover"
 cd /home/edu/.mozilla/firefox/firefox-mpris/
 for picture in `ls *.png`
 do
 nuevonombre=$nombre
 mv $picture $nuevonombre.png
 done
