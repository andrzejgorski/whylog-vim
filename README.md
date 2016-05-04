### Before instalating you need to have installed some programs:

#### 1. vim-pathogen
https://github.com/tpope/vim-pathogen

##### installation:
```sh
mkdir -p ~/.vim/autoload ~/.vim/bundle && \
curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim
```


#### 2. vim-python-jedi
build python in vim

##### installation:
```sh
(sudo) apt-get install vim-python-jedi
```


#### 3. whylog
https://github.com/9livesdata/whylog.git

##### installation:
```sh
git clone https://github.com/9livesdata/whylog.git
cd whylog
(sudo) python setup.py install
```


Add to your .vimrc file these two lines:

```vim
map <f3> :call whylog#Whylog_Action()<CR>
map <f4> :call whylog#Whylog_Teach()<CR>
```


### Installation: (same as install.sh)
```sh
git clone https://github.com/9livesdata/whylog-vim.git
cd whylog-vim
mkdir -p ~/.vim/bundle/whylog
cp -r vim/whylog/* ~/.vim/bundle/whylog
```
##### python whylog\_vim:

```sh
cd whylog_vim
(sudo) python setup.py install
```
sudo parametr is optional
