ConfigurePlugin(function()
  Flash = require('flash')
  Telescope = require('telescope')
  Telescope.builtin = require('telescope.builtin')
  Trouble = require('trouble')

  Telescope.setup {
    defaults = {
      mappings = {
        i = { ['<c-t>'] = Trouble.open_with_trouble },
        n = { ['<c-t>'] = Trouble.open_with_trouble },
      },
    },
  }
end)

return {
  { 'tpope/vim-sleuth' },                 -- auto-detect indents
  { 'numToStr/Comment.nvim', opts = {} }, -- comment code
  ----------------------------------------------------------------------------

  { -- indentation guides
    'lukas-reineke/indent-blankline.nvim',
    opts = {
      show_current_context = true,
      space_char_blankline = ' ',
    },
  },

  { -- auto-complete pairs
    'windwp/nvim-autopairs',
    event = "InsertEnter",
    opts = {}
  },

  { -- add/delete/replace pairs
    "kylechui/nvim-surround",
    version = "*",
    event = "VeryLazy",
    opts = {}
  },

  { -- todo comments manager
    'folke/todo-comments.nvim',
    dependencies = { 'nvim-lua/plenary.nvim' },
    opts = { highlight = { keyword = 'fg' }, }
  },

  { -- search utilities
    'folke/flash.nvim',
    event = 'VeryLazy',
  },

  { -- fuzzy finder
    'nvim-telescope/telescope.nvim',
    branch = '0.1.x',
    dependencies = { 'nvim-lua/plenary.nvim' },
  },

  { -- list view
    'folke/trouble.nvim',
    dependencies = { "nvim-tree/nvim-web-devicons" },
    opts = {},
  },

  { -- code folding
    'kevinhwang91/nvim-ufo',
    dependencies = { 'kevinhwang91/promise-async' },
    config = function()
      vim.keymap.set('n', 'zR', require('ufo').openAllFolds)
      vim.keymap.set('n', 'zM', require('ufo').closeAllFolds)
      vim.keymap.set('n', 'zr', require('ufo').openFoldsExceptKinds)
      vim.keymap.set('n', 'zm', require('ufo').closeFoldsWith)
      vim.keymap.set('n', 'K', function()
        local winid = require('ufo').peekFoldedLinesUnderCursor()
        if not winid then vim.lsp.buf.hover() end
      end)
      require('ufo').setup({ -- default to syntax based
        provider_selector = function() return { 'treesitter', 'indent' } end
      })
    end
  }
}

--[[
  -- some really long comment
  V-- I want to fold ot
      print(10)         -- no action (comment)
  test``
  that spands multiple lines
--]]
