local create_group = vim.api.nvim_create_augroup
local create_autocmd = vim.api.nvim_create_autocmd

-- highlight on copy
local highlight_group = create_group('YankHighlight', { clear = true })
create_autocmd('TextYankPost', {
  group = highlight_group,
  callback = function() vim.highlight.on_yank() end,
  pattern = '*',
})

-- change cwd when launching a directory
local auto_cd = create_group('AutoCDOnEnter', { clear = true })
create_autocmd('VimEnter', {
  group = auto_cd,
  callback = function()
    local arg = vim.fn.expand('<amatch>')
    if vim.fn.isdirectory(arg) == 1 then
      vim.cmd('cd ' .. arg)
    end
  end,
})

-- indents
vim.opt.tabstop = 4
vim.opt.softtabstop = 4
vim.opt.shiftwidth = 4
vim.opt.expandtab = true
vim.opt.breakindent = true

-- editor
vim.opt.colorcolumn = '80'
vim.opt.cursorline = true
vim.opt.signcolumn = 'yes'
vim.opt.scrolloff = 8

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

-- spelling
vim.opt.spell = true
vim.opt.spelllang = { 'en_us' }

-- code folding
vim.o.foldlevel = 99
vim.o.foldlevelstart = 99
vim.o.foldenable = true
vim.o.fillchars = [[eob: ,fold: ,foldopen:,foldsep: ,foldclose:]]

-- miscellaneous options
vim.opt.guicursor = 'n-v-c:hor25,i-ci:ver25,r-cr:block,n:blinkon250'
vim.opt.mouse = 'a'               -- enable mouse support
vim.opt.clipboard = 'unnamedplus' -- use os clipboard
vim.opt.undofile = true           -- store undo tree between sessions
vim.opt.updatetime = 250          -- decrease update time
vim.opt.termguicolors = true      -- true terminal colors
