# Prerequisites
- Python 3.8
- a virtual environment is recommended


# Installation
First, configure your shell by setting `PUDDL_HOME` and using Puddl's
completion:
```
mkdir -p ~/.bash/
cat <<'EOF' >> ~/.bash/puddl
# Namespaces are one honking great idea -- let's do more of those!
export PUDDL_HOME=~/puddl

hash puddl 2>/dev/null && eval "$(_PUDDL_COMPLETE=source puddl)"
EOF

cat <<'EOF' >> ~/.bashrc
[[ -f ~/.bash/puddl ]] && source ~/.bash/puddl
EOF

exec $SHELL
```

Next, install puddl [^pypi-not-yet]:
```
mkdir -p ${PUDDL_HOME}
git clone https://gitlab.com/puddl/puddl.git ${PUDDL_HOME}/puddl
cd ${PUDDL_HOME}/puddl
pip install --editable .
```

[^pypi-not-yet]: We'll have installer later. ;)

Initialize environment and database:
```
cd $PUDDL_HOME/puddl/
./env/dev/generate_env_file.sh > .env
./env/dev/create_database.sh
source sourceme
./env/dev/init-config-from-env.py
./manage.py migrate
```

Try it:
```
puddl ingress file README.md
```


# Development
Run flake8 before committing
```
ln -s $(readlink -m env/dev/git-hooks/pre-commit.sample) .git/hooks/pre-commit
```

Basic development workflow:
```
# hack, hack
make
```

Got `psql` installed?
```
source sourceme
echo "select 'OK' as status" | psql
```


# Developing a new Ingress
See `puddl/ingress/file/` for reference.
