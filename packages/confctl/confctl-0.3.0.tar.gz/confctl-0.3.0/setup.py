# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['confctl']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0', 'jinja2>=2.11.1,<3.0.0']

entry_points = \
{'console_scripts': ['confctl = confctl.cli:main']}

setup_kwargs = {
    'name': 'confctl',
    'version': '0.3.0',
    'description': 'Simple configuration management',
    'long_description': '<p align="center">\n    <a href="https://pypi.org/project/confctl/">\n        <img src="https://badge.fury.io/py/confctl.svg" alt="Package version">\n    </a>\n</p>\n\n# confctl\n\nHelps to organize you configs and how they generated, installed.\n\n```sh\n$ confctl configure i3 rofi\n```\n\n![Example execution](https://github.com/miphreal/python-rofi-menu/raw/master/docs/example_output.png)\n\n\n```sh\n$ confctl --help\nUsage:\n  confctl configure [self] [<configuration>...]\n                   [--target=<target-system>|--nb|--pc|--srv]\n                   [--flags=<list-of-flags>] [--machine-id=<unique-node-id>]\n\nCommands:\n  configure       Cofiugre software on the host system (e.g. i3)\n\nOptions:\n  -h --help       Show this help\n  -v --version    Show version\n\nOptions for `confctl configure`:\n  --target=<target>  Current system type (nb, pc, srv)\n  --machine-id=<node-id>  Current system unique id (e.g. work.pc)\n  --flags=<flags>    A comma separated list of extra flags\n  ```\n\n## Getting started\n\n1. Create a virtual env specially for your configuration (use any tool you prefer for managing/creating python virtual envs)\n\n```sh\n$ pyenv virtualenv 3.8.2 confctl\n```\n\n2. Activate & install `confctl`\n```sh\n$ pyenv shell confctl\n$ pip install confctl\n$ confctl configure self --target=laptop --machine-id=dellxps\n```\n\nNote, we pass `--target` to specify the "type" of device and `--machine-id` to identify current device.\nThis info will be remembered in `~/.config/confctl/config` file. It might be usefull to understand\nduring configuration what it\'s applied to (e.g. to render differend configs for pc and laptop as\nthey might have differnt parameters).\n\n3. Create a couple configs\n\nGo to `~/.config/confctl/user-configs` and create there a folder with `__init__.py` inside.\n`__init__.py` must define `Configuration` class (inherited from `Base` which provides basic utils to run sh commands, render templates, etc).\n\n```py\n# ~/.config/confctl/user-configs/console/__init__.py\nfrom confctl import Base, Param\n\n\nclass Configuration(Base):\n    HOME = Param.PATH("~")\n    TARGET = Param()\n    YJ_PROJECT_ROOT = Param.PATH("~/Develop/yunojuno/platform")\n    tmux_plugin_manager_dir = Param.PATH("~/.tmux/plugins/tpm")\n    tmp_repo = "https://github.com/tmux-plugins/tpm"\n    fonts_repo = "https://github.com/ryanoasis/nerd-fonts"\n    prezto_repo = "https://github.com/sorin-ionescu/prezto"\n\n    def configure(self):\n        # patched fonts\n        fonts_dir = self.CACHE_DIR / "fonts"\n        if not (fonts_dir / ".git").exists():\n            self.run_sh(f"git clone --depth 1 {self.fonts_repo} {fonts_dir}")\n            self.run_sh(f\'bash {fonts_dir / "install.sh"}\')\n\n        # tmux\n        self.ensure_folders(self.tmux_plugin_manager_dir)\n        if not (self.tmux_plugin_manager_dir / ".git").exists():\n            self.run_sh(f"git clone {self.tmp_repo} {self.tmux_plugin_manager_dir}")\n        self.template("tmux.conf.j2", symlink=self.HOME / ".tmux.conf")\n\n        # prezto\n        prezto_dir = self.HOME / ".zprezto"\n        if not (prezto_dir / ".git").exists():\n            self.run_sh(f\'git clone --recursive {self.prezto_repo} "{prezto_dir}"\')\n\n        if not (self.HOME / ".zpreztorc").exists():\n            init_zprezto = """\nsetopt EXTENDED_GLOB\nfor rcfile in "${ZDOTDIR:-$HOME}"/.zprezto/runcoms/^README.md(.N); do\nln -s "$rcfile" "${ZDOTDIR:-$HOME}/.${rcfile:t}"\ndone\n"""\n            self.warning(\n                f"You may need to manually setup `zprezto`: \\n{init_zprezto}"\n            )\n```\n\nThe folder with configuration can contain any assets/templates used during configuration.\nIn this example, there should be `tmux.conf.j2`.\n\n\n4. Then you simply run this configuration\n\n```sh\n$ confctl configure console\n```\n\nOr just\n\n```sh\n$ confctl configure\n```\nwhich will apply all defined configurations.\n\n## API\n\nTBD\n\n\n## Internals\n\nTBD\n\n',
    'author': 'miphreal',
    'author_email': 'miphreal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/miphreal/confctl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
