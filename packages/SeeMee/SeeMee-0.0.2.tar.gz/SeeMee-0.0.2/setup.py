import setuptools

setuptools.setup(
    name = 'SeeMee',
    version = '0.0.2',
    url = 'https://github.com/gaming32/SeeMee',
    author = 'Gaming32',
    author_email = 'gaming32i64@gmail.com',
    license = 'License :: OSI Approved :: MIT License',
    description = "Detects which camera you're looking at",
    long_description = 'also install one of these: https://www.lfd.uci.edu/~gohlke/pythonlibs/#videocapture',
    long_description_content_type = 'text/markdown',
    # dependency_links = [
    #     '; sys_platform == "win32"',
    # ],
    install_requires = [
        'tensorflow',
        'pygame',
    ],
    packages = [
        'SeeMee',
    ],
    ext_modules = [
        setuptools.Extension('SeeMee.base', ['SeeMee/base.c']),
    ],
    entry_points = {
        'gui_scripts': [
            'seemee = SeeMee.base:main',
        ],
    },
    zip_safe = False,
)