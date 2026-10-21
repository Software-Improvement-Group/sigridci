Integrating Sigrid CI with Gerrit
=================================

## Required environment variables

| Name                  | Description                                                            |
|-----------------------|------------------------------------------------------------------------|
| `GERRIT_BASE_URL`     | The base URL of the Gerrit server, starting with `https://`.           |
| `GERRIT_REPO`         | The name of the (Git) repository as used within Gerrit.                |
| `GERRIT_BRANCH`       | The branch name of the (Git) repository as used within Gerrit.         |
| `GERRIT_CHANGE_ID`    | The Gerrit change ID for which you are posting feedback.               |
| `GERRIT_USER` [1]     | Credentials for the Gerrit user that will post on behalf of Sigrid CI. |
| `GERRIT_PASSWORD` [1] | Credentials for the Gerrit user that will post on behalf of Sigrid CI. |

[1] Sigrid CI cannot use the newer token-based authentication that was introduced in Gerrit 3.13, to retain
backward compatibility with older Gerrit versions.

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues
you may have after reading this documentation or when using Sigrid.
