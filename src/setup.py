from setuptools import setup, find_namespace_packages
import sys

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 7)

# Check the current python version
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write('MDDE requires Python {0[0]}.{0[1]} or higher. You have Python {1[0]}.{1[1]}.'
                     .format(REQUIRED_PYTHON, CURRENT_PYTHON))
    sys.exit(1)

setup(
    name='mdde.integration.maac',
    version='0.1',
    description='Multi-agent Data Distribution Environment: Actor-Attention-Critic for Multi-Agent Reinforcement '
                'Learning',

    author='Andrey Kharitonov',
    author_email='andrey.kharitonov@ovgu.de',

    license='MIT Licence',
    packages=find_namespace_packages(include=['mdde.integration.maac.*'], exclude=['mdde.test.*']),

    installs_requires=['gym==0.9.4',
                       'tensorboardx==1.9',
                       'tensorboard==2.0.0',
                       'seaborn==0.9.0'],
    zip_safe=False,
)
