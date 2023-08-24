-- disable leader button
MapKey({ 'n', 'v' }, '<Space>', '<Nop>', "+Leader", { silent = true })

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

for _, mapper in ipairs(PluginsMappers) do
  mapper()
end
