# MiSTer Companion Themes

This repository contains themes for the MiSTer Companion Theme Store.

Themes in this repository can be shown inside MiSTer Companion with a preview image, author name, and install option.

## Repository Structure

```text
index.json
official-themes/
  theme_name.json
  theme_name.png
community-themes/
  community_theme.json
  community_theme.png
tools/
  generate_index.py
.github/
  workflows/
    update-index.yml
```

## Official Themes

Official themes are created and maintained by Anime0t4ku.

These themes are stored in:

```text
official-themes/
```

## Community Themes

Community themes are created by users and contributors.

These themes are stored in:

```text
community-themes/
```

## Adding a Community Theme

If you would like to add your own custom theme, you can open a pull request.

Please include:

- Your theme JSON file
- A screenshot or preview image of the theme

Both files should use the same filename.

Example:

```text
community-themes/my_theme.json
community-themes/my_theme.png
```

Preview images can be:

```text
.png
.jpg
.jpeg
```

## Theme Format

Themes use the normal MiSTer Companion theme format:

```json
{
  "id": "my_theme",
  "name": "My Theme",
  "author": "Your Name",
  "background": "#ffffff",
  "surface": "#f3f4f6",
  "accent": "#7c3aed",
  "text": "#111827"
}
```

## Index Generation

The `index.json` file is generated automatically by GitHub Actions.

When themes or preview images are added or changed, the workflow updates the index so MiSTer Companion can display them in the Theme Store.