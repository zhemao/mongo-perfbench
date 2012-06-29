if [ -d $HOME/bin ] && [ -z `echo $PATH | grep $HOME/bin ` ]; then
    export PATH=$HOME/bin:$PATH
fi

