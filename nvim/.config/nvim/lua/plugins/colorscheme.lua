-- 安装 gruvbox 主题
return {
  "ellisonleao/gruvbox.nvim",
  priority = 1000, -- 确保主题优先加载
  config = function()
    -- 设置 gruvbox 主题
    vim.o.background = "dark" -- 或 "light" 切换亮色/暗色模式
    vim.cmd("colorscheme gruvbox")
  end,
}
