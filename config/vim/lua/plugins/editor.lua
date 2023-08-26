local whichkey = function()
  local show_keymap = function() vim.cmd('WhichKey') end
  MapKey({ 'n', 'v' }, '<leader>?', show_keymap, "Show base keybinds")
end
ConfigurePlugin(whichkey)

local session_memory = function()
  local persistence = require('persistence')
  local load_last = function() persistence.load({ last = true }) end
  MapKey('n', '<leader>qs', persistence.load, "Load session")
  MapKey('n', '<leader>ql', load_last, "Load last session")
  MapKey('n', '<leader>qd', persistence.stop, "Delete session")
end
ConfigurePlugin(session_memory)

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
  { -- session memory
    'folke/persistence.nvim',
    event = 'BufReadPre',
    opts = {}
  },
  { -- indentation guides
    'lukas-reineke/indent-blankline.nvim',
    opts = {
      show_current_context = true,
      space_char_blankline = ' ',
    },
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
        bottom_search = true, -- use a classic bottom cmdline for search
        command_palette = true, -- position the cmdline and popupmenu together
        long_message_to_split = true,
        lsp_doc_border = true
      },
    },
  }
}
