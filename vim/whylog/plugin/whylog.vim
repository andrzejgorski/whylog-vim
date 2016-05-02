function! whylog#Whylog_Action()
    if !has('python') | !has('byte_offset')
        finish
    endif
python << EOF
import whylog_vim
whylog_vim.whylog_action()
EOF
endfunction

function! whylog#Whylog_Teach()
    if !has('python') | !has('byte_offset')
        finish
    endif
python << EOF
import whylog_vim
whylog_vim.whylog_teach()
EOF
endfunction
