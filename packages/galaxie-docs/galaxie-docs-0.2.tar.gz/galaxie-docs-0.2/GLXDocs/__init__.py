#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Docs Team, all rights reserved

import markdown

import codecs
import os


# Inspired from: https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/
class Docs(object):
    def __init__(self):
        self.__lang = None
        self.__charset = None
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

        self.lang = 'en'
        self.charset = 'utf-8'

        self.src_dirname = None
        self.src_basename = None
        self.src_extension = None

        self.dst_dirname = None
        self.dst_basename = None
        self.dst_extension = None

        self.input_file = None
        self.output_file = None
        self.text = None
        self.body = None

    @property
    def lang(self):
        """
        A reference to HTTP_ACCEPT_LANGUAGE

        :return: Reference List HTTP_ACCEPT_LANGUAGE
        :rtype: str
        """
        return self.__lang

    @lang.setter
    def lang(self, value=None):
        """
        Set the ``lang`` property value

        Default value is ``en`` and be restore when ``lang`` is set to None

        :param value: The lang use on the html document
        :type value: str or none
        :raise TypeError: When ``lang`` value is not str type or None
        """
        if value is None:
            value = 'en'
        if type(value) != str:
            raise TypeError('"lang" value must be a str type or None')
        if self.lang != value:
            self.__lang = value

    @property
    def charset(self):
        """
        The ``charset`` property, Specify the character encoding for the HTML document

        http://webcheatsheet.com/html/character_sets_list.php

        :return: the character encoding
        :rtype: str
        """
        return self.__charset

    @charset.setter
    def charset(self, value=None):
        """
        set the ``charset`` property

        Default value is 'utf-8' and be restore when ``charset`` is set to None

        In theory, any character encoding can be used, but no browser understands all of them.
        The more widely a character encoding is used, the better the chance that a browser will understand it.

        https://www.iana.org/assignments/character-sets/character-sets.txt

        :param value: the charset use on html and markdown document
        :type value: str or none
        :raise TypeError: ``charset`` is not a str type or None
        """
        if value is None:
            value = 'utf-8'
        if type(value) != str:
            raise TypeError('"charset" value must be a str type or None')
        if self.charset != value:
            self.__charset = value

    @property
    def src_dirname(self):
        """
        The ``src_dirname`` property is use to store source directory path where is locate the input file

        :return: The source directory
        :rtype: str or None
        """
        return self.__src_base_dir

    @src_dirname.setter
    def src_dirname(self, value=None):
        """
        Set the ``src_dirname`` property value

        :param value: The location path of the source directory
        :type value: str or None
        :raise TypeError: ``src_dirname`` value is not a str type or None
        :raise FileNotFoundError: ``src_dirname`` value is path it not exist or None
        :raise NotADirectoryError: ``src_dirname`` value is path it not a directory or None
        """
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
        """
        The ``src_basename`` property is the the name of a source file without extension and without directory path

        :return: The source file basename
        :rtype: str or None
        """
        return self.__src_base_name

    @src_basename.setter
    def src_basename(self, value=None):
        """
        Set the ``src_basename`` property

        :param value: The source file basename
        :type value: str or None
        :raise TypeError: ``src_basename`` value is not a str type or None
        """
        if value is not None and type(value) != str:
            raise TypeError('"src_base_name" value must be a str type or None')
        if self.src_basename != value:
            self.__src_base_name = value

    @property
    def src_extension(self):
        """
        The ``src_extension`` property is the the suffix part

        Example: ``Hello.42`` have ``.42`` as extension

        :return: The source file extension
        :rtype: str or None
        """
        return self.__src_base_extension

    @src_extension.setter
    def src_extension(self, value=None):
        """
        Set ``src_extension`` property value.

        :param value: the extension of the source file
        :type value: str or None
        :raise TypeError: When ``src_extension`` value is not a str type or None
        """
        if value is not None and type(value) != str:
            raise TypeError('"src_base_extension" value must be a str type or None')
        if self.src_extension != value:
            self.__src_base_extension = value

    @property
    def dst_dirname(self):
        """
        The ``dst_dirname`` property is use to store destination directory path where is locate the output file

        :return: The destination directory
        :rtype: str or None
        """
        return self.__dst_base_dir

    @dst_dirname.setter
    def dst_dirname(self, value=None):
        """
        Set the ``dst_dirname`` property value

        :param value: The location path of the destination directory
        :type value: str or None
        :raise TypeError: When ``dst_dirname`` value is not a str type or None
        :raise FileNotFoundError: When ``dst_dirname`` value is path it not exist or None
        :raise NotADirectoryError: When ``dst_dirname`` value is path it not a directory or None
        """
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
        """
        The ``dst_basename`` property is the the name of a destination file without extension and without directory path

        :return: The destination file basename
        :rtype: str or None
        """
        return self.__dst_base_name

    @dst_basename.setter
    def dst_basename(self, value=None):
        """
        Set the ``dst_basename`` property

        :param value: The destination file basename
        :type value: str or None
        :raise TypeError: When ``dst_basename`` value is not a str type or None
        """
        if value is not None and type(value) != str:
            raise TypeError('"dst_base_name" value must be a str type or None')
        if self.dst_basename != value:
            self.__dst_base_name = value

    @property
    def dst_extension(self):
        """
        The ``dst_extension`` property is the the suffix part

        Example: ``Hello.42`` have ``.42`` as extension

        :return: The destination file extension
        :rtype: str or None
        """
        return self.__dst_base_extension

    @dst_extension.setter
    def dst_extension(self, value=None):
        """
        Set ``dst_extension`` property value.

        :param value: the extension of the destination file
        :type value: str or None
        :raise TypeError: When ``dst_extension`` value is not a str type or None
        """
        if value is not None and type(value) != str:
            raise TypeError('"dst_base_extension" value must be a str type or None')
        if self.dst_extension != value:
            self.__dst_base_extension = value

    @property
    def input_file(self):
        """
        The ``input_file`` property store the codecs.StreamReaderWriter object of the input file.

        :return: The input file descriptor
        :rtype: codecs.StreamReaderWriter or None
        """
        return self.__input_file

    @input_file.setter
    def input_file(self, value=None):
        """
        Set ``input_file`` property value

        :param value: The input file descriptor
        :type value: codecs.StreamReaderWriter or None
        :raise TypeError: When ``input_file`` value is not a codecs.StreamReaderWriter type or None
        """
        if value is not None and type(value) != codecs.StreamReaderWriter:
            raise TypeError('"input_file" value must be a codecs.StreamReaderWriter type or None')
        if self.input_file != value:
            self.__input_file = value

    @property
    def output_file(self):
        """
        The ``output_file`` property store the codecs.StreamReaderWriter object of the output file.

        :return: The output file descriptor
        :rtype: codecs.StreamReaderWriter
        """
        return self.__output_file

    @output_file.setter
    def output_file(self, value=None):
        """
        Set ``output_file`` property value

        :param value: The output file descriptor
        :type value: codecs.StreamReaderWriter or None
        :raise TypeError: When ``output_file`` value is not a codecs.StreamReaderWriter type or None
        """
        if value is not None and type(value) != codecs.StreamReaderWriter:
            raise TypeError('"output_file" value must be a codecs.StreamReaderWriter type or None')
        if self.output_file != value:
            self.__output_file = value

    @property
    def text(self):
        """
        The ``text`` property store the text imported from input file

        :return: input file imported text
        :rtype: str or None
        """
        return self.__text

    @text.setter
    def text(self, value=None):
        """
        Set the ``text`` property

        :param value: input file imported text
        :type value: str or None
        :raise TypeError: When ``text`` value is not a str type or None
        """
        if value is not None and type(value) != str:
            raise TypeError('"text" value must be a str type or None')
        if self.text != value:
            self.__text = value

    @property
    def body(self):
        """
        The ``body`` property store the html body part generate by MarkDown python module.

        :return: The html body part
        :rtype: str or None
        """
        return self.__html

    @body.setter
    def body(self, value=None):
        """
        Set the ``body`` property

        :param value: The html body part
        :type value: str or None
        :raise TypeError: When ``body`` value is not a str type or None
        """
        if value is not None and type(value) != str:
            raise TypeError('"text" value must be a str type or None')
        if self.body != value:
            self.__html = value

    @property
    def input_file_path(self):
        """
        The ``input_file_path`` is a read only property is return the real path of the source file.

        :return: The real path of the source file
        :rtype: os.path
        """
        return os.path.join(
            self.src_dirname,
            '{0}{1}'.format(self.src_basename, self.src_extension)
        )

    @property
    def output_file_path(self):
        """
        The ``output_file_path`` is a read only property is return the real path of the destination file.

        :return: The real path of the destination file
        :rtype: os.path
        """
        return os.path.join(
            self.dst_dirname,
            '{0}{1}'.format(self.dst_basename, self.dst_extension)
        )

    def add_src_file_name(self, value=None):
        """
        It function assist it import the source file path, basically it set
        ``src_dirname``, ``src_basename`` and ``src_extension`` automatically from a file path

        :param value: the input file path
        :type value: str or None
        :raise TypeError: When ``value`` is not a str type or None
        """
        if value is None:
            self.src_dirname = None
            self.src_basename = None
            self.src_extension = None
            return
        if type(value) != str:
            raise TypeError('"value" must be a str type or None')
        self.src_dirname = os.path.dirname(value)
        self.src_basename = os.path.splitext(os.path.basename(value))[0]
        self.src_extension = os.path.splitext(os.path.basename(value))[1]

    def add_dst_file_name(self, value):
        """
        It function assist it import the destination file path, basically it set
        ``dst_dirname``, ``dst_basename`` and ``dst_extension`` automatically from a file path

        :param value: the output file path
        :type value: str or None
        :raise TypeError: When ``value`` is not a str type or None
        """
        if value is None:
            self.dst_dirname = None
            self.dst_basename = None
            self.dst_extension = None
            return
        if type(value) != str:
            raise TypeError('"value" must be a str type or None')
        self.dst_dirname = os.path.dirname(value)
        self.dst_basename = os.path.splitext(os.path.basename(value))[0]
        self.dst_extension = os.path.splitext(os.path.basename(value))[1]

    @property
    def style(self):
        """
        The ``style`` is a read only property it return the style part of the html code

        :return: The style part of the html code
        :rtype: list
        """
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

    @property
    def html_code(self):
        """
        The ``html_code`` is a a read only property ir return the html code with everything.

        Basically it merge the result of ``body``, ``style``, ``charset`` and ``lang``.

        :return: html code
        :rtype: str
        """
        return '<!DOCTYPE html>\n' \
               '<html lang="{4}">\n' \
               '<head>\n' \
               '<meta charset="{3}">\n' \
               '<style>\n' \
               '{2}\n' \
               '</style>\n' \
               '</head>\n' \
               '<body>\n' \
               '{0}\n' \
               '</body>\n' \
               '</html>\n' \
               ''.format(self.body, '}', self.style, self.charset, self.lang)

    def md2html(self):
        """
        That function , make the job.

        Everything must be set before star it function.

        Take a look to add_src_file_name and add_dst_file_name
        """
        self.input_file = codecs.open(self.input_file_path,
                                      mode="r",
                                      encoding=self.charset
                                      )

        self.text = self.input_file.read()

        self.body = markdown.markdown(self.text,
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
                                       encoding=self.charset,
                                       errors="xmlcharrefreplace"
                                       )

        self.output_file.write(self.html_code)

        self.input_file.close()
        self.output_file.close()
