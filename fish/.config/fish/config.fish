if status is-interactive
    # Commands to run in interactive sessions can go here
end

set -U fish_greeting



# Load all fish config files in ~/.config/fish/conf.d
for file in ~/.config/fish/conf.d/*.fish
    source $file
end




