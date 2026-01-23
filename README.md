# karabiner-config

karabiner & rectangle configs :smile:

## Usage

### Karabiner

Clone directly to `$HOME/.config/karabiner`.
Karabiner stores its settings there, should be easy to version.

### Rectangle

#### Export (Rectangle -> Repo)

To export from Rectangle (when you change a setting in Rectangle).

From the current folder:

```bash
./rectangle_export.py
```

The main thing `rectangle_export.py` does is ensure that the settings are stably sorted, for versioning.

The result is written to `Rectangle.plist`

#### Import (Repo -> Rectangle)

From the current folder:

```bash
./rectangle_import.sh
```

Main thing this does is quit Rectangle, import `Rectangle.plist`,
then reopen Rectangle.