-- convert leader to group
RegisterGroup('<space>', "Leader")
MapKey({ 'n', 'v' }, '<space>', '<nop>', "Leader", { silent = true })
-- leader group
MapKey('n', '<leader>e', NeoTree.toggle, "File explorer")

-- show keymaps
local modes = { 'n', 'v', 'x', 'o', 'i', 'c', 't', }
for _, mode in ipairs(modes) do
  local keymap = function() vim.cmd('WhichKey "" ' .. mode) end
  MapKey(mode, '<c-?>', keymap, "Show keymap")
end

-- diagnostics
RegisterGroup('<leader>x', "Diagnostics")
-- MapKey('n', '<leader>xd', vim.diagnostic.open_float, "Open floating diagnostic message")
-- MapKey('n', '<leader>xl', vim.diagnostic.setloclist, "Open diagnostics list")


-- completions
MapKey('i', '<c-space>', ToggleCompletion, "Complete")
MapKey('i', '<cr>', CMP.mapping.confirm({ select = true }), "Confirm")


-- window management
MapKey('n', '<c-w>H', '<c-w>H', "Move window to the right")
MapKey('n', '<c-w>J', '<c-w>J', "Move window Down")
MapKey('n', '<c-w>K', '<c-w>K', "Move window Up")
MapKey('n', '<c-w>L', '<c-w>L', "Move window to the left")

-- session management
RegisterGroup('<leader>q', "Session")
MapKey('n', '<leader>qq', '<cmd>qa<cr>', "Quit all")
MapKey('n', '<leader>qs', Persistence.load, "Load session")
MapKey('n', '<leader>ql', Persistence.load_last, "Load last session")
MapKey('n', '<leader>qd', Persistence.stop, "Delete session")

-- git
RegisterGroup('<leader>g', "Git")
MapKey('n', '<leader>gg', Lazygit, "LazyGit")
MapKey('n', '<leader>gp', Git.preview_hunk, "Preview hunk")
MapKey('n', '<leader>gt', Git.toggle_deleted, "Toggle deleted lines")
MapKey('n', '<leader>gb', Git.blame_line, "Blame line")

-- window management
MapKey('n', '<c-w>H', '<c-w>H', "Move window to the right")
MapKey('n', '<c-w>J', '<c-w>J', "Move window Down")
MapKey('n', '<c-w>K', '<c-w>K', "Move window Up")
MapKey('n', '<c-w>L', '<c-w>L', "Move window to the left")

-- flash
MapKey({ 'n', 'x', 'o' }, 's', Flash.jump, "Flash")
MapKey({ 'n', 'o', 'x' }, 'S', Flash.treesitter, "Flash Treesitter")
MapKey({ 'o' }, 'r', Flash.remote, "Remote Flash")
MapKey({ 'o', 'x' }, 'R', Flash.treesitter_search, "Treesitter Search")
MapKey({ 'c' }, '<c-s>', Flash.toggle, "Toggle Flash Search")

-- trouble
local trouble = require('trouble')
local ref = function() trouble.open("lsp_references") end
local def = function() trouble.open("lsp_defenitions") end
local ws = function() trouble.open("workspace_diagnostics") end
local doc = function() trouble.open("document_diagnostics") end
local qf = function() trouble.open("quickfix") end
local ll = function() trouble.open("locfiles") end

RegisterGroup('<leader>x', "Diagnostics")
MapKey('n', '<leader>xx', function() trouble.open() end, "Trouble")
MapKey('n', '<leader>xw', ws, "Show workspace diagonistics")
MapKey('n', '<leader>xd', doc, "Show document diagnostics")
MapKey('n', '<leader>xq', qf, "Show quickfix list")
MapKey('n', '<leader>xl', ll, "Show location list")
MapKey('n', 'gR', ref, "Show references")
MapKey('n', 'gD', def, "Show defenitions")

-- telescope
local builtin = require('telescope.builtin')
RegisterGroup('<leader><space>', "Search")
MapKey('n', '<leader><space>', builtin.find_files, "Files")
MapKey('n', '<leader><space>g', builtin.live_grep, "Grep")
MapKey('n', '<leader>/', builtin.current_buffer_fuzzy_find, "Search buffer")
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

-- remaps --------------------------------------------------------------------

-- move through wrapped lines as separate lines
MapKey('n', 'k', "v:count == 0 ? 'gk' : 'k'", nil, {
  expr = true, silent = true
})
MapKey('n', 'j', "v:count == 0 ? 'gj' : 'j'", nil, {
  expr = true, silent = true
})

-- center after jumping screen
MapKey('n', '<c-d>', '<c-d>zz', "Page down and center")
MapKey('n', '<c-u>', '<c-u>zz', "Page up and center")

-- groups renames
RegisterGroup('g', "Goto")
RegisterGroup('[', "Previous")
RegisterGroup(']', "Next")
