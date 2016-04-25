function! whylog#Whylog_Action()
    if !has('python')
        finish
    endif
    if !has("byte_offset")
        finish
    endif

python << EOF
import whylog_vim
whylog_vim.whylog_action()
EOF
endfunction

function! whylog#Whylog_Teach()
    if !has('python')
        finish
    endif
    if !has("byte_offset")
        finish
    endif

python << EOF
import whylog_vim
whylog_vim.whylog_teach()
EOF
endfunction
