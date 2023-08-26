ConfigurePlugin(function()
  LSP = require('lsp-zero').preset({})

  LSP.ensure_installed({
    'pyright',
    'lua_ls',
  })

  LSP.on_attach(function(_, bufnr)
    LSP.default_keymaps({ buffer = bufnr })
    LSP.buffer_autoformat() -- auto-format
  end)

  -- code folding
  LSP.set_server_config({
    capabilities = {
      textDocument = {
        foldingRange = {
          dynamicRegistration = false,
          lineFoldingOnly = true
        }
      }
    }
  })

  -- editor diagnostics signs
  LSP.set_sign_icons({
    error = '',
    warn = '',
    hint = '',
    info = ''
  })

  -- fix undefined global 'vim'
  LSP.configure('lua_ls', {
    settings = {
      Lua = { diagnostics = { globals = { 'vim' } } }
    }
  })

  -- inline hints


  require('lspconfig.ui.windows').default_options.border = 'rounded'
  LSP.setup()
end)

ConfigurePlugin(function()
  CMP = require('cmp')
  function ToggleCompletion()
    if CMP.visible() then CMP.abort() else CMP.complete() end
  end

  local config = CMP.get_config()
  config.window = {
    completion = CMP.config.window.bordered(),
    documentation = CMP.config.window.bordered(),
  }

  table.insert(config.sources, { name = 'nvim_lua' })
  table.insert(config.sources, { name = 'luasnip' })
  table.insert(config.sources, { name = 'spell' })

  require('luasnip.loaders.from_vscode').lazy_load()
  CMP.setup(config)
end)

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
      { 'hrsh7th/cmp-nvim-lua' },
      { 'f3fora/cmp-spell' },

      -- snippets
      { 'L3MON4D3/LuaSnip' },
      { 'saadparwaiz1/cmp_luasnip' },
      { 'rafamadriz/friendly-snippets' },
    }
  }
}
