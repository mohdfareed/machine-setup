return {
	-- dracula theme
	{
		"Mofiqul/dracula.nvim",
		opts = {
			transparent_bg = true,
		},
	},

	-- set theme colorscheme
	{
		"LazyVim/LazyVim",
		opts = {
			colorscheme = "dracula",
		},
	},

	-- symbols-outline
	{
		"simrat39/symbols-outline.nvim",
		cmd = "SymbolsOutline",
		keys = { { "<leader>cs", "<cmd>SymbolsOutline<cr>", desc = "Symbols Outline" } },
		config = true,
	},
}
