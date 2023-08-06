from setuptools import setup


setup(
    name='django-shadow-tasks',
    version='0.0.6',
    author='Supl.biz',
    author_email='tech@supl.biz',
    description='Run tasks in background workers',
    url='https://git.supl.biz/web-back-tools/django-shadow-tasks',
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
