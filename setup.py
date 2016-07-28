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
            "fake_plugin = gaia_plugin_demo.fake_plugin",
            "another_fake_plugin = gaia_plugin_demo.another_fake_plugin"
        ]
  }
)
