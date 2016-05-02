# Before instalating you need to have installed some programs:
#
### 1 vim-pathogen ###
# https://github.com/tpope/vim-pathogen
#
# installation:
# mkdir -p ~/.vim/autoload ~/.vim/bundle && \
#    curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim
#
#
### 2 vim-python-jedi ###
# build python in vim
#
# installation:
# sudo apt-get install vim-python-jedi
#
#
### 3 whylog ###
# https://github.com/9livesdata/whylog.git
#
# installation:
# git clone https://github.com/9livesdata/whylog.git
# cd whylog
# sudo python setup.py install
#
#
# Add to your .vimrc file these two lines:
#
# map <f3> :call whylog#Whylog_Action()<CR>
# map <f4> :call whylog#Whylog_Teach()<CR>


mkdir -p ~/.vim/bundle/whylog
cp -r vim/whylog/* ~/.vim/bundle/whylog


# sudo python setup.py install
# if doesn't work try:
# sudo python setup.py install
