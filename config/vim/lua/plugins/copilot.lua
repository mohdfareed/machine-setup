local copilot = function()
  -- setup auto-completion
  local cmp = require('cmp')
  local cmp_config = cmp.get_config()
  table.insert(cmp_config.sources, { name = 'copilot' })
  cmp.setup(cmp_config)

  -- setup statusline indicator
  local lualine = require('lualine')
  local lualine_config = lualine.get_config()
  local stat = function() return require("copilot_status").status_string() end
  table.insert(lualine_config.sections.lualine_c, stat)
  lualine.setup(lualine_config)
end
ConfigurePlugin(copilot)

return {
  { -- copilot
    'zbirenbaum/copilot.lua',
    event = 'InsertEnter',
    build = ':Copilot auth',
    opts = {
      suggestion = { enabled = false },
      panel = { enabled = false },
      filetypes = { ['*'] = true },
    },
  },

  -- statusline integration
  { "jonahgoldwastaken/copilot-status.nvim", event = "BufReadPost", },
  -- completion integration
  { 'zbirenbaum/copilot-cmp',                opts = {} },
}
