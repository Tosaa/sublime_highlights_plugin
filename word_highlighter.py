"""
Word Highlighter Plugin

This plugin allows highlighting of:
1. Whole words (exact matches)
2. Partial words (substrings inside words)
3. Regex patterns (advanced matching)

Highlight priority:
    partial < whole < regex

Later highlights override earlier ones visually.

Highlights are stored per-view and can be cleared reliably.
"""

import sublime
import sublime_plugin
import json
import re
import os


# ---------------------------------------------------------
# Color options (used in UI elsewhere)
# Maps human-readable label → Sublime scope name
# ---------------------------------------------------------
COLOR_OPTIONS = [
    ("🟥 Red (Error)", "invalid"),
    ("🟩 Green (String)", "string"),
    ("⬜ Gray (Comment)", "comment"),
    ("🟦 Blue (Keyword)", "keyword"),
    ("🟪 Purple (Function)", "entity.name.function"),
    ("🟨 Yellow (Constant)", "constant.numeric")
]


# ---------------------------------------------------------
# Main command: Apply highlighting
# ---------------------------------------------------------
class WordHighlighterCommand(sublime_plugin.TextCommand):
    """
    Applies all configured highlights to the current view.

    Execution flow:
    1. Load settings
    2. Clear existing highlights
    3. Apply highlights in priority order:
       - partial matches
       - whole word matches
       - regex matches
    """

    def run(self, edit):
        settings = self._get_settings()

        # Always clear previous highlights first
        _clear_regions(settings, self.view)

        # Order defines priority (later overrides earlier)
        self._highlight_partial(settings.get("partial_words", {}))
        self._highlight_whole(settings.get("whole_words", {}))
        self._highlight_regex(settings.get("regex_patterns", {}))

    # -------------------------
    # Settings
    # -------------------------

    def _get_settings(self):
        """
        Loads plugin settings from:
        Packages/User/WordHighlighter.sublime-settings
        """
        return sublime.load_settings("WordHighlighter.sublime-settings")

    # -------------------------
    # Highlighting methods
    # -------------------------

    def _highlight_partial(self, words):
        """
        Highlight substrings anywhere inside words.

        Example:
            pattern: "onnected"
            text: "Connected", "Disconnected"
            → only "onnected" is highlighted
        """
        for word, scope in words.items():
            pattern = re.escape(word)

            regions = self.view.find_all(pattern)

            self._add_regions(f"partial_{word}", regions, scope)

    def _highlight_whole(self, words):
        """
        Highlight complete words only.

        Uses word boundaries (\b) to ensure exact matches.

        Example:
            pattern: "TODO"
            → matches "TODO"
            → does NOT match "METHOD"
        """
        for word, scope in words.items():
            pattern = r"\b" + re.escape(word) + r"\b"

            regions = self.view.find_all(pattern)

            self._add_regions(f"whole_{word}", regions, scope)

    def _highlight_regex(self, patterns):
        """
        Highlight using raw regex patterns provided by the user.

        Example:
            "\\d+" → all numbers

        Invalid regex patterns are safely skipped.
        """
        for pattern, scope in patterns.items():
            try:
                regions = self.view.find_all(pattern)
                self._add_regions(f"regex_{pattern}", regions, scope)
            except Exception:
                print(f"[WordHighlighter] Invalid regex skipped: {pattern}")

    # -------------------------
    # Region helper
    # -------------------------

    def _add_regions(self, key, regions, scope):
        """
        Adds highlight regions to the view and stores the key.

        Args:
            key (str): Unique identifier for this highlight group
            regions (list): Regions to highlight
            scope (str): Sublime scope (controls color via theme)

        Also stores the key in view settings so it can be cleared later.
        """
        self.view.add_regions(
            key,
            regions,
            scope,
            "dot",
            sublime.DRAW_SOLID_UNDERLINE
        )

        # Track region keys for reliable clearing
        keys = self.view.settings().get("word_highlighter_keys", [])
        if key not in keys:
            keys.append(key)
            self.view.settings().set("word_highlighter_keys", keys)


# ---------------------------------------------------------
# Command: Clear highlights
# ---------------------------------------------------------
class ClearWordHighlightsCommand(sublime_plugin.TextCommand):
    """
    Removes all highlights created by this plugin from the current view.
    """

    def run(self, edit):
        settings = sublime.load_settings("WordHighlighter.sublime-settings")

        _clear_regions(settings, self.view)

        sublime.status_message("✅ Highlights cleared")


# ---------------------------------------------------------
# Command: Open settings file
# ---------------------------------------------------------
class EditWordHighlightsCommand(sublime_plugin.WindowCommand):
    """
    Opens the plugin settings file in the user's Packages/User directory.

    This allows editing:
        - whole_words
        - partial_words
        - regex_patterns

    Uses real filesystem path to avoid virtual path issues.
    """

    def run(self):
        user_path = os.path.join(sublime.packages_path(), "User")

        file_path = os.path.join(user_path, "WordHighlighter.sublime-settings")

        self.window.open_file(file_path)


# ---------------------------------------------------------
# Clearing helper
# ---------------------------------------------------------
def _clear_regions(settings, view):
    """
    Removes all highlight regions previously added by the plugin.

    Uses stored region keys from view settings to ensure:
        - no stale highlights remain
        - no dependency on current settings structure

    Args:
        view: Sublime view instance
    """
    keys = view.settings().get("word_highlighter_keys", [])

    for key in keys:
        view.erase_regions(key)

    # Reset registry
    view.settings().set("word_highlighter_keys", [])