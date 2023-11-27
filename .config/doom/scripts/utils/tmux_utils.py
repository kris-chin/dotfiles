import libtmux

#gets the tmux server, AND session
def setup_tmux():
    server = libtmux.Server()
    return server

#takes a tmux server and attempts to find the first pane that is running zsh
def find_first_zsh_pane(tmux):
    for session in tmux.sessions:
        for pane in session.panes:
            pane_name = pane.cmd('display-message', '-p', '#{pane_current_command}').stdout[0]
            if (pane_name == "zsh"):
                return pane
    return None
