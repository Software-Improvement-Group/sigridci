# Managing the Sigrid scope configuration file separate from your repository

Script that uses the Sigrid API to retrieve and dump the Sigrid [scope configuration file](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html) for a system.
We recommend you add `sigrid.yaml` to your repository, so that it is automatically in sync with the source code and part of versions control.
However, is it possible to retrieve and/or update the scope configuration file *without* making the `sigrid.yaml` file part of your repository.

## Prerequisites

You will need the following to use this script.

- The script requires Python 3.9+.
- You will need a valid [API token](https://docs.sigrid-says.com/organization-integration/authentication-tokens.html) to access the [Sigrid REST API](https://docs.sigrid-says.com/integrations/sigrid-api-documentation.html).
- Your API token should be available to the script as the environment variable `SIGRID_CI_TOKEN`.

## Retrieving your current Sigrid scope configuration file 

Once all prerequisites are in place, you can use the script:

    ./get_sigrid_scope_file.py --customer <mycustomername> --system <mysystemname>

This will then output the Sigrid scope configuration file to `stdout`.

**Note:** This script is intended for retrieving the scope configuration file for the analysis results *currently* in Sigrid.
This script is *not* suitable for "live" editing. If you want a fast feedback loop while editing scope files, we recommend you use the [Visual Studio Code and JetBrains support for editing scope configuration files](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#editing-scope-files).

## Updating your scope configuration file

You can use [Sigrid CI](https://docs.sigrid-says.com/reference/client-script-usage.html) to update your scope configuration file.
First, create a directory that contains your `sigrid.yaml` configuration file (it is a Sigrid convention to creat a separate directory for each system, since the file is always called `sigrid.yaml`).
Once all prerequisites are in place, you can use following command:

    git clone https://github.com/Software-Improvement-Group/sigridci.git sigridci-client

    ./sigridci-client/sigridci/sigridci.py \
      --customer <mycustomername> \
      --system <mysystemname> \
      --source <dir> \
      --subsystem scopefile \
      --publishonly

Where `<dir>` is the directory containing your `sigrid.yaml` file. Running this command will do the following:

- Validate your scope configuration file, and report errors when validation fails.
- Publish your scope configuration file to Sigrid *without* publishing source code.
- Trigger a new analysis of your system.

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
