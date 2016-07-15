from setuptools import setup, find_packages

setup(
  name="MyGaiaPlugin",
  version="0.0",
  description="""Gaia plugin""",
  author="Matt",
  install_requires=["gaia>=0.0.0"],
  packages=find_packages(),
  include_package_data=True,
  entry_points={
    'gaia.plugins': [
            "fake_plugin = my_gaia_plugins.fake_plugin",
            "another_fake_plugin = my_gaia_plugins.another_fake_plugin"
        ]
  }
)
