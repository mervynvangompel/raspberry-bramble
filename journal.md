Set up the git repo, created architecture, execution plan and readme documents. Also added a repo structure and branchnaming to keep things nice and tidy for myself (or see what issues I run into).
Next, to work!
Flashed the SD cards. 
Ran into two issues:
- one is that the settings you can add when flashing the sd with the raspberry imager don't seem to be applied (ssh and username). This can be done manually however by adding files to the SD, which I further automated as well with a script.
- Next, found out that PIs don't seem to use dhcpcd so had to find another way to set the static IP, i.e. through nmcli.
Added a troubleshooting document to keep track of the issues I run into, you never know there might be more of those...
