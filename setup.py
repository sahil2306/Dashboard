from setuptools import find_packages,setup

setup(
    name='timmins',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'run-app = timmins:execute',
        ]
    }
)
