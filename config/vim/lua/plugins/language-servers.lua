ConfigurePlugin(function()
  CodeActionMenu = function() vim.cmd('CodeActionMenu') end
  LSP = require('lsp-zero').preset({ name = 'recommended' })
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

  require('lspconfig.ui.windows').default_options.border = 'rounded'
  LSP.setup()
end)


ConfigurePlugin(function()
  CMP = require('cmp')

  -- completion window border
  local config = CMP.get_config()
  config.window = {
    completion = CMP.config.window.bordered(),
    documentation = CMP.config.window.bordered(),
  }

  -- completion icons
  ---@diagnostic disable-next-line: missing-fields
  config.formatting = {
    format = require('lspkind').cmp_format({
      mode = 'symbol_text',
      maxwidth = 50,
      ellipsis_char = '...',
      symbol_map = { Copilot = '', }
    })
  }

  -- key mappings
  local cmp_action = require('lsp-zero').cmp_action()
  config.mapping['<cr>'] = CMP.mapping.confirm()
  config.mapping['<tab>'] = cmp_action.luasnip_supertab()
  config.mapping['<s-tab>'] = cmp_action.luasnip_shift_supertab()
  config.mapping['<c-space>'] = cmp_action.toggle_completion()

  -- extra completion sources
  table.insert(config.sources, { name = 'nvim_lua' })
  table.insert(config.sources, { name = 'buffer' })
  table.insert(config.sources, { name = 'path' })
  table.insert(config.sources, { name = 'spell' })
  table.insert(config.sources, { name = 'luasnip' })

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
      { 'onsails/lspkind.nvim' },
      { 'folke/neodev.nvim',                opts = {} },
      { 'weilbith/nvim-code-action-menu', },
      {
        'kosayoda/nvim-lightbulb',
        opts = {
          autocmd = { enabled = true },
          sign = { text = '' },
        }
      },

      -- auto-completion
      { 'hrsh7th/nvim-cmp' },
      { 'hrsh7th/cmp-nvim-lsp' },
      { 'hrsh7th/cmp-nvim-lua' },
      { 'hrsh7th/cmp-buffer' },
      { 'hrsh7th/cmp-path' },
      { 'f3fora/cmp-spell' },

      -- snippets
      { 'L3MON4D3/LuaSnip' },
      { 'saadparwaiz1/cmp_luasnip' },
      { 'rafamadriz/friendly-snippets' },
    },
    cond = function() return not vim.g.vscode end,
  }
}
