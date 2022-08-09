# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.abspath("../../src"))

# -- Project information -----------------------------------------------------

project = "mofdscribe"
copyright = f"{date.today().year}, Kevin M. Jablonka"
author = "Kevin M. Jablonka"

# The full version, including alpha/beta/rc tags.
release = "0.0.1-dev"

# The short X.Y version.
parsed_version = re.match(
    r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?:-(?P<release>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+(?P<build>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?",
    release,
)
version = parsed_version.expand(r"\g<major>.\g<minor>.\g<patch>")

if parsed_version.group("release"):
    tags.add("prerelease")

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# A list of prefixes that are ignored when creating the module index. (new in Sphinx 0.6)
modindex_common_prefix = ["mofdscribe."]

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinxcontrib.katex",
    "sphinx_copybutton",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosectionlabel",
    "sphinxcontrib.needs",
    "sphinx.ext.intersphinx",
    "sphinx-pydantic",
]

intersphinx_mapping = {
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "sklearn": ("https://scikit-learn.org/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
}

needs_extra_options = [
    "start_time",
    "end_time",
    "version",
    "features",
    "name",
    "task",
    "model_type",
    "reference",
    "implementation",
    "mofdscribe_version",
    "mean_squared_error",
    "mean_absolute_error",
    "r2_score",
    "max_error",
    "mean_absolute_percentage_error",
    "top_5_in_top_5",
    "top_10_in_top_10",
    "top_50_in_top_50",
    "top_100_in_top_100",
    "top_500_in_top_500",
    "references",
    "considers_geometry",
    "considers_structure_graph",
    "encodes_chemistry",
    "scalar",
    "scope",
    "session_info",
]

needs_types = [
    dict(
        directive="regressionmetrics",
        title="Regression Metrics",
        prefix="R_",
        color="#DCB239",
        style="node",
    ),
    dict(
        directive="featurizer",
        title="Featurizers",
        prefix="F_",
        color="#FFB039",
        style="node",
    ),
]

needs_id_regex = "[A-Za-z0-9 .():_]+"

autodoc_type_aliases = {"ArrayLike": "numpy.typing.ArrayLike"}

copybutton_selector = "div:not(.no-copy)>div.highlight pre"
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# generate autosummary pages
autosummary_generate = True


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


needs_table_style = "datatables"
# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    "globaltoc_collapse": False,
    "source_repository": "https://github.com/kjappelbaum/mofdscribe/",
    "source_branch": "main",
    "source_directory": "docs/source",
    # Since Furo doesn't allow us to disable dark mode, we make dark mode
    # equivalent to light mode by overriding all colors back to their light value.
    # See: https://github.com/pradyunsg/furo/issues/28
    "dark_css_variables": {
        # Taken from: https://github.com/pradyunsg/furo/blob/c682d5d3502f3fa713c909eebbf9f3afa0f469d9/src/furo/assets/styles/variables/_colors.scss
        "color-problematic": "#b30000",
        # Base Colors
        "color-foreground-primary": "black",  # for main text and headings
        "color-foreground-secondary": "#5a5c63",  # for secondary text
        "color-foreground-muted": "#646776",  # for muted text
        "color-foreground-border": "#878787",  # for content borders
        "color-background-primary": "white",  # for content
        "color-background-secondary": "#f8f9fb",  # for navigation + ToC
        "color-background-hover": "#efeff4ff",  # for navigation-item hover
        "color-background-hover--transparent": "#efeff400",
        "color-background-border": "#eeebee",  # for UI borders
        "color-background-item": "#ccc",  # for "background" items (eg: copybutton)
        # Announcements
        "color-announcement-background": "#000000dd",
        "color-announcement-text": "#eeebee",
        # Brand colors
        "color-brand-primary": "#2962ff",
        "color-brand-content": "#2a5adf",
        # Highlighted text (search)
        "color-highlighted-background": "#ddeeff",
        # GUI Labels
        "color-guilabel-background": "#ddeeff80",
        "color-guilabel-border": "#bedaf580",
        # API documentation
        "color-api-keyword": "var(--color-foreground-secondary)",
        "color-highlight-on-target": "#ffffcc",
        # Admonitions
        "color-admonition-background": "transparent",
        # Cards
        "color-card-border": "var(--color-background-secondary)",
        "color-card-background": "transparent",
        "color-card-marginals-background": "var(--color-background-hover)",
        # Code blocks
        "color-code-foreground": "black",
        "color-code-background": "#f8f9fb",
    },
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#
if os.path.exists("figures/logo.png"):
    html_logo = "figures/logo.png"

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "mofdscribedoc"

# -- Options for LaTeX output ------------------------------------------------

# latex_elements = {
#     The paper size ('letterpaper' or 'a4paper').
#
#     'papersize': 'letterpaper',
#
#     The font size ('10pt', '11pt' or '12pt').
#
#     'pointsize': '10pt',
#
#     Additional stuff for the LaTeX preamble.
#
#     'preamble': '',
#
#     Latex figure (float) alignment
#
#     'figure_align': 'htbp',
# }

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
# latex_documents = [
#     (
#         master_doc,
#         'mofdscribe.tex',
#         'mofdscribe Documentation',
#         author,
#         'manual',
#     ),
# ]

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (
        master_doc,
        "mofdscribe",
        "mofdscribe Documentation",
        [author],
        1,
    ),
]

# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "mofdscribe",
        "mofdscribe Documentation",
        author,
        "Kevin M. Jablonka",
        "Ecosystem for digital reticular chemistry",
        "Miscellaneous",
    ),
]

# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
# epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
# epub_exclude_files = ['search.html']

# -- Extension configuration -------------------------------------------------


autoclass_content = "both"

# Don't sort alphabetically, explained at:
# https://stackoverflow.com/questions/37209921/python-how-not-to-sort-sphinx-output-in-alphabetical-order
autodoc_member_order = "bysource"
