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
PluginsMappers = {} -- plugins mapping functions table
function LoadPluginsKeyMaps() -- load plugins keymaps
  for _, mapper in ipairs(PluginsMappers) do mapper() end
end
