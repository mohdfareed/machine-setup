ConfigurePlugin(function()
  Persistence = require('persistence')
  Persistence.load_last = function() Persistence.load({ last = true }) end
end)

return {
  { -- session memory
    'folke/persistence.nvim',
    event = 'BufReadPre',
    opts = {}
  },
}
