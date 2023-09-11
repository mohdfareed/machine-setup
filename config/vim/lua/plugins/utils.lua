ConfigurePlugin(function()
  if vim.g.vscode then return end
  Persistence = require('persistence')
  Persistence.load_last = function() Persistence.load({ last = true }) end
end)

return {
  { -- session memory
    'folke/persistence.nvim',
    event = 'BufReadPre',
    opts = {},
    cond = function() return not vim.g.vscode end,
  },
}
