import setuptools
from jivi.fs import JFile,JDir
from jivi.wrapper import jvWrapper,jvWrapperSuper

@jvWrapper()
class HelperClass(jvWrapperSuper):
	def __init__(self):
		def find_settings_dir() -> JDir:
			for d in JFile(__file__).all_parent_dir_ob:
				dSetting = d.copyob.down('settings')
				if dSetting.exists:
					return dSetting
			

		self.dSettings = find_settings_dir()
		settings_fp = '.'
		if not self.dSettings:
			print("Settings dir not found")
			exit()
		else:
			settings_fp = self.dSettings.fp

		
		self.config           = JFile(self.dSettings.fp,'config.json').reader.json()
		self.long_description = JFile(self.dSettings.fp,"README.md").reader.text()
		self.version          = self.config.get('version')


	def info(self):
		self.jvlog.info('info')

Helper = HelperClass()

setuptools.setup(
    name="jivi",
    version=Helper.version,
    author="Joris Vercleyen",
    author_email="jorisvercleyen@gmail.com",
    description="Joris Vercleyen his personal library",
    long_description=Helper.long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)