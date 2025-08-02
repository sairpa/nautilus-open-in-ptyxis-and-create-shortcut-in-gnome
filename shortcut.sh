#!/bin/bash
# Quick script to add Ptyxis Flatpak shortcut

KEY_COMBO="${1:-<Primary>t}"
CUSTOM_PATH="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/"

# Add to custom keybindings list
gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "['$CUSTOM_PATH']"

# Set the keybinding properties
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$CUSTOM_PATH name 'Launch Ptyxis Terminal'
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$CUSTOM_PATH command 'flatpak run app.devsuite.Ptyxis'
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$CUSTOM_PATH binding "$KEY_COMBO"

echo "Ptyxis (Flatpak) shortcut created with key combination: $KEY_COMBO"