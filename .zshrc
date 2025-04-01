# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/Users/jakesilver/opt/anaconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/Users/jakesilver/opt/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/Users/jakesilver/opt/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/Users/jakesilver/opt/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

export ELEVENLABS_API_KEY='sk_470ef187d4e35cfc9798688621afde67b9a617c06305bbb8'
export OPENAI_API_KEY='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'

# opam configuration
[[ ! -r /Users/jakesilver/.opam/opam-init/init.zsh ]] || source /Users/jakesilver/.opam/opam-init/init.zsh  > /dev/null 2> /dev/null
source /opt/homebrew/opt/chruby/share/chruby/chruby.sh
source /opt/homebrew/opt/chruby/share/chruby/auto.sh
chruby ruby-3.1.3 # run chruby to see actual version
source /opt/homebrew/opt/chruby/share/chruby/chruby.sh
source /opt/homebrew/opt/chruby/share/chruby/auto.sh
chruby ruby-3.1.3 # run chruby to see actual version
source /opt/homebrew/opt/chruby/share/chruby/chruby.sh
source /opt/homebrew/opt/chruby/share/chruby/auto.sh
chruby ruby-3.1.3 # run chruby to see actual version
source /opt/homebrew/opt/chruby/share/chruby/chruby.sh
source /opt/homebrew/opt/chruby/share/chruby/auto.sh
chruby ruby-3.1.3 # run chruby to see actual version

export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"


alias make=gmake

# The next line updates PATH for the Google Cloud SDK.
if [ -f '/Users/jakesilver/Documents/google-cloud-sdk/path.zsh.inc' ]; then . '/Users/jakesilver/Documents/google-cloud-sdk/path.zsh.inc'; fi

# The next line enables shell command completion for gcloud.
if [ -f '/Users/jakesilver/Documents/google-cloud-sdk/completion.zsh.inc' ]; then . '/Users/jakesilver/Documents/google-cloud-sdk/completion.zsh.inc'; fi
export PATH=$PATH:/Users/jakesilver/Documents/google-cloud-sdk/bin
export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"
export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"
