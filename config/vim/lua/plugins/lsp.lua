local function lsp()
  local lsp = require('lsp-zero').preset({})

  lsp.ensure_installed({
    'pyright',
    'lua_ls',
  })

  lsp.on_attach(function(_, bufnr)
    lsp.default_keymaps({ buffer = bufnr })
    lsp.buffer_autoformat() -- autoformat
  end)

  lsp.set_sign_icons({
    error = '',
    warn = '',
    hint = '',
    info = ''
  })
  -- fix undefined global 'vim'
  lsp.configure('lua_ls', {
    settings = {
      Lua = { diagnostics = { globals = { 'vim' } } }
    }
  })

  require('lspconfig.ui.windows').default_options.border = 'rounded'
  lsp.setup()
end

local function cmp()
  local cmp = require('cmp')
  local config = cmp.get_config()
  local cmp_action = require('lsp-zero').cmp_action()

  config.window = {
    completion = cmp.config.window.bordered(),
    documentation = cmp.config.window.bordered(),
  }

  config.mapping = {
    ['<CR>'] = cmp.mapping.confirm({ select = false }),
    ['<C-f>'] = cmp_action.luasnip_jump_forward(),
    ['<C-b>'] = cmp_action.luasnip_jump_backward(),
  }

  table.insert(config.sources, { name = 'spell' })
  table.insert(config.sources, { name = 'luasnip' })

  require('luasnip.loaders.from_vscode').lazy_load()
  cmp.setup(config)
end

local config = function()
  lsp()
  cmp()
end
ConfigurePlugin(config)

return {
  {
    'VonHeikemen/lsp-zero.nvim',
    branch = 'v2.x',
    dependencies = {
      -- lsp support
      { 'neovim/nvim-lspconfig' },
      {
        'williamboman/mason.nvim',
        opts = { ui = { border = 'rounded' }, }
      },
      { 'williamboman/mason-lspconfig.nvim' },
      { 'folke/neodev.nvim',                opts = {} },

      -- auto-completion
      { 'hrsh7th/nvim-cmp' },
      { 'hrsh7th/cmp-nvim-lsp' },
      { 'f3fora/cmp-spell' },

      -- snippets
      { 'L3MON4D3/LuaSnip' },
      { 'saadparwaiz1/cmp_luasnip' },
      { 'rafamadriz/friendly-snippets' },
    }
  }
}
