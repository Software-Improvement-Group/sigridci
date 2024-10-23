# Sigrid objectives report

This script generates a number of charts that depict progress towards your Sigrid objectives. 

These charts are mostly about tracking progress across your portfolio, over longer periods of time. The charts are intended to be incorporated into your existing reporting structure. The data is obtained using the [Sigrid REST API](https://docs.sigrid-says.com/integrations/sigrid-api-documentation.html), which is used to determine the status and trend for your Sigrid portfolio.

## Prerequisites

You will need the following to use this script.

- The script requires Python 3.9+.
- Install the dependencies (e.g. `pip3 install -r requirements.txt --user`). We intentionally try to keep Sigrid CI self-contained, to make it as portable as possible. However, generating charts without a chart library is simply not feasible, so this script *does* require dependencies.
- You will need a valid [API token](https://docs.sigrid-says.com/organization-integration/authentication-tokens.html) to access the [Sigrid REST API](https://docs.sigrid-says.com/integrations/sigrid-api-documentation.html).
- Your API token should be available to the script as the environment variable `SIGRID_CI_TOKEN`.

## Usage

Once all prerequisites are in place, you can use the script. The following example generate a report for the Sigrid account called `example`:

    ./objectives_report.py example --out ~/Desktop
        
The script will then generate a bunch of SVG charts in the output directory. The charts in SVG format are vector-based and will look good at different resolutions, making it easier to embed them in PowerPoint slides. 
        
The script also accepts a number of *optional* arguments:

- The `--start` and `--end` options can be used to select a time period, with dates in `yyyy-mm-dd` format. The default time period for the report is one year.
- You can use the `--sigridurl` to indicate a different Sigrid instance. You can use this option if you're working
with an on-premise Sigrid environment.

The script will create the following charts:

- For your entire portfolio:
  - Overall trend chart, for each objective.
  - Trend chart with a breakdown per division, for each objective.
  - Trend chart with a breakdown per team, for each objective.
- For each division in your portfolio:
  - Radar chart with the current status.
  - Trend chart, for each objective.
- For each team in your portfolio:
  - Radar chart with the current status.
  - Trend chart, for each objective.
  
That's a lot of charts! The reason is that while every organization has reporting needs, those needs are often somewhat specific to both the organizational structure and the reporting structure. Providing this many visualizations and charts allows people to cherry-pick the charts that are the best fit for their specific situation.

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
    
    

