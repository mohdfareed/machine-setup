return {
	-- disabled plugins
	{ "akinsho/bufferline.nvim", enabled = false },
	{ "goolord/alpha-nvim", enabled = false },

	{ -- configure LazyVim
		"LazyVim/LazyVim",
		opts = {
			colorscheme = "onedark",
		},
	},

	{ -- symbols-outline
		"simrat39/symbols-outline.nvim",
		cmd = "SymbolsOutline",
		keys = {
			{ "<leader>cs", "<cmd>SymbolsOutline<cr>", desc = "Symbols Outline" },
		},
		config = true,
	},

	{ -- notification banners
		"rcarriga/nvim-notify",
		opts = {
			background_colour = "#000000", -- transparent background
			stages = "fade",
		},
	},

	-- { -- configure bufferline (tabline)
	-- 	"akinsho/bufferline.nvim",
	-- 	opts = {
	-- 		options = {
	-- 			numbers = "buffer_id",
	-- 			show_duplicate_prefix = true,
	-- 			indicator = { icon = "" },
	-- 			offsets = {
	-- 				{
	-- 					filetype = "neo-tree",
	-- 					text = "File Explorer",
	-- 					highlight = "Directory",
	-- 					text_align = "center",
	-- 					separator = true,
	-- 				},
	-- 			},
	-- 			groups = {
	-- 				items = {
	-- 					require("bufferline.groups").builtin.pinned:with({ icon = "" }),
	-- 				},
	-- 			},
	-- 		},
	-- 	},
	-- },
}
