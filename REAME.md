# How to set up 
I'm not gonna lie I cried a little when doing this
1. ssh zxxxx@d.cse.unsw.edu.au
2. cd /localstorage/zId
3. copy the env file and replace "JAS" with your zId https://cgi.cse.unsw.edu.au/~cs3311/21T3/pracs/env
4. source ./env (to execute the commands)
5. next step is to run "initdb" but I got this error AKA what made me cry: initdb.bin: invalid locale settings; check LANG and LC_* environment variables 
6. to solve run this in your machine's terminal: export LC_ALL="en_AU.UTF-8"  LC_CTYPE="en_AU.UTF-8"


# How to set up alias for remote address
1. vi ~/.ssh/config
2. add the detail
e.g:\
Host ${name}\
    HostName e.g: 192.168.225.22\
    User e.g: sk

# Changes to ~/.bashrc files to make life easier
1. checks if the file exist and then runs the command\
 [[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$home/.rvm/scripts/rvm"
2. add alias for command\
alias ${name}="command" 
3. this one has a comment with useful stuff to have in .bashrc\
https://unix.stackexchange.com/questions/129143/what-is-the-purpose-of-bashrc-and-how-does-it-work

