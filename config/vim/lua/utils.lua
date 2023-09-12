-- plugins configuration functions table
local plugin_configs = {}

--- configure a plugin by loading its config function
function ConfigurePlugin(config, vscode)
  vscode = vscode or false -- whether to load the function in vscode
  if not vim.g.vscode or vscode then
    table.insert(plugin_configs, config)
  end
end

-- load plugins configurations
function LoadPluginConfigs()
  for _, config in ipairs(plugin_configs) do config() end
end

-- create a keymap group
function RegisterGroup(bind, name)
  if not vim.g.vscode then
    local ok, whichkey = pcall(require, 'which-key')
    if ok then whichkey.register({ [bind] = { name = "+" .. name } }) end
  end
end

-- map a keybind
function MapKey(mode, l, r, desc, opts)
  opts = opts or {}
  opts.desc = desc
  vim.keymap.set(mode, l, r, opts)
end
