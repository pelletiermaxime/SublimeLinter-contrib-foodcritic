#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Maxime Pelletier
# Copyright (c) 2014
#
# License: MIT
#

"""This module exports the Foodcritic plugin class."""

from os import path
from SublimeLinter.lint import RubyLinter, util, persist


class Foodcritic(RubyLinter):

    """Provides an interface to foodcritic."""

    syntax = 'ruby'
    cmd = 'foodcritic @'
    executable = None
    regex = r'(?P<message>FC\d+: .+): (?P<file>.+):(?P<line>.+)'
    multiline = False
    line_col_base = (1, 1)
    tempfile_suffix = None
    error_stream = util.STREAM_BOTH
    selectors = {}
    word_re = None
    defaults = {}
    inline_settings = None
    inline_overrides = None
    comment_re = r'\s*#'

    excluded_files = ["Berksfile", "Rakefile", "Gemfile"]

    def __init__(self, view, syntax):
        """Override the init to add the has_metadata_rb condition."""

        super(RubyLinter, self).__init__(view, syntax)

        self.has_metadata_rb = self.get_metadata_rb()

    def lint(self, hit_time):
        """Check RubyLinter options then run lint."""

        curr_file = path.basename(self.filename)
        if curr_file in self.excluded_files:
            self.disabled = True

        if not self.has_metadata_rb:
            self.disabled = True

        super(RubyLinter, self).lint(hit_time)

    def get_cmd(self):
        """Add condition before calling foodcritic."""

        cmd = super(RubyLinter, self).get_cmd()

        # Do nothing for unsaved files
        if self.view.is_dirty():
            persist.debug("foodcritic: Can't handle unsaved files, skipping")
            return False

        return cmd

    def get_metadata_rb(self):
        """Get the path to the metadata.rb file for the current file."""

        curr_file = self.view.file_name()

        if curr_file:
            cwd = path.dirname(curr_file)

            if cwd:
                return self.find_metadata_rb(cwd)

        return False

    def find_metadata_rb(self, cwd):
        """
        Search parent directories for metadata.rb.

        Starting at the current working directory. Go up one directory
        at a time checking if that directory contains a metadata.rb
        file. If it does, return that directory.
        """

        name = 'metadata.rb'
        metadata_path = path.normpath(path.join(cwd, name))

        if path.isfile(metadata_path):
            return True

        parent = path.normpath(path.join(cwd, '../'))

        if parent == '/' or parent == cwd:
            return False

        return self.find_metadata_rb(parent)
