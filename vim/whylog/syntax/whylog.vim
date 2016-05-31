"
" Vim syntax file
" Language:      Whylog output window
" Maintainer:    Andrzej Górski <andrzejgorski@supermond.com>
" Last Change:   2016 May 4
"

if exists('b:current_syntax')
  finish
endif
let b:current_syntax = 'whylog'

syn keyword todo contained TODO FIXME

syn match comment '#.*$' contains=todo,headers,prefixes,params,button

syn match headers '^---\( \w\+\)\{1,}:\?'
syn match headers '^===\( \w\+\)\{1,}:\?'

syn keyword converters to_date
syn keyword converters string
syn keyword converters int
syn keyword converters float

syn match warnings '!!.*!!'
syn match warnings 'undefined'

syn match prefixes 'file:'
syn match prefixes 'offset:'
syn match prefixes 'log type:'
syn match prefixes 'parser:'
syn match prefixes 'params'
syn match prefixes 'line:'
syn match prefixes 'group:'
syn match prefixes 'host pattern:'
syn match prefixes 'path pattern:'
syn match prefixes 'super parser regex:'
syn match prefixes 'file name matcher:'
syn match prefixes 'primary key groups:'
syn match prefixes 'group_converter \d\+:'
syn match prefixes 'group \d\+:'
syn match prefixes 'match:'

syn match button '\[[^[^[]*\]'

syn region descBlock start='===' end='<<<' fold transparent contains=headers,prefixes,params,button,todo


hi def link todo            Todo
hi def link comment         Comment
hi def link headers         Statement
hi def link converters      Statement
hi def link warnings        Constant
hi def link prefixes        Type
hi def link button          Todo
