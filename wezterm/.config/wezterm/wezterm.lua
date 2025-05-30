local wezterm = require 'wezterm'

local config = wezterm.config_builder()

-- theme settings
config.color_scheme = 'Catppuccin Mocha'

-- window settings
config.initial_cols = 120
config.initial_rows = 30

-- font settings
config.font_size = 12
config.font = wezterm.font('FiraCode Nerd Font', { weight = 'Regular', italic = false })



return config