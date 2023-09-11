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

local lazy_config = {                         -- plugin manager config
  checker = { enabled = true },               -- check for updates on startup
  install = { colorscheme = { 'onedark' } },  -- startup installation theme
  ui = { border = 'rounded' },                -- use rounded borders
}

require('utils')                              -- load utilities
require('lazy').setup('plugins', lazy_config) -- load plugins
LoadPluginConfigs()                           -- load plugins configurations
require('keymaps')                            -- load personal keymaps
require('options')                            -- load personal config options
