local function gitsigns_mapper(buffer)
  local function visual_selection()
    return { { vim.fn.line('.'), vim.fn.line('v') } }
  end

  local gs = require('gitsigns')
  local stage_selection = function() gs.stage_hunk(visual_selection) end
  local reset_selection = function() gs.reset_hunk(visual_selection) end
  local blame_line = function() gs.blame_line { full = true } end

  MapKey('n', ']g', function()
    if vim.wo.diff then return ']c' end
    vim.schedule(function() gs.next_hunk() end)
    return '<Ignore>'
  end, "Next git hunk", {expr=true})
  MapKey('n', '[g', function()
    if vim.wo.diff then return '[c' end
    vim.schedule(function() gs.prev_hunk() end)
    return '<Ignore>'
  end, "Previous git hunk", {expr=true})

  RegisterGroup('<leader>g', "Git")
  MapKey('n', '<leader>gs', gs.stage_hunk, "Stage hunk")
  MapKey('n', '<leader>gr', gs.reset_hunk, "Reset hunk")
  MapKey('v', '<leader>gs', stage_selection, "Stage selection")
  MapKey('v', '<leader>gr', reset_selection, "Reset selection")
  MapKey('n', '<leader>gS', gs.stage_buffer, "Stage buffer")
  MapKey('n', '<leader>gu', gs.undo_stage_hunk, "Unstage buffer")
  MapKey('n', '<leader>gR', gs.reset_buffer, "Reset buffer")
  MapKey('n', '<leader>gp', gs.preview_hunk, "Preview hunk")
  MapKey('n', '<leader>gb', blame_line, "Blame line")
  MapKey('n', '<leader>gB', gs.toggle_current_line_blame, "Toggle blame line")
  MapKey('n', '<leader>gd', gs.diffthis, "Diff against index")
  MapKey('n', '<leader>gD', function() gs.diffthis('~') end, "Diff against head")
  MapKey('n', '<leader>gt', gs.toggle_deleted, "Toggle deleted lines")
  MapKey({'o', 'x'}, 'ih', ':<C-U>Gitsigns select_hunk<CR>', "Select git hunk")
end

return {
  {
    'lewis6991/gitsigns.nvim',
    opts = {
      on_attach = gitsigns_mapper,
      preview_config = { border = 'rounded' },
    },
  },
}
