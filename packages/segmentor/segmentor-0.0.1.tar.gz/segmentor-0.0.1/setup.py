import setuptools

with open("README.md", "r") as fh:
	long_description =fh.read()


setuptools.setup(

	name="segmentor",
	version="0.0.1",
	author="sydilkupa",
	author_email="skupa@ska.ac.za",
	description=" Packaging a segmentation project",
	long_description=long_description,
	long_description_content_type ="text/markdown",
	url="https://gitlab.com/sydilkupa/segmentation-and-classification",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
        	"Operating System :: OS Independent",
	],
	python_requires='>=3.6',

)
