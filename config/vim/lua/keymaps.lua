-- load plugins keymaps
LoadPluginConfigs()

-- convert leader to group
RegisterGroup('<Space>', "Leader")
MapKey({ 'n', 'v' }, '<Space>', '<Nop>', "Leader", { silent = true })

-- center screen after jumping screen
MapKey('n', '<C-d>', '<C-d>zz', "Page down and center")
MapKey('n', '<C-u>', '<C-u>zz', "Page up and center")

-- move through wrapped lines as separate lines
MapKey('n', 'k', "v:count == 0 ? 'gk' : 'k'", nil, {
  expr = true, silent = true
})
MapKey('n', 'j', "v:count == 0 ? 'gj' : 'j'", nil, {
  expr = true, silent = true
})

-- diagnostics
RegisterGroup('<leader>x', "Diagnostics")
MapKey('n', '[d', vim.diagnostic.goto_prev, "Previous diagnostic message")
MapKey('n', ']d', vim.diagnostic.goto_next, "Next diagnostic message")
MapKey('n', '<leader>xd', vim.diagnostic.open_float, "Open floating diagnostic message")
MapKey('n', '<leader>xl', vim.diagnostic.setloclist, "Open diagnostics list")

-- window management
MapKey('n', '<c-w>H', '<c-w>L', "Move window to the left")
MapKey('n', '<c-w>L', '<c-w>H', "Move window to the right")
MapKey('n', '<c-w>J', '<c-w>J', "Move window Down")
MapKey('n', '<c-w>K', '<c-w>K', "Move window Up")

-- session management
RegisterGroup('<leader>q', "Session")
MapKey('n', '<leader>qq', '<cmd>qa<cr>', "Quit all")

-- groups
RegisterGroup('g', "Goto")
RegisterGroup('[', "Previous")
RegisterGroup(']', "Next")
