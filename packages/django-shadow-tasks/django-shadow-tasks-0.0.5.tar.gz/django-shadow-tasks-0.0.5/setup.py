from setuptools import setup


setup(
    name='django-shadow-tasks',
    version='0.0.5',
    author='Andrei Loskutov',
    author_email='andrewloscutov@gmail.com',
    description='Run tasks in background workers',
    url='https://github.com/suplbiz/django-shadow-tasks',
    entry_points={'console_scripts': [
        'shadow-tasks-consumer = '
        'shadow_tasks.consuming.cli_start:execute_from_command_line',
    ]},
    packages=[
        'shadow_tasks',
        'shadow_tasks.consuming',
        'shadow_tasks.publishing',
    ],
    install_requires=['django>=2.1', 'pika==1.1.0'],
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
)
