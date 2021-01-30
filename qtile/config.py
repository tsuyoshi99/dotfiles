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

from typing import List  # noqa: F401

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import subprocess

mod = "mod1"
terminal = 'alacritty'


background_colors = ["32174D"]
colors = ["FFBDF7", "9C51B6", "c3e88d", "89ddff",
          "ffcb6b", "f78c6c", "82aaff", "e1addc"]


def backlight(action):
    def f(qtile):
        brightness = int(subprocess.run(['xbacklight', '-get'],
                                        stdout=subprocess.PIPE).stdout)
        if brightness != 1 or action != 'dec':
            if (brightness > 49 and action == 'dec') \
                    or (brightness > 39 and action == 'inc'):
                subprocess.run(['xbacklight', f'-{action}', '10',
                                '-fps', '10'])
            else:
                subprocess.run(['xbacklight', f'-{action}', '1'])
    return f


keys = [
    # Switch between windows in current stack pane
    Key([mod], "j", lazy.layout.down(),
        desc="Move focus down in stack pane"),
    Key([mod], "k", lazy.layout.up(),
        desc="Move focus up in stack pane"),

    # Move windows up or down in current stack
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down in current stack "),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(),
        desc="Move window up in current stack "),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack"),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate(),
        desc="Swap panes of split stack"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown qtile"),
    # Key([mod], "d", lazy.spawncmd(),
    # desc="Spawn a command using a prompt widget"),
    Key([mod, 'control'], "o", lazy.spawn('chromium')),
    Key([mod, "shift"], "f",
        lazy.window.toggle_floating(),
        desc='toggle floating'
        ),
    Key([], 'XF86AudioMute', lazy.spawn('amixer -D pulse set Master toggle')),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn(
            'pactl set-sink-volume @DEFAULT_SINK@ +5%')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn(
            'pactl set-sink-volume @DEFAULT_SINK@ -5%')),
    Key([], 'XF86MonBrightnessUp',   lazy.function(backlight('inc'))),
    Key([], 'XF86MonBrightnessDown', lazy.function(backlight('dec'))),
    Key([mod, "shift"], 'v', lazy.spawn('copyq menu')),
    Key(["control", "shift"], 'p', lazy.spawn('flameshot gui')),
    Key([mod, "shift"], 'l', lazy.spawn(
        'sh -c "i3lock -i /home/tsuyoshi/Pictures/wallpapers/wallpaper.png & sleep 5 && xset dpms force off"')),
    Key([mod, "shift"], 's', lazy.spawn(
        'systemctl suspend')),
    Key([mod], 'd', lazy.spawn(
        'rofi -show run -hide-scrollbar -lines 3 -eh 1 -width 40 -location 8 -xoffset 170 -yoffset 70 -padding 30 -disable-history -font "monospace 18"')),
]

groups = [Group(i) for i in "1234567890"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layout_theme = {
    "border_width": 2,
    "margin": 10,
    "border_focus": colors[0],
    "border_normal": colors[1],
}


layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.Floating(**layout_theme)
]

widget_defaults = dict(
    font='monospace',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()


padding = 10
fontsize = 14

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.CurrentLayout(foreground=colors[0]),
                widget.Prompt(foreground=colors[2]),
                widget.WindowName(foreground=colors[0]),
                widget.TextBox("Pink💜Purple", padding=padding,
                               foreground=colors[0]),
                widget.Sep(
                    linewidth=0,
                    padding=padding
                ),
                widget.TextBox('🔋', padding=0, fontsize=fontsize),
                widget.Battery(foreground=colors[2]),
                widget.Sep(
                    linewidth=0,
                    padding=padding
                ),
                widget.TextBox('📢', padding=0, fontsize=fontsize),
                widget.PulseVolume(foreground=colors[3]),
                widget.Sep(
                    linewidth=0,
                    padding=padding
                ),
                widget.Sep(
                    linewidth=0,
                    padding=padding
                ),
                widget.TextBox('💻', padding=0, fontsize=fontsize),
                widget.CPU(
                    foreground=colors[1]
                ),
                widget.Sep(
                    linewidth=0,
                    padding=padding
                ),
                widget.TextBox(' 🖬', padding=0, fontsize=fontsize,
                               foreground=colors[7]
                               ),
                widget.Memory(
                    foreground=colors[7]
                ),
                widget.Sep(
                    linewidth=0,
                    padding=padding
                ),
                widget.TextBox('🔅', padding=0, fontsize=fontsize),
                widget.Backlight(
                    backlight_name='intel_backlight', foreground=colors[0]),
                widget.Sep(
                    linewidth=0,
                    padding=padding
                ),
                widget.TextBox('📶', padding=0, fontsize=fontsize),
                widget.Wlan(
                    interface="wlp44s0",
                    foreground=colors[4]
                ),
                widget.Sep(
                    linewidth=0,
                    padding=padding
                ),
                widget.TextBox('🚄', padding=0, fontsize=fontsize),
                widget.Net(
                    interface="wlp44s0",
                    format='{down} ↓↑ {up}',
                    foreground=colors[5]
                ),
                widget.Sep(
                    linewidth=0,
                    padding=padding
                ),
                widget.TextBox('📅 ', padding=0, fontsize=fontsize),
                widget.Clock(format='%d-%m-%Y %a %I:%M %p',
                             foreground=colors[3]),
                widget.Sep(
                    linewidth=1,
                    padding=padding
                ),
                widget.Systray(),
            ],
            24,
            background=background_colors[0]
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod, 'shift'], "Button1", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(**layout_theme, float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
