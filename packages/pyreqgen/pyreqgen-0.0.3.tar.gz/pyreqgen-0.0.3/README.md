# Python Requirements Tool

This package compiles and puts all of the required python packages into a single requirements.txt file.

## Quick Start
#### Usage
ReqParser is a module which contains static functions for generating the requirements.txt from
python source code.

```
from pyreqgen import ReqParser

root_dir_of_project = "/location/to/project"

ReqParser.run(root_dir_of_project, write_o=True, alpha=True)
```
## ReqParser
The run method is the main entry point to generate the requirements.txt.
It takes a mandatory argument the location of the root directory of the project as a string.
Optional arguments arguments are if you want to write out the required modules to a requirements.txt
in the function.  If not then it will return with a set of strings the module names.

The alpha option is set True if you want the modules sorted alphanumerically.


### Contributing
Please submit an issue or pull request if you have suggestions on how to make this project better.