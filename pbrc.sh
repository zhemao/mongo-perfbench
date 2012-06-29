if [ -z "$PBRC" ]; then
    export PBRC=1

    MONGO_DIR="$(dirname $0)/.."

    if [ -d $HOME/bin ] && [ -z `echo $PATH | grep $HOME/bin ` ]; then
        export PATH=$HOME/bin:$PATH
    fi

    SERVER_INFO='{hostname: "localhost:27018"}'

    export MONGO_DIR SERVER_INFO
fi
