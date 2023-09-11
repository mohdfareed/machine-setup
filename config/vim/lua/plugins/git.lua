ConfigurePlugin(function()
  Lazygit = function() vim.cmd('LazyGit') end
  Git = require('gitsigns')
end)

return {
  { -- git client
    'kdheepak/lazygit.nvim',
    dependencies = {
      "nvim-lua/plenary.nvim",
    },
    cond = function() return not vim.g.vscode end,
  },

  { -- git editor utilities
    'lewis6991/gitsigns.nvim',
    opts = {
      preview_config = { border = 'rounded' },
    },
    cond = function() return not vim.g.vscode end,
  },
}
