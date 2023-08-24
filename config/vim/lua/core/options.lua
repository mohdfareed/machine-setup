-- indents
vim.opt.tabstop = 4
vim.opt.softtabstop = 4
vim.opt.shiftwidth = 4
vim.opt.expandtab = true
vim.opt.breakindent = true
vim.opt.smartindent = true

-- editor
vim.opt.completeopt = 'menuone,preview'
vim.opt.colorcolumn = '80'
vim.opt.signcolumn = 'yes'
vim.opt.scrolloff = 8
vim.opt.foldmethod = 'syntax'

-- search
vim.opt.hlsearch = false
vim.opt.ignorecase = true
vim.opt.smartcase = true

-- show hidden chars
vim.opt.list = true
vim.opt.listchars:append 'space:⋅'

-- line numbers
vim.opt.number = true
vim.opt.relativenumber = true

-- miscellaneous options
vim.opt.guicursor = 'n-v-c:hor25,i-ci:ver25,r-cr:block,n:blinkon250'
vim.opt.mouse = 'a' -- enable mouse support
vim.opt.clipboard = 'unnamedplus' -- use os clipboard
vim.opt.undofile = true -- store undo tree between sessions
vim.opt.updatetime = 250 -- decrease update time
vim.opt.termguicolors = true -- true terminal colors
