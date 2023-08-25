local whichkey = function()
  local show_keymap = function() vim.cmd('WhichKey') end
  MapKey({ 'n', 'v' }, '<leader>?', show_keymap, "Show base keybinds")
end

local session_memory = function()
  local persistence = require('persistence')
  local load_last = function() persistence.load({ last = true }) end
  MapKey('n', '<leader>qs', persistence.load, "Load session")
  MapKey('n', '<leader>ql', load_last, "Load last session")
  MapKey('n', '<leader>qd', persistence.stop, "Delete session")
end

table.insert(PluginConfigs, session_memory)
table.insert(PluginConfigs, whichkey)

return {
  { -- keybinds window
    'folke/which-key.nvim',
    event = 'VeryLazy',
    init = function()
      vim.o.timeout = true
      vim.o.timeoutlen = 300
    end,
    opts = {
      window = { border = 'rounded' },
    }
  },

  { -- one dark theme
    'navarasu/onedark.nvim',
    lazy = false,
    priority = 1000,
    config = function()
      require('onedark').setup({
        transparent = true,
        lualine = { transparent = true },
        colors = { bg1 = "none", },
      }) 
      require('onedark').load()
    end,
  },

  { -- indentation guides
    'lukas-reineke/indent-blankline.nvim',
    opts = {
      show_current_context = true,
      space_char_blankline = ' ',
    },
  },

  { -- statusline
    'nvim-lualine/lualine.nvim',
    opts = {
      options = {
        theme = 'onedark',
        component_separators = '|',
        section_separators = { left = '', right = ''},
        globalstatus = true,
      },
      sections = {
        lualine_c = { 'filetype', },
        lualine_x = { 'buffers', },
        lualine_y = { 'tabs', },
        lualine_z = { 'location', 'searchcount', 'selectioncount', },
      },
    },
  },

  { -- session memory
    'folke/persistence.nvim',
    event = 'BufReadPre',
    opts = {}
  },
}
