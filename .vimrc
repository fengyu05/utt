"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" set line no on

set wildmenu
" Ignore compiled files
set wildignore=*.o,*~,*.pyc
set ruler
set cmdheight=2
" A buffer becomes hidden when it is abandoned
set hid

" Configure backspace so it acts as it should act
set backspace=eol,start,indent
set whichwrap+=<,>,h,l

" Makes search act like search in modern browsers
set incsearch

" Don't redraw while executing macros (good performance config)
set lazyredraw

" For regular expressions turn magic on
set magic

" Show matching brackets when text indicator is over them
set showmatch
" How many tenths of a second to blink when matching brackets
set mat=2

" No annoying sound on errors
set noerrorbells
set novisualbell
set t_vb=
set tm=500

set lbr
set ai "Auto indent
set si "Smart indent
set wrap "Wrap lines

" => Status line
" Always show the status line
set laststatus=2
set statusline=\ %{HasPaste()}%F%m%r%h\ %w\ \ CWD:\ %r%{getcwd()}%h\ \ \ Line:\ %l
set listchars=tab:--,trail:!,extends:>,precedes:<

" buff explorer
let mapleader = "\\"
let g:mapleader = "\\"

let g:miniBufExplModSelTarget = 1
let g:miniBufExplorerMoreThanOne = 0
let g:miniBufExplModSelTarget = 0
let g:miniBufExplUseSingleClick = 1
let g:miniBufExplMapWindowNavVim = 1
let g:miniBufExplVSplit = 25
let g:miniBufExplSplitBelow=1

" Java Importer
let g:JavaImpPaths = $HOME."/javasource"
let g:JavaImpDataDir = $HOME."/javaimp_cache"
let g:JavaImpDataDir = $HOME."/javaimp_cache"
let g:JavaImpDocPaths= $HOME."/javadoc"
let g:JavaImpDocViewer = "lynx"
" Import class
nmap <leader>ji :JI<CR>
" Sort class import
nmap <leader>js :JIS<CR>
" View file
nmap <leader>jf :JIF<CR>
" Java Doc
nmap <leader>jD :JID<CR>


" window and buff navigation
nmap <Tab> :bn<cr>
nmap <S-Tab> :bn<cr>

nmap <C-up> :bp<cr>
nmap <C-down> :bn<cr>

map <C-j> <C-W>j
map <C-k> <C-W>k
map <C-h> <C-W>h
map <C-l> <C-W>l

" function key
nmap <F2> :source ~/.vimrc<cr>
nmap <F3> :e ~/.vimrc<cr>
nmap <F4> :bd<cr>
nmap <F5> :Tlist<cr>
nmap <F6> :MRU<cr>
nmap <F7> :set number! number?<cr>
nmap <F8> :set nopaste! nopaste?<cr>
nmap <F9> :call FindUniqueWords()<cr>

nmap <leader><F12> :qa!<cr>
nmap <leader><F11> :call PlainMode()<cr>
nmap <leader><F10> :call PlainMode()<cr>
nmap <c-`> <esc>

" function key alt
imap <F1> <esc><F1>
imap <F2> <esc><F2>
imap <F3> <esc><F3>
imap <F4> <esc><F4>
imap <F5> <esc><F5>
imap <F6> <esc><F6>
imap <F7> <esc><F7>
imap <F8> <esc><F8>
imap <F9> <esc><F9>

" undo and redo <C-u> <C-r>
nmap <C-u> :undo<cr>
nmap u <esc>

" highlight kework
nmap # #*

" scorlling
nmap <C-D> 25j
nmap <C-F> 25k
" Set 7 lines to the cursor - when moving vertically using j/k
set so=7

" word correct
iab pirnt print

" FileType shortcut
au FileType java call MyJavaConfig()
function! MyJavaConfig()
iab println System.out.println
iab FlagSpec @FlagSpec(altName = "", help = "")<cr>public static final Flag<
iab Loggers private static final FormattingLogger logger =<cr>Loggers.getContextFormattingLogger();
endfunction

au FileType python call MyPythonConfig()
function! MyPythonConfig()
iab __name__ __name__ == '__main__':<cr>main()
endfunction

"set shell=bash\ -l don't work
"set shellcmdflag=-ic work

" function
" Returns true if paste mode is enabled
function! HasPaste()
if &paste
return 'PASTE MODE '
en
return ''
endfunction

function! GoogleNit()
execute '!nit.py %'
endfunction

function! UniqworkCheck()
execute '!uniqword_checker.py -l 8 %'
endfunction"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" set line no on

set wildmenu
" Ignore compiled files
set wildignore=*.o,*~,*.pyc
set ruler
set cmdheight=2
" A buffer becomes hidden when it is abandoned
set hid

" Configure backspace so it acts as it should act
set backspace=eol,start,indent
set whichwrap+=<,>,h,l

" Makes search act like search in modern browsers
set incsearch

" Don't redraw while executing macros (good performance config)
set lazyredraw

" For regular expressions turn magic on
set magic

" Show matching brackets when text indicator is over them
set showmatch
" How many tenths of a second to blink when matching brackets
set mat=2

" No annoying sound on errors
set noerrorbells
set novisualbell
set t_vb=
set tm=500

syntax enable
set nobackup
set nowb
set noswapfile
set smarttab
set expandtab " Force this, although it's in google.vim
set shiftwidth=2 " Force this, although it's in google.vim
set softtabstop=2 " Make tabs act like spaces for editing ops
set wildmode=longest,list,full " Completion modes for wildcard expansion
set hlsearch " Highlight previous search results
set showmode " Show the mode you're currently in
set showmatch " Show matching braces / brackets
set incsearch " Do incremental searching
set number " Set line numbers
set title " Let vim change my tab/window title
set autoread
setlocal textwidth=500
colorscheme elflord
match Label /\s\u\w\+\s/

set lbr
set ai "Auto indent
set si "Smart indent
set wrap "Wrap lines

" => Status line
" Always show the status line
set laststatus=2
set statusline=\ %{HasPaste()}%F%m%r%h\ %w\ \ CWD:\ %r%{getcwd()}%h\ \ \ Line:\ %l

" buff explorer
let mapleader = "\\"
let g:mapleader = "\\"

let g:miniBufExplModSelTarget = 1
let g:miniBufExplorerMoreThanOne = 0
let g:miniBufExplModSelTarget = 0
let g:miniBufExplUseSingleClick = 1
let g:miniBufExplMapWindowNavVim = 1
let g:miniBufExplVSplit = 25
let g:miniBufExplSplitBelow=1

" buff ctrl
nmap <leader>a :e  
nmap <leader>e :e  
nmap <leader>z :ls<cr>



" window and buff navigation
nmap <Tab> :bn<cr>
nmap <S-Tab> :bn<cr>

nmap <C-up> :bp<cr>
nmap <C-down> :bn<cr>

map <C-j> <C-W>j
map <C-k> <C-W>k
map <C-h> <C-W>h
map <C-l> <C-W>l

" function key
nmap <F2> :source ~/.vimrc<cr>
nmap <F3> :e ~/.vimrc<cr>
nmap <F4> :bd<cr>
nmap <F6> :MRU<cr>
nmap <F7> :set number! number?<cr>
nmap <F8> :set nopaste! nopaste?<cr>

nmap <leader><F12> :qa!<cr>
nmap <leader><F9> :call PlainMode()<cr>
nmap <c-`> <esc>

" function key alt
imap <F1> <esc><F1>
imap <F2> <esc><F2>
imap <F3> <esc><F3>
imap <F4> <esc><F4>
imap <F5> <esc><F5>
imap <F6> <esc><F6>
imap <F7> <esc><F7>
imap <F8> <esc><F8>
imap <F9> <esc><F9>

" undo and redo <C-u> <C-r>
nmap <C-u> :undo<cr>
nmap u <esc>

" highlight kework
nmap # #*

" scorlling
nmap <C-D> 25j
nmap <C-F> 25k
" Set 7 lines to the cursor - when moving vertically using j/k
set so=7

" word correct
iab pirnt print

" FileType shortcut
au FileType java call MyJavaConfig()
function! MyJavaConfig()
iab println System.out.println
iab FlagSpec @FlagSpec(altName = "", help = "")<cr>public static final Flag<
iab Loggers private static final FormattingLogger logger =<cr>Loggers.getContextFormattingLogger();
endfunction

" Read .class using javap decompiler
function! s:ReadClass(dir, classname)
  execute "cd " . a:dir
  execute "0read !javap -c " . a:classname
  1
  setlocal readonly
  setlocal nomodified
endfunction
autocmd BufReadCmd *.class call <SID>ReadClass(expand("<afile>:p:h"), expand("<afile>:t:r"))
" End Read .class

augroup filetypedetect
  au BufNewFile,BufRead *.pig set filetype=pig syntax=pig
augroup END
"set shell=bash\ -l don't work
"set shellcmdflag=-ic work

" Function begin here, Function mush start with capital letter.
function! HasPaste()
if &paste
return 'PASTE MODE '
en
return ''
endfunction

function! GoogleNit()
execute '!nit.py %'
endfunction

function! FindUniqueWords()
  let stat = {}
  for ii in range(1, line('$'))
    for word in split(getline(ii), '\(\k\@!.\)\+')
      let stat[word] = get(stat, word, 0) + 1
    endfor
  endfor
  let uq_worbs = filter(copy(stat), 'v:val == 1')
  for word in keys(uq_worbs)
  endfor
  echo sort(keys(uq_worbs))
endfunction

function! PlainMode()
set nonu
only
endfunction

function! FindAllTag()
  echo 'FindAllTag'
  echo expand("<cword>")
  ta /expand("<cword>")
endfunction
