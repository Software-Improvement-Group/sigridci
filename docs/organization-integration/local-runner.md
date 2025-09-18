# Sigrid Local Runner

This documentation covers the Sigrid Local Runner, which is only used when you are part of an
[IT Due Diligence](https://www.softwareimprovementgroup.com/it-due-diligence/) where your source code needs to
remain on-premise. You do not need the Local Runner outside of IT Due Diligences. 
{: .attention }

The Local Runner does the following:

- Analyze your source code. This is done locally, so the source code will never leave your environment.
- Publish the analysis results to Sigrid. Your source code is *not* published to Sigrid.

## Prerequisites

Before you can start using the Local Runner, you need the following:

- You need to install [Docker](https://www.docker.com). In most cases, the most convenient to run Docker locally
  is by installing [Docker Desktop](https://docs.docker.com/desktop/). Docker Desktop supports Windows, Mac, and Linux.
- A Sigrid license file. This is provided to you by SIG.
- Download and install the Local Runner. A download link is provided to you by SIG. The Local Runner
  supports Windows, Mac, and Linux.
- You will need local access to your source code that you want to analyze using the Local Runner. 

## Using the Local Runner

When you start the Local Runner, you'll see something that looks like this:

<img src="../images/local-runner/welcome.png" width="500" />

The Local Runner checks if Docker is running. If you followed the [prerequisites](#prerequisites), you should see
a green box confirming this:

<img src="../images/local-runner/docker.png" width="300" />

You can now provide the Local Runner with the license file and the source code directory.

<img src="../images/local-runner/input.png" width="300" />

The license file is only valid for a limited time. If you see an error message that your license file has
expired, contact SIG to request a new one.

If you're not seeing any red error messages, you're good to go. You can now click the button to start analyzing
your source code. This might take a while, depending on how large your source code is. 

<img src="../images/local-runner/progress.png" width="400" />

Optionally, you can click "show process output" to see the log output. This is purely for information purposes.

After the analysis has completed, you will see the following confirmation message. This indicates the Local Runner
has successfully completed its analysis, and has published the analysis results to Sigrid. That means you're done!

If your analysis results in an error, [contact SIG](#contact-and-support) so we can try to help you out.

If you made a mistake, you can use the Local Runner multiple times. Whenever you use the Local Runner, the new
analysis results will simply replace the old ones. You can continue to use the Local Runner for as long as your
Sigrid license file is valid.

## Supported technologies

The Local Runner is able to analyze over 250 different technologies. For a full overview, see the 
[list of supported technologies](../reference/technology-support.md#list-of-supported-technologies)
and filter the table by "Local Runner".

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or
issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact 
us by phone at +31 20 314 0953.
