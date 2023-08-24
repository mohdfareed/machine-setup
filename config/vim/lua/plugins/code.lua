local mapper = function ()
  -- todo comments
  local todo = require('todo-comments')
  MapKey('n', ']t', function() todo.jump_next() end, "Next todo list")
  MapKey('n', '[t', function() todo.jump_prev() end, "Previous todo list")

  -- flash search utility
  local flash = require('flash')
  MapKey({ 'n', 'x', 'o' }, 's', flash.jump, "Flash")
  MapKey({ 'n', 'o', 'x' }, 'S', flash.treesitter, "Flash Treesitter")
  MapKey({ 'o' }, 'r', flash.remote, "Remote Flash")
  MapKey({ 'o', 'x' }, 'R', flash.treesitter_search, "Treesitter Search")
  MapKey({ 'c' }, '<c-s>', flash.toggle, "Toggle Flash Search")
end
table.insert(PluginsMappers, mapper)

return {
  'tpope/vim-sleuth', -- auto-detect indents
  { 'numToStr/Comment.nvim', opts = {} }, -- comment code

  { -- todo comments manager
    'folke/todo-comments.nvim',
    dependencies = { 'nvim-lua/plenary.nvim' },
    opts = { highlight = { keyword = 'fg' }, }
  },

  { -- search utilities
    'folke/flash.nvim',
    event = 'VeryLazy',
  },
}
