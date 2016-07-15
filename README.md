# gaia_plugin_demo

To run an example:

  - Install the 'plugins' branch of gaia
    - git clone -b plugins https://github.com/OpenDataAnalytics/gaia.git
    - cd gaia
    - pip install -e .
    - cd ..
  - Install this repo
    - git clone https://github.com/mbertrand/gaia_plugin_demo.git
    - cd gaia_plugin_demo
    - pip install -e .
    - cd ..
  - Run the Gaia parser on the provided test.json file:
    - python gaia/gaia/parser.py gaia_plugin_demo/test.json

The output should be:

```
Created FakeIO
Created AnotherFakeIO
Created FakeProcess
Compute something with FakeProcess
Process complete.
```
