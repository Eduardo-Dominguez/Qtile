# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook


mod = "mod4"
terminal = "kitty"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "j", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "k", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "i", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "j", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "i", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "j", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "k", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "i", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "control"], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key([mod, "shift", "control"], "j", lazy.layout.swap_column_left()),
    Key([mod, "shift", "control"], "l", lazy.layout.swap_column_right()),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"],"Return",lazy.layout.toggle_split(),desc="Toggle between split and unsplit sides of stack",),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    #Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "r", lazy.spawn("rofi -show"), desc="Spawn a command using a prompt widget"),

    # User programs
    Key([mod], "c", lazy.spawn("chromium"), desc="Spawn chromium"),
    Key([mod], "f", lazy.spawn("firefox"), desc="Spawn firefox"),
    Key([mod], "d", lazy.spawn("code"), desc="Spawn code"),
    Key([mod], "n", lazy.spawn("nitrogen"), desc="Spawn nitrogen"),
    Key([mod], "u", lazy.spawn('terminator -e "unimatrix -s 93 -a -f -o"'), desc="Spawn unimatrix"),
    Key([mod], "p", lazy.spawn('terminator -e "cd /opt/pycharm-community-2021.3/bin;./pycharm.sh"'), desc="Spawn pycharm"),
    Key([mod], "t", lazy.spawn('thunar'), desc="Spawn thunar"),
    Key([mod], "o", lazy.spawn('libreoffice'), desc="Spawn libreoffice"),
    Key([mod], "b", lazy.spawn('thunderbird'), desc="Spawn thunderbird"),
    Key([mod], "v", lazy.spawn('copyq'), desc="Spawn copyq"),

     # Special Keys (atajos de teclado)
    Key([], "XF86AudioRaiseVolume", lazy.spawn('sh -c "pw-volume change +5%"'), desc="Raise volume"),
    Key([], "XF86AudioLowerVolume", lazy.spawn('sh -c "pw-volume change -5%"'), desc="Lower volume"),
    Key([], "XF86AudioMute", lazy.spawn('pw-volume mute toggle'), desc="Mute volume"),
    Key([], "XF86AudioMicMute", lazy.spawn('amixer set Capture toggle'), desc="Mute mic"),

        #ThinkPad T470 haven't play/pause and previous/next keys, so I use this:
    Key([mod], "Up", lazy.spawn('playerctl play-pause'), desc="Play-Pause"),
    Key([mod], "Down", lazy.spawn('playerctl play-pause'), desc="Play-Pause"),
    Key([mod], "Right", lazy.spawn('playerctl next'), desc="Next"),
    Key([mod], "Left", lazy.spawn('playerctl previous'), desc="Previous"),

    Key([], "XF86AudioPlay", lazy.spawn('playerctl play-pause'), desc="Play-Pause"),
    Key([], "XF86AudioNext", lazy.spawn('playerctl next'), desc="Play-Pause"),
    Key([], "XF86AudioPrev", lazy.spawn('playerctl previous'), desc="Play-Pause"),

    Key([], "XF86MonBrightnessDown", lazy.spawn('xbacklight -dec 10'), desc="Bright down"),
    Key([], "XF86MonBrightnessUp", lazy.spawn('xbacklight -inc 10'), desc="Bright up"),

    Key([], "XF86Display", lazy.spawn('arandr'), desc="Display"),


    Key([], "XF86Bluetooth", lazy.spawn('blueman-applet'), desc="Bluetooth"),

    Key([], "Print", lazy.spawn('sh -c "import -window root ~/Screenshots/$(date "+%Y%m%d-%H%M%S").jpg"'), desc="Screenshot"),
    Key(["control"], "Print", lazy.spawn('spectacle'), desc="Spectacle"), #Also a like use spectacle for my screenshots

]

#groups = [Group(i) for i in "123456789"]

#for i in groups:
    #keys.extend(
        #[
            ## mod1 + letter of group = switch to group
            #Key(
                #[mod],
                #i.name,
                #lazy.group[i.name].toscreen(),
                #desc="Switch to group {}".format(i.name),
            #),
            ## mod1 + shift + letter of group = switch to & move focused window to group
            #Key(
                #[mod, "shift"],
                #i.name,
                #lazy.window.togroup(i.name, switch_group=True),
                #desc="Switch to & move focused window to group {}".format(i.name),
            #),
            ## Or, use below if you prefer not to switch to that group.
            ## # mod1 + shift + letter of group = move focused window to group
            ## Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            ##     desc="move focused window to group {}".format(i.name)),
        #]
    #)

groups = [Group(i) for i in [
    "", "", "", "", "", "", "", "", "",
]]

for i, group in enumerate(groups):
    actual_key = str(i + 1)
    keys.extend([
        # Switch to workspace N
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        # Send window to workspace N
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])


layouts = [
    layout.Columns(border_focus=["#ffffff", "#000000"],
                   border_focus_stack=["#ffffff", "#000000"],
                   border_normal=["#000000", "#000000"],
                   border_normal_stack=["#000000", "#000000"],
                   border_on_single=True,
                   border_width=4,
                   fair=True,
                   grow_amount=5,
                   insert_position=0,
                   margin=0,
                   margin_on_single=50,
                   num_columns=3,
                   split=True,
                   wrap_focus_columns=True,
                   wrap_focus_rows=True,
                   wrap_focus_stacks=True,
                   ),

    layout.Max(),
    #layout.Floating(border_focus='#ffffff',
                    #border_normal='#000000',
                    #border_width=4,
                    #fullscreen_border_width=0,
                    #max_border_width=0
                    #),

    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="manrope bold", 
    fontsize=12,
    padding=3,
    foreground="#000000"
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(
                    padding=8,
                    ),
                widget.GroupBox(
                    font="feather bold",
                    rounded=True,
                    fontsize=14,
                    padding=6,
                    active="#000000",
                    inactive="#A4A4A4",
                    highlight_method='block',
                    this_current_screen_border="#2B7B82"#["#FFE487", "#FFE7A8", "#FEE9A6" ]

                    ),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Systray(),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                widget.QuickExit(
                    font="icomoon-feather",
                    padding = 10,
                    foreground = "#E9524A",
                    default_text = '⏻',
                    countdown_format = '鈴',
                    fontsize = 14,),
            ],
            24, background= "#EEE2C8", margin=[15, 0, 15, 0],  # N E S W  
            border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            border_color=["000000", "000000", "000000", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])
