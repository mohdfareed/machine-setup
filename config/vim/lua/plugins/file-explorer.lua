local neotree = function()
  local open = function() vim.cmd('Neotree') end
  local open_here = function() vim.cmd('Neotree position=current') end

  MapKey('n', '<leader>e', open, "File explorer")
  MapKey('n', '<leader>E', open_here, "File explorer (current window)")
end
table.insert(PluginConfigs, neotree)

return {
  {
    'nvim-neo-tree/neo-tree.nvim',
    branch = 'v3.x',
    dependencies = {
      'nvim-lua/plenary.nvim',
      'nvim-tree/nvim-web-devicons',
      'MunifTanjim/nui.nvim',
      {
        's1n7ax/nvim-window-picker',
        name = 'window-picker',
        event = 'VeryLazy',
        version = '2.*',
        config = function()
          require('window-picker').setup()
        end,
      }
    },
    opts = {
      close_if_last_window = true,
      popup_border_style = "rounded",
      buffers = {
        follow_current_file = { enabled = true },
      },
      filesystem = {
        follow_current_file = { enabled = true },
        bind_to_cwd = true,
      },
    }
  }
}
