from __future__ import print_function

import sys
import os
import io

try: 
    from setuptools import setup, find_packages
    from setuptools.command.install import install as _install
except ImportError: 
    from distutils.core import setup
    from distutils.command.install import install as _install
    def find_packages():
        return ['ugali','ugali.analysis','ugali.config','ugali.observation',
                'ugali.preprocess','ugali.simulation','ugali.candidate',
                'ugali.utils']

import distutils.cmd

import versioneer
VERSION = versioneer.get_version()

NAME = 'ugali'
HERE = os.path.abspath(os.path.dirname(__file__))
URL = 'https://github.com/DarkEnergySurvey/ugali'
DESC = "Ultra-faint galaxy likelihood toolkit."
LONG_DESC = "See %s"%URL
CLASSIFIERS = """\
Development Status :: 2 - Pre-Alpha
Intended Audience :: Science/Research
Intended Audience :: Developers
Programming Language :: Python
Natural Language :: English
Topic :: Scientific/Engineering
"""

ISOCHRONES = URL+'/releases/download/v1.6.3/ugali-isochrones-v1.6.3.tar.gz'
ISOSIZE = "~100MB" 
# Could find file size dynamically, but it's a bit slow...
# int(urllib.urlopen(ISOCHRONES).info().getheaders("Content-Length")[0])/1024**2
UGALIDIR = os.getenv("UGALIDIR","$HOME/.ugali")

class ProgressFileIO(io.FileIO):
    def __init__(self, path, *args, **kwargs):
        self._total_size = os.path.getsize(path)
        io.FileIO.__init__(self, path, *args, **kwargs)

    def read(self, size):
        count = self.tell()/size
        self.progress_bar(count,size,self._total_size)
        return io.FileIO.read(self, size)

    @staticmethod
    def progress_bar(count, block_size, total_size):
        block = 100*block_size/float(total_size)
        progress = count*block
        if progress % 1 < 1.01*block:
            msg = '\r[{:51}] ({:d}%)'.format(int(progress//2)*'='+'>',int(progress))
            sys.stdout.write(msg)
            sys.stdout.flush()

class IsochroneCommand(distutils.cmd.Command):
    """ Command for downloading isochrone files """
    description = "install isochrone files"
    user_options = [
        ('isochrones-path=',None,
         'path to install isochrones (default: %s)'%UGALIDIR),
        ('force','f',
         'force installation (overwrite any existing files)')
        ]
    # Should the default path be set by install 'prefix'?
    boolean_options = ['force']

    def initialize_options(self):
        self.isochrones_path = os.path.expandvars(UGALIDIR)
        self.force = False

    def finalize_options(self):
        pass

    def install_isochrones(self):
        import urllib
        import tarfile

        print("installing isochrones")
        if not os.path.exists(self.isochrones_path):
            print("creating %s"%self.isochrones_path)
            os.makedirs(self.isochrones_path)
            #self.mkpath(self.isochrones_path)

        os.chdir(self.isochrones_path)

        url = ISOCHRONES
        tarball = os.path.basename(url)

        print("downloading %s..."%url)
        urllib.urlretrieve(url, tarball, reporthook=ProgressFileIO.progress_bar)
        print('')

        print("extracting %s..."%tarball)
        with tarfile.open(fileobj=ProgressFileIO(tarball),mode='r:gz') as tar:
            tar.extractall()
            tar.close()
            print('')

        print("removing %s"%tarball)
        os.remove(tarball)

    def run(self):
        if self.dry_run:
            print("skipping isochrone install")
            return

        if os.path.exists(os.path.join(self.isochrones_path,'isochrones')):
            if self.force:
                print("overwriting isochrone directory")
            else:
                print("isochrone directory found; skipping installation")
                return
       
        self.install_isochrones()

class install(_install):
    """ 
    Subclass the setuptools 'install' class to add isochrone options.
    """

    user_options = _install.user_options + [
        ('isochrones',None,"install isochrone files (%s)"%ISOSIZE),
        ('no-isochrones',None,"don't install isochrone files [default]"),
        ('isochrones-path=',None,"isochrone installation path [default: %s]"%UGALIDIR)
    ]
    boolean_options = _install.boolean_options + ['isochrones','no-isochrones']

    def initialize_options(self):
        _install.initialize_options(self)
        self.isochrones = None
        self.no_isochrones = None
        self.isochrones_path = None

    def finalize_options(self):
        _install.finalize_options(self)
        if self.no_isochrones is False: self.isochrones = False
        if self.isochrones is False: self.no_isochrones = False

    def run(self):
        # run superclass install
        _install.run(self)

        # Could ask user whether they want to install isochrones, but 
        # pip filters sys.stdout, so the prompt never gets sent:
        # https://github.com/pypa/pip/issues/2732#issuecomment-97119093

        if self.isochrones: 
            self.install_isochrones()
        else:
            print("skipping isochrone install")
            
    def install_isochrones(self):
        """
        Call to isochrone install command:
        http://stackoverflow.com/a/24353921/4075339
        """
        if self.isochrones_path:
            cmd_obj = self.distribution.get_command_obj('isochrones')
            cmd_obj.isochrones_path = self.isochrones_path

        cmd_obj = self.distribution.get_command_obj('isochrones')
        cmd_obj.force = self.force

        self.run_command('isochrones')
            
CMDCLASS = versioneer.get_cmdclass()
CMDCLASS['isochrones'] = IsochroneCommand
CMDCLASS['install'] = install

setup(
    name=NAME,
    version=VERSION,
    cmdclass=CMDCLASS,
    url=URL,
    author='Keith Bechtol & Alex Drlica-Wagner',
    author_email='bechtol@kicp.uchicago.edu, kadrlica@fnal.gov',
    scripts = [],
    install_requires=[
        'python >= 2.7.0',
        'numpy >= 1.9.0',
        'scipy >= 0.14.0',
        'healpy >= 1.6.0',
        'pyfits >= 3.1',
        'emcee >= 2.1.0',
        'corner >= 1.0.0',
        'pyyaml >= 3.10',
    ],
    packages=find_packages(),
    description=DESC,
    long_description=LONG_DESC,
    platforms='any',
    classifiers = [_f for _f in CLASSIFIERS.split('\n') if _f]
)
