# Get Sigrid scope configuration file

Script that uses the Sigrid API to retrieve and dump the Sigrid [scope configuration file](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html) for a system. 
It is recommended to store the scope configuration file in your repository, named `sigrid.yaml`, and have it under version control. 
However, you can use this example to retrieve the scope file in scenarios where it is not possible to store the scope configuration file in the repository, but you still want to retrieve it.

**Note:** This script is intended for retrieving the scope configuration file for the analysis results *currently* in Sigrid.
This script is *not* suitable for "live" editing. If you want a fast feedback loop while editing scope files, we recommend you use the [Visual Studio Code and JetBrains support for editing scope configuration files](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#editing-scope-files).

## Prerequisites

You will need the following to use this script.

- The script requires Python 3.9+.
- You will need a valid [API token](https://docs.sigrid-says.com/organization-integration/authentication-tokens.html) to access the [Sigrid REST API](https://docs.sigrid-says.com/integrations/sigrid-api-documentation.html).
- Your API token should be available to the script as the environment variable `SIGRID_CI_TOKEN`.

## Usage

Once all prerequisites are in place, you can use the script:

    ./get_sigrid_scope_file.py --customer <mycustomername> --system <mysystemname>

This will then output the Sigrid scope configuration file to `stdout`. 

## License

Copyright Software Improvement Group

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
