local create_group = vim.api.nvim_create_augroup
local create_autocmd = vim.api.nvim_create_autocmd

-- highlight on yank
local highlight_group = create_group('YankHighlight', { clear = true })
create_autocmd('TextYankPost', {
  callback = function() vim.highlight.on_yank() end,
  group = highlight_group,
  pattern = '*',
})

