return {
	{ -- configure LazyVim
		"LazyVim/LazyVim",
		opts = {
			colorscheme = "onedark",
		},
	},

	{ -- symbols-outline
		"simrat39/symbols-outline.nvim",
		cmd = "SymbolsOutline",
		keys = { { "<leader>cs", "<cmd>SymbolsOutline<cr>", desc = "Symbols Outline" } },
		config = true,
	},

	{ -- fix notifications background color
		"rcarriga/nvim-notify",
		opts = {
			background_color = "#000000",
		},
	},

	-- disabled plugins
	{ "akinsho/bufferline.nvim", enabled = false },
}
