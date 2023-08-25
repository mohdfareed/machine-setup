local trouble = function()
  local trouble = require('trouble')
  local ref = function() trouble.open("lsp_references") end
  local def = function() trouble.open("lsp_defenitions") end
  local ws = function() trouble.open("workspace_diagnostics") end
  local doc = function() trouble.open("document_diagnostics") end
  local qf = function() trouble.open("quickfix") end
  local ll = function() trouble.open("quickfix") end

  RegisterGroup('<leader>x', "Diagnostics")
  MapKey('n', '<leader>xx', function() trouble.open() end, "Trouble")
  MapKey('n', '<leader>xw', ws, "Show workspace diagonistics")
  MapKey('n', '<leader>xd', doc, "Show document diagnostics")
  MapKey('n', '<leader>xq', qf, "Show quickfix list")
  MapKey('n', '<leader>xl', ll, "Show location list")
  MapKey('n', 'gR', ref, "Show references")
  MapKey('n', 'gD', def, "Show defenitions")

  -- telescope
  local actions = require('telescope.actions')
  local trouble = require('trouble.providers.telescope')
  local telescope = require('telescope')
  telescope.setup {
    defaults = {
      mappings = {
        i = { ["<c-t>"] = trouble.open_with_trouble },
        n = { ["<c-t>"] = trouble.open_with_trouble },
      },
    },
  }
end
ConfigurePlugin(trouble)

return {
 "folke/trouble.nvim",
 dependencies = { "nvim-tree/nvim-web-devicons" },
 opts = {
 },
}
