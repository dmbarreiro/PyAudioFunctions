from distutils.core import setup

setuptools.setup(
        name="PyAudioFunctions",
        version="0.1.0",
        author="David Martinez Barreiro",
        author_email="5133990+dmbarreiro@users.noreply.github.com",
        description="Functions written in python for audio processing",
        long_description=open('README.txt').read(),
        url="https://github.com/dmbarreiro/PyAudioFunctions",
        license='LICENSE.txt'
	packages=['pyaudiofunctions'],
        install_requires=[
            "numpy",
            "scipy",
            "matplotlib",
        ],
	classifiers=(
		"Programming Language :: Python :: 3",
		"License :: Affero GPL",
        ),
)
