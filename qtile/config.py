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

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod1"
terminal = guess_terminal()


background_colors = ["32174D"]
colors = ["FFBDF7", "9C51B6", "c3e88d", "89ddff",
          "ffcb6b", "f78c6c", "82aaff", "e1addc"]


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "o", lazy.layout.maximize()),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift", "control"], "r",
        lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift", "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "d", lazy.spawn('rofi -show run'),
        desc="Spawn rofi"),

    # Launching User Application
    Key(['control', 'shift'], "s", lazy.spawn('flameshot gui')),
    Key([mod, 'control'], "p", lazy.spawn('pavucontrol')),
    Key([mod, 'control'], "o", lazy.spawn('chromium')),
    Key(["mod4"], "e", lazy.spawn('pcmanfm')),
    Key([mod, 'control'], "b", lazy.spawn('blueman-manager')),
    Key([mod, 'control'], "c", lazy.spawn('octave --gui')),
    Key([mod, 'control', 'shift'], "i", lazy.spawn('shutdown -h now')),
    Key([mod], "f",
        lazy.window.toggle_floating(),
        desc='toggle floating'
        ),
    Key([], 'XF86AudioMute', lazy.spawn('amixer -D pulse set Master toggle')),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn(
            'pactl set-sink-volume @DEFAULT_SINK@ +5%')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn(
            'pactl set-sink-volume @DEFAULT_SINK@ -5%')),
    Key([], 'XF86MonBrightnessUp',   lazy.spawn('xbacklight -inc 5')),
    Key([], 'XF86MonBrightnessDown', lazy.spawn('xbacklight -dec 5')),
]

groups = [Group(i) for i in "1234567890"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(
                    i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layout_theme = {
    "border_width": 2,
    "margin": 10,
    "border_focus": colors[0],
    "border_normal": colors[1],
}

layouts = [
    layout.MonadTall(**layout_theme),
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(**layout_theme),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
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
                widget.TextBox('💻', padding=0, fontsize=fontsize),
                widget.CPU(
                    format='CPU {load_percent}%',
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
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
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
