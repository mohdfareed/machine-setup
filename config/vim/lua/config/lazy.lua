local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
	-- bootstrap lazy.nvim
	vim.fn.system({
		"git",
		"clone",
		"--filter=blob:none",
		"https://github.com/folke/lazy.nvim.git",
		"--branch=stable",
		lazypath,
	})
end
vim.opt.rtp:prepend(vim.env.LAZY or lazypath)

require("lazy").setup({
	spec = {
		-- add LazyVim and import its plugins
		{ "LazyVim/LazyVim", import = "lazyvim.plugins" },
		-- import any 'extras' modules
		{ import = "lazyvim.plugins.extras.coding.copilot" },
		{ import = "lazyvim.plugins.extras.lang.python" },
		{ import = "lazyvim.plugins.extras.formatting.prettier" },
		-- import/override with custom plugins
		{ import = "plugins" },
	},
	defaults = {
		lazy = false, -- lazy-load custom plugins
		version = false, -- always use the latest git commit
		-- version = "*", -- try installing the latest stable version for plugins
	},
	checker = { enabled = true }, -- automatically check for plugin updates
	performance = {
		rtp = {
			-- disable some rtp plugins
			disabled_plugins = {
				-- "tutor",
			},
		},
	},
})
