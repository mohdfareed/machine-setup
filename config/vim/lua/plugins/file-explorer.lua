ConfigurePlugin(function()
  NeoTree = require('neo-tree')
  NeoTree.toggle = function() vim.cmd('Neotree toggle float') end

  Harpoon = require('harpoon')
  Harpoon.ui = require('harpoon.ui')
  Harpoon.mark = require('harpoon.mark')
  Harpoon.term = require('harpoon.term')
  Harpoon.tmux = require('harpoon.tmux')
  Harpoon.cmd_ui = require('harpoon.cmd-ui')
  require('telescope').load_extension('harpoon')

  Harpoon.open = function() vim.cmd('Telescope harpoon marks') end
  Harpoon.goto = function(index)
    return function() Harpoon.ui.nav_file(index) end
  end
end)

return {
  { 'ThePrimeagen/harpoon' },

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
