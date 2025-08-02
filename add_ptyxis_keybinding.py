import subprocess
import logging
import os

def add_ptyxis_keybinding_dconf(binding_name="Launch Ptyxis", shortcut="<Super>t", command="sh -c 'flatpak run app.devsuite.Ptyxis'"):
    """
    Adds a custom keybinding in GNOME for launching Ptyxis terminal using dconf, with error checking.
    """
    # Get current custom keybindings
    get_bindings_cmd = [
        "dconf", "read", "/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings"
    ]
    result = subprocess.run(get_bindings_cmd, capture_output=True, text=True)
    current = result.stdout.strip()
    if current in ("", "[]", "@as []"):
        bindings = []
    else:
        try:
            bindings = eval(current.replace("@as ", ""))
        except Exception as e:
            print(f"Error parsing current bindings: {e}")
            bindings = []
    # Find next available binding path
    idx = 0
    while True:
        new_binding = f"/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom{idx}/"
        if new_binding not in bindings:
            break
        idx += 1
    # Set the details for the new keybinding BEFORE updating the list
    base_path = f"/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom{idx}/"
    for prop, value in [
        ("name", binding_name),
        ("command", command),
        ("binding", shortcut)
    ]:
        key_path = base_path + prop
        key_path = key_path.rstrip("/")  # Remove trailing slash
        value_str = f'"{value}"'  # Double quotes for GVariant string
        res = subprocess.run(["dconf", "write", key_path, value_str], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Error writing {prop}: {res.stderr}")
    # Now update the custom-keybindings list
    bindings.append(base_path)
    bindings_str = "[" + ", ".join([f'"{b}"' for b in bindings]) + "]"
    res = subprocess.run(["dconf", "write", "/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings", bindings_str], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error updating custom-keybindings list: {res.stderr}")
    logging.info(f"Added keybinding {shortcut} for Ptyxis terminal using dconf.")
    # Optionally restart GNOME Shell (uncomment if needed)
    # subprocess.run(["killall", "-3", "gnome-shell"])

if __name__ == "__main__":
    add_ptyxis_keybinding_dconf(binding_name="Launch Ptyxis", shortcut="<Super>t", command="sh -c 'flatpak run app.devsuite.Ptyxis'")
