if status is-interactive
    # Commands to run in interactive sessions can go here
end

set -U fish_greeting

# set PATH
set -gx PATH /opt/homebrew/bin $PATH
set -gx PATH $PATH /Users/yjydist/.spicetify
set -gx PATH /opt/homebrew/opt/openjdk/bin $PATH
set -gx PATH /usr/local/bin $PATH
# set alias
alias mc="macchina -o host -o kernel -o terminal -o shell -o packages -o memory"
alias ls="eza -l"
