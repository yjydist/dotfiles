-- bootstrap lazy.nvim, LazyVim and your plugins
require("config.lazy")

-- neovide 设置
if vim.g.neovide then
  -- neovide 字体设置
  vim.o.guifont = "JetbrainsMonoNL Nerd Font:h14"
end
