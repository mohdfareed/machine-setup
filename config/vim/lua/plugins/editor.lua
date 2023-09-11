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
    },
    cond = function() return not vim.g.vscode end,
  },

  { -- one dark theme
    'navarasu/onedark.nvim',
    lazy = false,
    priority = 1000,
    config = function()
      require('onedark').setup({
        transparent = true,
        lualine = { transparent = true },
        highlights = {
          NormalFloat = { bg = 'none' },
          FloatBorder = { bg = 'none' },
        }
      })
      require('onedark').load()
    end,
    cond = function() return not vim.g.vscode end,
  },

  { -- statusline
    'nvim-lualine/lualine.nvim',
    opts = {
      options = {
        theme = 'onedark',
        component_separators = '|',
        section_separators = { left = '', right = '' },
        globalstatus = true,
      },
      sections = {
        lualine_c = { 'filetype' },
        lualine_x = { 'buffers', },
        lualine_y = { 'tabs', },
        lualine_z = { 'location', 'searchcount', 'selectioncount', },
      },
      extensions = {
        'quickfix',
        'lazy',
        'neo-tree',
        'nvim-dap-ui',
        'trouble',
        'toggleterm',
        'symbols-outline',
      },
    },
    cond = function() return not vim.g.vscode end,
  },

  {
    'folke/noice.nvim',
    event = 'VeryLazy',
    dependencies = { 'MunifTanjim/nui.nvim' },
    opts = {
      lsp = {
        override = {
          ['vim.lsp.util.convert_input_to_markdown_lines'] = true,
          ['vim.lsp.util.stylize_markdown'] = true,
          ['cmp.entry.get_documentation'] = true,
        },
      },
      presets = {
        bottom_search = true,
        command_palette = true,
        long_message_to_split = true,
        lsp_doc_border = true
      },
    },
    cond = function() return not vim.g.vscode end,
  }
}
