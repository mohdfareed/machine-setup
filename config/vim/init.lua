-- install plugin manager
local lazypath = vim.fn.stdpath 'data' .. '/lazy/lazy.nvim'
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system {
    'git',
    'clone',
    '--filter=blob:none',
    'https://github.com/folke/lazy.nvim.git',
    '--branch=stable',
    lazypath,
  }
end
vim.opt.rtp:prepend(lazypath)

-- set leader to <space>
vim.g.mapleader = ' '
vim.g.maplocalleader = ' '
-- load utilities
require('utils')

-- load plugins
require('lazy').setup('plugins', {
  checker = { enabled = true },  -- check for plugin updates automatically
  install = { colorscheme = { 'onedark' } },  -- startup installation theme
  ui = { border = 'rounded' },
})

-- load personal configuration
require('keymaps')
require('options')
