local telescope = function()
  local telescope = require('telescope')
  local builtin = require('telescope.builtin')
  pcall(telescope.load_extension, 'fzf')

  RegisterGroup('<leader><space>', "Search")
  MapKey('n', '<leader><space>f', builtin.find_files, "Files")
  MapKey('n', '<leader><space>g', builtin.live_grep, "Grep")
  MapKey('n', '<leader>/', builtin.current_buffer_fuzzy_find,
    "Fuzzily search current buffer")

  MapKey('n', '<leader><space>h', builtin.help_tags, "Help")
  MapKey('n', '<leader><space>k', builtin.keymaps, "Keymaps")
  MapKey('n', '<leader><space>c', builtin.commands, "Commands")
  MapKey('n', '<leader><space>C', builtin.commands, "Commands history")
  MapKey('n', '<leader><space><space>', builtin.search_history, "History")
  MapKey('n', '<leader><space>x', builtin.diagnostics, "Diagnostics")

  MapKey('n', '<leader>gf', builtin.git_files, "Search git files")
  MapKey('n', '<leader>gc', builtin.git_commits, "Search commits")
  MapKey('n', '<leader>gC', builtin.git_bcommits, "Search buffer commits")

  MapKey('n', '<leader>lr', builtin.lsp_references, "List references")
  MapKey('n', '<leader>lo', builtin.lsp_outgoing_calls, "List outgoing calls")
  MapKey('n', '<leader>li', builtin.lsp_incoming_calls, "List incoming calls")
  MapKey('n', 'gd', builtin.lsp_definitions, "Go to definition")
  MapKey('n', 'gi', builtin.lsp_implementations, "Go to implementation")
end
ConfigurePlugin(telescope)

return {
  {
    'nvim-telescope/telescope.nvim',
    branch = '0.1.x',
    dependencies = {
      'nvim-lua/plenary.nvim',
      {
        'nvim-telescope/telescope-fzf-native.nvim',
        build = 'make',
        cond = function() return vim.fn.executable 'make' == 1 end,
      },
    },
  },
}
