"
" Vim syntax file
" Language:      Whylog output window
" Maintainer:    Andrzej Górski <andrzejgorski@supermond.com>
" Last Change:   2016 Apr 09
"

if exists('b:current_syntax')
  finish
endif
syn keyword todo contained TODO FIXME
syn match comment '#.*$' contains=todo

let b:current_syntax = 'whylog'
syn match headers '^---\( \w\+\)\{1,}:\?'
syn match headers '^===\( \w\+\)\{1,}:\?'
syn region descBlock start='===' end='<<<' fold transparent contains=headers,prefixes,params,button,todo
syn match params '!!.*!!'

syn keyword headers date
syn keyword headers string
syn keyword headers int
syn match prefixes 'file:'
syn match prefixes 'offset:'
syn match prefixes 'log type:'
syn match prefixes 'parser:'
syn match prefixes 'group:'
syn match prefixes 'host pattern:'
syn match prefixes 'path pattern:'
syn match prefixes 'file name matcher:'
syn match prefixes 'primary key groups:'
syn match prefixes 'group_converter \d\+:'
syn match prefixes 'group \d\+:'
syn match prefixes 'match:'
syn match button '\[[^[^[]*\]'


hi def link todo            Todo
hi def link comment         Comment
hi def link headers         Statement
hi def link headers2        Statement
hi def link prefixes        Type
hi def link params          Constant
hi def link button          Todo
