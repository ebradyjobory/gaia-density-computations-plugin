# gaia_least_cost_plugin

This is a simple example of a Gaia plugin project.

The project at minimum should include a setup.py file containing an
'entry_points' attribute that specified the location of your plugin modules:

```
  entry_points={
    'gaia.plugins': [
            "fake_plugin = my_gaia_plugins.fake_plugin",
            "another_fake_plugin = my_gaia_plugins.another_fake_plugin"
        ]
  }
```

Optionally, your project may also include a requirements.txt file and
a 'gaia.cfg' configuration file.


For consistency, your plugin parent module's name should start with 'gaia_'.

To run this example:

  - Install the 'plugins' branch of gaia
    - git clone -b plugins https://github.com/OpenDataAnalytics/gaia.git
    - cd gaia
    - pip install -e .
    - cd ..
  - Install this repo
    - git clone https://github.com/mbertrand/gaia_least_cost_plugin.git
    - cd gaia_least_cost_plugin
    - pip install -e .
    - cd ..
  - Run the Gaia parser on the provided test.json file:
    - python gaia/gaia/parser.py gaia_least_cost_plugin/test.json

The output should be:

```
Created LeastCostIO
Value of Gaia plugin config: demo_setting
Created AnotherLeastCostIO
Created LeastCostProcess
Compute something with LeastCostProcess
Process complete.
```
