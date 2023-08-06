#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Docs Team, all rights reserved

import markdown

import codecs
import os


class Docs(object):
    def __init__(self):
        self.__src_base_dir = None
        self.__src_base_name = None
        self.__src_base_extension = None

        self.__dst_base_dir = None
        self.__dst_base_name = None
        self.__dst_base_extension = None

        self.__input_file = None
        self.__output_file = None
        self.__text = None
        self.__html = None

        self.src_dirname = None
        self.src_basename = None
        self.src_extension = None

        self.dst_dirname = None
        self.dst_basename = None
        self.dst_extension = None

        self.input_file = None
        self.output_file = None
        self.text = None
        self.html = None

    @property
    def src_dirname(self):
        return self.__src_base_dir

    @src_dirname.setter
    def src_dirname(self, value=None):
        if value is not None and type(value) != str:
            raise TypeError('"src_base_dir" value must be a str type or None')
        if value is not None and not os.path.exists(os.path.realpath(value)):
            raise FileNotFoundError('"src_base_dir" path do not exist')
        if value is not None and not os.path.isdir(os.path.realpath(value)):
            raise NotADirectoryError('"src_base_dir" is not a directory')

        if self.src_dirname != value:
            self.__src_base_dir = value

    @property
    def src_basename(self):
        return self.__src_base_name

    @src_basename.setter
    def src_basename(self, value=None):
        if value is not None and type(value) != str:
            raise TypeError('"src_base_name" value must be a str type or None')
        if self.src_basename != value:
            self.__src_base_name = value

    @property
    def src_extension(self):
        return self.__src_base_extension

    @src_extension.setter
    def src_extension(self, value=None):
        if value is not None and type(value) != str:
            raise TypeError('"src_base_extension" value must be a str type or None')
        if self.src_extension != value:
            self.__src_base_extension = value

    @property
    def dst_dirname(self):
        return self.__dst_base_dir

    @dst_dirname.setter
    def dst_dirname(self, value=None):
        if value is not None and type(value) != str:
            raise TypeError('"dst_base_dir" value must be a str type or None')
        if value is not None and not os.path.exists(os.path.realpath(value)):
            raise FileNotFoundError('"dst_base_dir" path do not exist')
        if value is not None and not os.path.isdir(os.path.realpath(value)):
            raise NotADirectoryError('"dst_base_dir" is not a directory')
        if self.dst_dirname != value:
            self.__dst_base_dir = value

    @property
    def dst_basename(self):
        return self.__dst_base_name

    @dst_basename.setter
    def dst_basename(self, value=None):
        if value is not None and type(value) != str:
            raise TypeError('"dst_base_name" value must be a str type or None')
        if self.dst_basename != value:
            self.__dst_base_name = value

    @property
    def dst_extension(self):
        return self.__dst_base_extension

    @dst_extension.setter
    def dst_extension(self, value=None):
        if value is not None and type(value) != str:
            raise TypeError('"dst_base_extension" value must be a str type or None')
        if self.dst_extension != value:
            self.__dst_base_extension = value

    @property
    def input_file(self):
        return self.__input_file

    @input_file.setter
    def input_file(self, value=None):
        if value is not None and type(value) != codecs.StreamReaderWriter:
            raise TypeError('"input_file" value must be a codecs.StreamReaderWriter type or None')
        if self.input_file != value:
            self.__input_file = value

    @property
    def output_file(self):
        return self.__output_file

    @output_file.setter
    def output_file(self, value=None):
        if value is not None and type(value) != codecs.StreamReaderWriter:
            raise TypeError('"output_file" value must be a codecs.StreamReaderWriter type or None')
        if self.output_file != value:
            self.__output_file = value

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value=None):
        if self.text != value:
            self.__text = value

    @property
    def html(self):
        return self.__html

    @html.setter
    def html(self, value=None):
        if self.html != value:
            self.__html = value

    @property
    def input_file_path(self):
        return os.path.join(
            self.src_dirname,
            '{0}{1}'.format(self.src_basename, self.src_extension)
        )

    @property
    def output_file_path(self):
        return os.path.join(
            self.src_dirname,
            '{0}{1}'.format(self.dst_basename, self.dst_extension)
        )

    def add_src_file_name(self, value):
        self.src_dirname = os.path.dirname(value)
        self.src_basename = os.path.splitext(os.path.basename(value))[0]
        self.src_extension = os.path.splitext(os.path.basename(value))[1]

    def add_dst_file_name(self, value):
        self.dst_dirname = os.path.dirname(value)
        self.dst_basename = os.path.splitext(os.path.basename(value))[0]
        self.dst_extension = os.path.splitext(os.path.basename(value))[1]

    @property
    def codehilite_css(self):
        css = ['body { font-family: Impact, Charcoal, sans-serif;}',
               '.hll { background-color: #ffffcc }',
               '.c { color: #408080; font-style: italic } /* Comment */',
               '.err { border: 1px solid #FF0000 } /* Error */',
               '.k { color: #008000; font-weight: bold } /* Keyword */',
               '.o { color: #666666 } /* Operator */',
               '.cm { color: #408080; font-style: italic } /* Comment.Multiline */',
               '.cp { color: #BC7A00 } /* Comment.Preproc */',
               '.c1 { color: #408080; font-style: italic } /* Comment.Single */',
               '.cs { color: #408080; font-style: italic } /* Comment.Special */',
               '.gd { color: #A00000 } /* Generic.Deleted */',
               '.ge { font-style: italic } /* Generic.Emph */',
               '.gr { color: #FF0000 } /* Generic.Error */',
               '.gh { color: #000080; font-weight: bold } /* Generic.Heading */',
               '.gi { color: #00A000 } /* Generic.Inserted */',
               '.go { color: #888888 } /* Generic.Output */',
               '.gp { color: #000080; font-weight: bold } /* Generic.Prompt */',
               '.gs { font-weight: bold } /* Generic.Strong */',
               '.gu { color: #800080; font-weight: bold } /* Generic.Subheading */',
               '.gt { color: #0044DD } /* Generic.Traceback */',
               '.kc { color: #008000; font-weight: bold } /* Keyword.Constant */',
               '.kd { color: #008000; font-weight: bold } /* Keyword.Declaration */',
               '.kn { color: #008000; font-weight: bold } /* Keyword.Namespace */',
               '.kp { color: #008000 } /* Keyword.Pseudo */',
               '.kr { color: #008000; font-weight: bold } /* Keyword.Reserved */',
               '.kt { color: #B00040 } /* Keyword.Type */',
               '.m { color: #666666 } /* Literal.Number */',
               '.s { color: #BA2121 } /* Literal.String */',
               '.na { color: #7D9029 } /* Name.Attribute */',
               '.nb { color: #008000 } /* Name.Builtin */',
               '.nc { color: #0000FF; font-weight: bold } /* Name.Class */',
               '.no { color: #880000 } /* Name.Constant */',
               '.nd { color: #AA22FF } /* Name.Decorator */',
               '.ni { color: #999999; font-weight: bold } /* Name.Entity */',
               '.ne { color: #D2413A; font-weight: bold } /* Name.Exception */',
               '.nf { color: #0000FF } /* Name.Function */',
               '.nl { color: #A0A000 } /* Name.Label */',
               '.nn { color: #0000FF; font-weight: bold } /* Name.Namespace */',
               '.nt { color: #008000; font-weight: bold } /* Name.Tag */',
               '.nv { color: #19177C } /* Name.Variable */',
               '.ow { color: #AA22FF; font-weight: bold } /* Operator.Word */',
               '.w { color: #bbbbbb } /* Text.Whitespace */',
               '.mf { color: #666666 } /* Literal.Number.Float */',
               '.mh { color: #666666 } /* Literal.Number.Hex */',
               '.mi { color: #666666 } /* Literal.Number.Integer */',
               '.mo { color: #666666 } /* Literal.Number.Oct */',
               '.sb { color: #BA2121 } /* Literal.String.Backtick */',
               '.sc { color: #BA2121 } /* Literal.String.Char */',
               '.sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */',
               '.s2 { color: #BA2121 } /* Literal.String.Double */',
               '.se { color: #BB6622; font-weight: bold } /* Literal.String.Escape */',
               '.sh { color: #BA2121 } /* Literal.String.Heredoc */',
               '.si { color: #BB6688; font-weight: bold } /* Literal.String.Interpol */',
               '.sx { color: #008000 } /* Literal.String.Other */',
               '.sr { color: #BB6688 } /* Literal.String.Regex */',
               '.s1 { color: #BA2121 } /* Literal.String.Single */',
               '.ss { color: #19177C } /* Literal.String.Symbol */',
               '.bp { color: #008000 } /* Name.Builtin.Pseudo */',
               '.vc { color: #19177C } /* Name.Variable.Class */',
               '.vg { color: #19177C } /* Name.Variable.Global */',
               '.vi { color: #19177C } /* Name.Variable.Instance */',
               '.il { color: #666666 } /* Literal.Number.Integer.Long */']

        to_return = ''
        for line in css:
            to_return = to_return + line + '\n'

        return to_return

    def html_with_body(self):
        return '<!DOCTYPE html>\n' \
               '<html lang="en">\n' \
               '<head>\n' \
               '<meta charset="utf-8">\n' \
               '<style>\n' \
               '{2}\n' \
               '</style>\n' \
               '</head>\n' \
               '<body>\n' \
               '{0}\n' \
               '</body>\n' \
               '</html>\n' \
               ''.format(self.html, '}', self.codehilite_css)

    def md2html(self):
        self.input_file = codecs.open(self.input_file_path,
                                      mode="r",
                                      encoding="utf-8"
                                      )

        self.text = self.input_file.read()

        self.html = markdown.markdown(self.text,
                                      output_format="html5",
                                      extensions=['extra',
                                                  'abbr',
                                                  'attr_list',
                                                  'def_list',
                                                  'fenced_code',
                                                  'footnotes',
                                                  'md_in_html',
                                                  'tables',
                                                  'admonition',
                                                  'codehilite',
                                                  'legacy_attrs',
                                                  'legacy_em',
                                                  'meta',
                                                  # 'nl2br',
                                                  'sane_lists',
                                                  'smarty',
                                                  'toc',
                                                  'wikilinks'
                                                  ])

        self.output_file = codecs.open(self.output_file_path,
                                       "w",
                                       encoding="utf-8",
                                       errors="xmlcharrefreplace"
                                       )

        self.output_file.write(self.html_with_body())

        self.input_file.close()
        self.output_file.close()

