# After instalating you need to have installed vim pathogen.
#
# To install check: https://github.com/tpope/vim-pathogen
#

mkdir -p ~/.vim/bundle/whylog
cp -r vim/whylog/* ~/.vim/bundle/whylog

python setup.py install
