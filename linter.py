#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by
# Copyright (c) 2014
#
# License: MIT
#

"""This module exports the Foodcritic plugin class."""

from SublimeLinter.lint import RubyLinter, util
# from SublimeLinter.lint import Linter

class Foodcritic(RubyLinter):
# class Foodcritic(Linter):

    """Provides an interface to foodcritic."""

    syntax = 'ruby'
    cmd = 'foodcritic @'
    executable = None
    version_args = '--version'
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 1.0'
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
