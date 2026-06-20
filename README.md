# 📘 README.md

```md
# Word Highlighter

Highlight words dynamically in Sublime Text with support for:

- ✅ Whole words
- ✅ Partial matches inside words
- ✅ Regex patterns
- ✅ Custom colors (via Sublime scopes)

Built for performance and designed to work well even with **large files**.

---

# ✨ Features

- 🔍 Highlight **exact words** (e.g. `TODO`)
- 🔎 Highlight **parts of words** (e.g. `onnected` inside `Disconnected`)
- 🧠 Highlight **regex patterns** (e.g. `\d+` for numbers)
- 🎨 Customize appearance using Sublime color scopes
- ⚡ Manual trigger → no performance issues on large files

---

# 🚀 Installation

## Option 1 — Manual install (recommended for now)

1. Open Sublime
2. Go to:
```

Preferences → Browse Packages...

```
3. Navigate to `Packages/`
4. Create a folder:
```

WordHighlighter

```
5. Copy these files into it:
- `word_highlighter.py`
- `Default.sublime-commands`
- `WordHighlighter.sublime-settings`

✅ Done!

---

## Option 2 — Package Control (after publishing)

Once published:

1. Open Command Palette:
```

Ctrl + Shift + P

```
2. Run:
```

Package Control: Install Package

```
3. Search:
```

Word Highlighter

```

---

# 🧑‍💻 Usage

## Apply highlights

```

Command Palette → Highlight Words (Custom)

```

---

## Clear highlights

```

Command Palette → Clear Word Highlights

```

---

## Edit highlight settings

```

Command Palette → Edit Highlight Words

```

This opens your settings file:
```

Packages/User/WordHighlighter.sublime-settings

````

---

# ⚙️ Configuration

Edit your settings file:

```json
{
    "whole_words": {
        "TODO": "string",
        "ERROR": "invalid"
    },

    "partial_words": {
        "onnected": "keyword"
    },

    "regex_patterns": {
        "\\d+": "constant.numeric"
    }
}
````

***

# 🧠 How It Works

## 🔹 Whole Words

Matches exact words only:

```json
"whole_words": {
    "TODO": "string"
}
```

✅ Matches:

```
TODO
```

❌ Does NOT match:

```
METHOD
```

***

## 🔹 Partial Words

Matches anywhere inside a word:

```json
"partial_words": {
    "onnected": "keyword"
}
```

✅ Matches:

```
Connected
Disconnected
```

(only the matching part is highlighted)

***

## 🔹 Regex Patterns

Full regex support:

```json
"regex_patterns": {
    "\\d+": "constant.numeric"
}
```

✅ Matches:

```
123
42
9999
```

***

# 🎯 Highlight Priority

If multiple rules overlap:

```
partial < whole < regex
```

👉 Regex overrides everything  
👉 Whole words override partial matches

***

# 🎨 Colors

Colors are defined using **Sublime scopes**, not raw colors.

Examples:

| Scope       | Typical Color |
| ----------- | ------------- |
| `"string"`  | green         |
| `"invalid"` | red           |
| `"comment"` | gray          |
| `"keyword"` | blue          |

⚠️ Actual colors depend on your theme.

***

# ⚡ Performance

* Highlights are applied **only when manually triggered**
* No background scanning
* Designed for **large files**

***

# 🧩 Commands

| Command                  | Description           |
| ------------------------ | --------------------- |
| Highlight Words (Custom) | Apply highlights      |
| Clear Word Highlights    | Remove all highlights |
| Edit Highlight Words     | Open settings file    |

***

# 🛠️ Development Notes

* Written in Python (Sublime API)
* Uses region tracking for safe clearing
* Regex patterns are validated safely

***

# 📌 Future Ideas

* Toggle highlighting on/off
* Visible-region-only highlighting
* Interactive UI for managing rules
