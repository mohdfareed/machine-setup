-- Autocmds are automatically loaded on the VeryLazy event
-- Default autocmds that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/autocmds.lua

local function augroup(name)
	return vim.api.nvim_create_augroup("lazyvim_" .. name, { clear = true })
end

-- cd to the argument if it's a directory
vim.api.nvim_create_autocmd("VimEnter", {
	group = augroup("autocd_on_dir"),
	callback = function()
		local arg = vim.fn.expand("<amatch>")
		if vim.fn.isdirectory(arg) == 1 then
			vim.cmd("cd " .. arg)
		end
	end,
})
