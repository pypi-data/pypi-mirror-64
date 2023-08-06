import setuptools

setuptools.setup(
    name = 'SeeMee',
    version = '0.0.1',
    url = 'https://github.com/gaming32/SeeMee',
    author = 'Gaming32',
    author_email = 'gaming32i64@gmail.com',
    license = 'License :: OSI Approved :: MIT License',
    description = "Detects which camera you're looking at",
    long_description = '',
    long_description_content_type = 'text/markdown',
    install_requires = [
        'tensorflow',
        'pygame',
        'opencv-python; sys_platform == "win32"'
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