# Configuration file for the Sphinx documentation builder.

###################### Fetching images stored through GitLFS ######################
import os

# If runs on ReadTheDocs environment
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

# Hack for lacking git-lfs support ReadTheDocs
if on_rtd:
    if not os.path.exists('./git-lfs'):
        os.system('wget https://github.com/git-lfs/git-lfs/releases/download/v2.7.1/git-lfs-linux-amd64-v2.7.1.tar.gz')
        os.system('tar xvfz git-lfs-linux-amd64-v2.7.1.tar.gz')
        os.system('./git-lfs install')  # make lfs available in current repository
        os.system('./git-lfs fetch')  # download content from remote
        os.system('./git-lfs checkout')  # make local files to have the real content on them

####################################################################################

# -- Project information

project = 'UnityWiki'
copyright = '2022, JeffCube'
author = 'JeffCube'

version = '0.0.1'
release = version

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx_panels',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'
