from setuptools import setup, find_packages

setup(
	name='protobufferize',
	version='2.0',
	license = 'GNU Affero General Public License v3.0',

	author="pierlauro",
	author_email="foss@pstux.dev",

	description='Compile protobuffers with setuptools',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',

	url='https://github.com/pierlauro/protobufferize',

	project_urls = {
		'Bug Tracker': 'https://github.com/pierlauro/protobufferize/issues',
		'Source': 'https://github.com/pierlauro/protobufferize',
	},

	classifiers = [
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7'
	],

	install_requires=[
    	"distro",
		"grpc-tools",
		"mock",
		"xmltodict",
	],

	python_requires='>=3.6',

	keywords = 'protocolbuffer proto protobuf grpc setuptools protobufferize',

	packages = find_packages(),

	py_modules=['protobufferize'],
	entry_points = {
		"distutils.commands": [
			"protobufferize = protobufferize:CompileProtoBuffers",
		],
	}
)
