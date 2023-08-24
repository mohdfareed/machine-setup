-- create a keymap group
function RegisterGroup(bind, name)
  require('which-key').register({ [bind] = { name = "+" .. name } })
end

-- map a keybind
function MapKey(mode, l, r, desc, opts)
  opts = opts or {}
  opts.desc = desc
  vim.keymap.set(mode, l, r, opts)
end

-- plugins load keymaps by loading mapping functions
PluginConfigs= {} -- plugins mapping functions table
function LoadPluginConfigs() -- load plugins keymaps
  for _, config in ipairs(PluginConfigs) do config() end
end
