local treesitter = function()
  require('nvim-treesitter.configs').setup({
    ensure_installed = { 'c', 'lua', 'python' },
    auto_install = false,
    highlight = { enable = true },
    indent = { enable = true },
  })

  -- enable syntax based code folding
  vim.opt.foldmethod = 'expr'
  vim.opt.foldexpr='nvim_treesitter#foldexpr()'
  vim.opt.foldlevelstart = 99
end
table.insert(PluginConfigs, treesitter)

return {
  'nvim-treesitter/nvim-treesitter-context',

  {
    'nvim-treesitter/nvim-treesitter',
    cmd = { "TSUpdateSync" },
    dependencies = {
      'nvim-treesitter/nvim-treesitter-textobjects',
    },
    build = ':TSUpdate',
  },
}
