ConfigurePlugin(function()
  Flash = require('flash')
  Telescope = require('telescope')
  Telescope.builtin = require('telescope.builtin')
  Trouble = require('trouble')
  UFO = require('ufo')
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
      require('ufo').setup({ -- default to syntax based
        provider_selector = function() return { 'treesitter', 'indent' } end
      })
    end
  }
}
