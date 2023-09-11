-- convert leader to group
RegisterGroup('<space>', "Leader")
MapKey({ 'n', 'v' }, '<space>', '<nop>', "Leader", { silent = true })
if not vim.g.vscode then

-- leader group
MapKey('n', '<leader>e', NeoTree.toggle, "File explorer")
MapKey('n', '<leader>s', Telescope.builtin.builtin, "Search")
MapKey('n', '<leader>/', Telescope.builtin.fuzzy_buffer, "Search buffer")
MapKey('n', '<leader>?', Telescope.builtin.live_grep, "Search files")
MapKey('n', '<leader><space>', Telescope.builtin.find_files, "Find file")
MapKey('n', '<leader>h', Harpoon.open, "Open Harpoon")

-- show keymaps
local modes = { 'n', 'v', 'x', 'o', 'i', 'c', 't', }
for _, mode in ipairs(modes) do
  local keymap = function() vim.cmd('WhichKey "" ' .. mode) end
  MapKey(mode, '<c-?>', keymap, "Show keymap")
end

-- marked files
for i=1,4 do -- show only 4 marks
  MapKey('n', '<leader>' .. i, Harpoon.goto(i), "Goto mark ".. i)
end

-- diagnostics
RegisterGroup('<leader>x', "Diagnostics")
MapKey('n', '<leader>xo', vim.diagnostic.open_float, "Open message")
MapKey('n', '<leader>xc', CodeActionMenu, "Code actions")
MapKey('n', '<leader>xw', WorkspaceDiagnostics, "Show workspace diagonistics")
MapKey('n', '<leader>xd', DocumentDiagnostics, "Show document diagnostics")

-- harpoon
RegisterGroup('<leader>h', "Harpoon")
MapKey('n', '<leader>h', Harpoon.open, "Menu")
MapKey('n', '<leader>ha', Harpoon.mark.add_file, "Add file")
MapKey('n', '<leader>hc', Harpoon.cmd_ui.toggle_quick_menu, "Commands")

-- session management
RegisterGroup('<leader>q', "Session")
MapKey('n', '<leader>qq', '<cmd>qa<cr>', "Quit all")
MapKey('n', '<leader>qs', Persistence.load, "Load session")
MapKey('n', '<leader>ql', Persistence.load_last, "Load last session")
MapKey('n', '<leader>qc', '<cmd>bp<bar>sp<bar>bn<bar>bd<cr>', "Close buffer")

-- git
RegisterGroup('<leader>g', "Git")
MapKey('n', '<leader>gg', Lazygit, "LazyGit")
MapKey('n', '<leader>gp', Git.preview_hunk, "Preview hunk")
MapKey('n', '<leader>gt', Git.toggle_deleted, "Toggle deleted lines")
MapKey('n', '<leader>gb', Git.blame_line, "Blame line")

end
-- remaps (applied in vscode)---------------------------------------------------

-- move through wrapped lines as separate lines
MapKey('n', 'k', "v:count == 0 ? 'gk' : 'k'", nil, {
  expr = true, silent = true
})
MapKey('n', 'j', "v:count == 0 ? 'gj' : 'j'", nil, {
  expr = true, silent = true
})

-- flash
MapKey({ 'n', 'x', 'o' }, 's', Flash.jump, "Flash")
MapKey({ 'n', 'o', 'x' }, 'S', Flash.treesitter, "Flash Treesitter")
MapKey({ 'o' }, 'r', Flash.remote, "Remote Flash")
MapKey({ 'o', 'x' }, 'R', Flash.treesitter_search, "Treesitter Search")
MapKey({ 'c' }, '<c-s>', Flash.toggle, "Toggle Flash Search")

-- code folding
if not vim.g.vscode then
  MapKey('n', 'zR', UFO.openAllFolds, "Open all folds")
  MapKey('n', 'zM', UFO.closeAllFolds, "Close all folds")
  MapKey('n', 'zr', UFO.openFoldsExceptKinds, "Open all folds except kinds")
  MapKey('n', 'zm', UFO.closeFoldsWith, "Close all folds with kinds")
end

-- window management
MapKey('n', '<c-w>H', '<c-w>H', "Move window to the right")
MapKey('n', '<c-w>J', '<c-w>J', "Move window Down")
MapKey('n', '<c-w>K', '<c-w>K', "Move window Up")
MapKey('n', '<c-w>L', '<c-w>L', "Move window to the left")

-- center after jumping screen
MapKey('n', '<c-d>', '<c-d>zz', "Page down and center")
MapKey('n', '<c-u>', '<c-u>zz', "Page up and center")

-- groups renames
RegisterGroup('g', "Goto")
RegisterGroup('[', "Previous")
RegisterGroup(']', "Next")
