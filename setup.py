from setuptools import setup

setup(
    name='ascended_tracking',
    version='0.0.1',
    description='Companion app for tracking and uploading sessions to ascended-tracking.com',
    url='http://github.com/verdesmarald/ascended-tracking',
    author='James Bungard',
    author_email='jmbungard@gmail.com',
    license='MIT',
    packages=['ascended_tracking'],
    zip_safe=False,
    entry_points = {
        'console_scripts': ['ascended_tracking=ascended_tracking.gui:main'],
    }
)
