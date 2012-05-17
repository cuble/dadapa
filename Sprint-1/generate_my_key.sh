if [ -d "$HOME/.ssh" ]; then
  if [ -d "$HOME/.ssh/key_backup" ]
    echo "The script already run, please check the key in ~/.ssh"
    exit 0
  fi
  if [ -f "id_rsa" ]; then
    echo "Backup the exist RSA key pair" 
    mkdir key_backup
    cp id_rsa* key_backup
    rm id_rsa*
  fi
else
  echo "create the .ssh directory"
  mkdir ~/.ssh
fi

echo "Generating RSA key pair for fouryu@sina.com.cn"
# key file is ~/.ssh/id_rsa and ~/.ssh/id_rsa.pub; -N provide passphrase, -C provide the comments.
ssh-keygen -q -t rsa -f $HOME/.ssh/id_rsa -N myGit8109 -C "fouryu@sina.com.cn"
