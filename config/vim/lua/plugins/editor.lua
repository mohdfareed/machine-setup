return {
  { -- keybinds window
    'folke/which-key.nvim',
    event = 'VeryLazy',
    init = function()
      vim.o.timeout = true
      vim.o.timeoutlen = 300
    end,
    opts = {}
  },

  { -- one dark theme
    'navarasu/onedark.nvim',
    lazy = false,
    priority = 1000,
    config = function()
      require('onedark').setup({
        ending_tildes = true,
        transparent = true,
        lualine = {
          transparent = true,
        },
      }) 
      require('onedark').load()
    end,
  },

  { -- indentation guides
    'lukas-reineke/indent-blankline.nvim',
    opts = {
      show_end_of_line = true,
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
      },
      sections = {
        lualine_c = {},
        lualine_x = { 'filetype', },
        lualine_y = { 'buffers', 'tabs', },
        lualine_z = { 'location', 'searchcount', 'selectioncount', },
      },
    },
  },
}
