from setuptools import setup

setup(
    name="zzzz",
    author="suiting",
    author_email="yukater@outlook.com",
    version="0.0.3",
    description='print("zzzz")',
    install_requests=[],
    py_modules=['zzzz'],
    entry_points={"console_scripts": ["zzzz=zzzz:main"]},
)
