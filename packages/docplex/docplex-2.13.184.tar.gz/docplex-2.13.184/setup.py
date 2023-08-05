import os
import re
from distutils.core import setup
import sys

required = ['requests',
            'six']
if ((sys.version_info[0]) < 3) or \
   ((sys.version_info[0] == 3) and (sys.version_info[1] < 2)):
    required.append('futures')

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    try:
        with open(os.path.join(HERE, *parts)) as f:
            return f.read()
    except:
        return None

readme = read('README.rst')
if readme is None:
    readme = 'DOcplex 2.13'

changelog = str(read('CHANGELOG.rst'))
if changelog is None:
    changelog = ''

ss = str(readme) + str(changelog)

setup(
    name='docplex',
    packages=['docplex',
               'docplex.cp',
               'docplex.cp.solver',
               'docplex.cp.cpo',
               'docplex.cp.fzn',
               'docplex.cp.lp',
               'docplex.mp',
               'docplex.mp.callbacks',
               'docplex.mp.internal',
               'docplex.mp.params',
               'docplex.mp.sktrans',
               'docplex.mp.sparktrans',
               'docplex.mp.worker',
               'docplex.util',
               'docplex.util.dods',
               'docplex.util.ws'],
    version = '2.13.184',  # replaced at build time
    description = 'The IBM Decision Optimization CPLEX Modeling for Python',
    author = 'The IBM Decision Optimization on Cloud team',
    author_email = 'dofeedback@wwpdl.vnet.ibm.com',
    long_description='%s\n' % ss,
    long_description_content_type='text/x-rst',
    url = 'https://onboarding-oaas.docloud.ibmcloud.com/software/analytics/docloud/',
    keywords = ['docloud', 'optimization', 'cplex', 'cpo'],
    license = 'Apache 2.0',
    install_requires=required,
    classifiers = ["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Developers",
                   "Intended Audience :: Information Technology",
                   "Intended Audience :: Science/Research",
                   "Operating System :: Unix",
                   "Operating System :: MacOS",
                   "Operating System :: Microsoft",
                   "Operating System :: OS Independent",
                   "Topic :: Scientific/Engineering",
                   "Topic :: Scientific/Engineering :: Mathematics",
                   "Topic :: Software Development :: Libraries",
                   "Topic :: System",
                   "Topic :: Other/Nonlisted Topic",
                   "License :: OSI Approved :: Apache Software License",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 2.7",
                   "Programming Language :: Python :: 3.6",
                   "Programming Language :: Python :: 3.7"
                   ],
)

print("** The documentation can be found here: https://github.com/IBMDecisionOptimization/docplex-doc")
print("** The examples can be found here: https://github.com/IBMDecisionOptimization/docplex-examples")
