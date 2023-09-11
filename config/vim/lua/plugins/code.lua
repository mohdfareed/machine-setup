ConfigurePlugin(function()
  Flash = require('flash')
end, true)

ConfigurePlugin(function()
  Telescope = require('telescope')
  Telescope.builtin = require('telescope.builtin')
  Telescope.builtin.fuzzy_buffer = Telescope.builtin.current_buffer_fuzzy_find
  Trouble = require('trouble')
  UFO = require('ufo')

  WorkspaceDiagnostics = function() Trouble.open("workspace_diagnostics") end
  DocumentDiagnostics = function() Trouble.open("document_diagnostics") end
end)

return {
  { -- auto-detect indents
    'tpope/vim-sleuth',
    -- cond = function() return not vim.g.vscode end,
  },

  { -- comment code
    'numToStr/Comment.nvim', opts = {},
    -- cond = function() return not vim.g.vscode end,
  },

  { -- indentation guides
    'lukas-reineke/indent-blankline.nvim',
    opts = {
      show_current_context = true,
      space_char_blankline = ' ',
    },
    cond = function() return not vim.g.vscode end,
  },

  { -- auto-complete pairs
    'windwp/nvim-autopairs',
    event = "InsertEnter",
    opts = {},
    cond = function() return not vim.g.vscode end,
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
    opts = { highlight = { keyword = 'fg' }, },
    cond = function() return not vim.g.vscode end,
  },

  { -- search utilities
    'folke/flash.nvim',
    event = 'VeryLazy',
  },

  { -- fuzzy finder
    'nvim-telescope/telescope.nvim',
    branch = '0.1.x',
    dependencies = { 'nvim-lua/plenary.nvim' },
    cond = function() return not vim.g.vscode end,
  },

  { -- list view
    'folke/trouble.nvim',
    dependencies = { "nvim-tree/nvim-web-devicons" },
    opts = {},
    cond = function() return not vim.g.vscode end,
  },

  { -- code folding
    'kevinhwang91/nvim-ufo',
    dependencies = { 'kevinhwang91/promise-async' },
    config = function()
      require('ufo').setup({ -- default to syntax based
        provider_selector = function() return { 'treesitter', 'indent' } end
      })
    end,
    cond = function() return not vim.g.vscode end,
  }
}
