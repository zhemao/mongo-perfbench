# Sets some common values used by different scripts

if [ -z "$PBRC" ]; then
    export PBRC=1

    MONGO_DIR="$(dirname $0)/.."

    if [ -d $HOME/bin ] && [ -z `echo $PATH | grep $HOME/bin ` ]; then
        export PATH=$HOME/bin:$PATH
    fi

    export MONGO_DIR 
fi
