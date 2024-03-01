#!/bin/bash

echo "Converting script shebang entries from ksh to bash"
type ksh >/dev/null 2>&1 ||  sed -i 's/ksh/bash/g' set_rad_env
type ksh >/dev/null 2>&1 ||  sed -i 's/ksh/bash/g' sbin/*

