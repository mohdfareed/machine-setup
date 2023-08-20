local function copy(lines, _)
	require("osc52").copy(table.concat(lines, "\n"))
end

local function paste()
	return { vim.fn.split(vim.fn.getreg(""), "\n"), vim.fn.getregtype("") }
end

vim.g.clipboard = {
	name = "clipboard",
	copy = { ["+"] = copy, ["*"] = copy },
	paste = { ["+"] = paste, ["*"] = paste },
}

return {
	{ -- system clipboard
		"ojroques/nvim-osc52",
	},
}
