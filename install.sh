# Before instalating you need to have installed vim pathogen.
#
# To install check: https://github.com/tpope/vim-pathogen
#
# Add to your .vimrc file these two lines:
#
# map <f3> :call whylog#Whylog_Action()<CR>
# map <f4> :call whylog#Whylog_Teach()<CR>
#

mkdir -p ~/.vim/bundle/whylog
cp -r vim/whylog/* ~/.vim/bundle/whylog

python setup.py install
