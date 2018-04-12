#!/bin/bash

__user_password() {
SSH_USERPASS=`pwgen -c -n -1 8`
echo user:$SSH_USERPASS | chpasswd
echo ssh user password: $SSH_USERPASS
}

__run_supervisor() {
echo "Running the run_supervisor function."
supervisord -n
}

# Call all functions
__user_password
__run_supervisor
