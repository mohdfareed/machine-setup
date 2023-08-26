ConfigurePlugin(function()
  NeoTree = require('neo-tree')
  NeoTree.toggle = function() vim.cmd('Neotree toggle float') end
end)

return {
  {
    'nvim-neo-tree/neo-tree.nvim',
    branch = 'v3.x',
    dependencies = {
      'nvim-lua/plenary.nvim',
      'nvim-tree/nvim-web-devicons',
      'MunifTanjim/nui.nvim',
    },
    opts = {
      close_if_last_window = true,
      popup_border_style = "rounded",
      buffers = {
        follow_current_file = { enabled = true },
      },
      filesystem = {
        follow_current_file = { enabled = true },
      },
      sources = { 'filesystem', 'buffers', 'git_status', 'document_symbols' },
    }
  }
}
