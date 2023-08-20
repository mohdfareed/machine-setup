-- Options are automatically loaded before lazy.nvim startup
-- Default options that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/options.lua

vim.opt.wrap = true -- enable line wrap
vim.opt.colorcolumn = "80" -- line length marker at 80 columns
vim.opt.foldmethod = "syntax" -- enable code folding

-- default to 4 spaces for tabs
vim.opt.shiftwidth = 4
vim.opt.tabstop = 4

-- set cursor shape
vim.opt.guicursor = "n-v-c:hor25,i-ci:ver25,r-cr:block,n:blinkon250"
