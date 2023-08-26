-- plugins configuration functions table
local plugin_configs = {}

-- configure a plugin by loading its config function
function ConfigurePlugin(config)
  table.insert(plugin_configs, config)
end

-- load plugins configurations
function LoadPluginConfigs()
  for _, config in ipairs(plugin_configs) do config() end
end

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
