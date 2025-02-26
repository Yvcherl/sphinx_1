# Configuration file for the Sphinx documentation builder.

# 项目元信息

project = 'NNEWN-DOCS' # 显示在左上角的项目名称
copyright = '2025 NNEWN INC. 保留所有权利'
author = 'Nnewn技术文档团队'
version = '0.1.0'  # 短版本号
release = '0.1.0-20250221A' # 完整版本号

#核心配置

extensions = [
  'sphinx_markdown_tables', 
  'sphinx_rtd_theme',
  'myst_parser'             # Markdown支持
]


source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = []

# 多语言支持

language = 'zh_CN'


# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'


html_static_path = ['_static']
html_css_files = ['custom.css']  # 确保这里引用了自定义的 CSS 文件

html_title = "NnewnDocs"

html_show_sourcelink = False

html_show_sphinx = False
