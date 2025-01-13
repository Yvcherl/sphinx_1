# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'nnewn'
copyright = '2024, nnewn-css'
author = 'nnewn-css'
release = 'test1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['recommonmark','sphinx_markdown_tables',  'sphinx_rtd_theme']
source_suffix = ['.rst', '.md']

templates_path = ['_templates']
exclude_patterns = []

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'


html_static_path = ['_static']
html_css_files = [
    '_static/custom.css'  # 确保这里引用了自定义的 CSS 文件
]

html_title = "嵌入式AI应用开发实战指南"

html_show_sourcelink = False


