if status is-interactive
    # Commands to run in interactive sessions can go here
end

set -U fish_greeting
set -gx http_proxy 127.0.0.1:7897
set -gx https_proxy 127.0.0.1:7897

alias ls 'eza -l'
alias ff fastfetch
