# Sets some common values used by different scripts

if [ -z "$PBRC" ]; then
    export PBRC=1

    MONGO_DIR="$(dirname $0)/.."

    if [ -d $HOME/bin ] && [ -z `echo $PATH | grep $HOME/bin ` ]; then
        PATH=$HOME/bin:$PATH
    fi

    [ -z $MAXTHREADS ] && MAXTHREADS=24

    export MONGO_DIR PATH MAXTHREADS
fi
