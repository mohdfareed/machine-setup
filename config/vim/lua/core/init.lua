function RegisterGroup(bind, name)
  require('which-key').register({ [bind] = { name = "+" .. name }})
end

function MapKey(mode, l, r, desc, opts)
  opts = opts or {}
  opts.desc = desc
  vim.keymap.set(mode, l, r, opts)
end

-- set leader to <space>
vim.g.mapleader = ' '
vim.g.maplocalleader = ' '
-- plugins key mapping functions
PluginsMappers = {}

-- load plugins
require('lazy').setup('plugins', {
  checker = { enabled = true },  -- check for plugin updates automatically
  install = { colorscheme = { 'onedark' } },  -- startup installation theme
})

-- load configuration
require('core.keymaps')
require('core.options')
require('core.autocmds')
