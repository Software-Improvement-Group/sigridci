# Group-level tokens

**Upcoming:** group-level tokens will be available from **2 January 2027**. A group-level token is an authentication token that belongs to a [system group](system-groups.md) instead of to a person. Use it for automation that should keep working regardless of who set it up: Sigrid CI in your pipelines, onboarding new systems, and your own scripts using the Sigrid API. *The documentation in this section is preliminary, intended for facilitating preparation prior to release of this feature, and may change before release.*
{: .attention }

## Personal tokens versus group-level tokens

|  | **Personal token** | **Group-level token** |
| --- | --- | --- |
| Belongs to | The user who created it | A system group |
| Access | The access of that user, as configured through their roles in system groups | The group it was created for. Tokens have associated roles, so the exact permissions depend on the role that is associated to the token. |
| If the creator leaves | Stops working | Keeps working |
| Managed by | The creator | The Admins and Owners of the group |
| Best for | Personal scripts and experiments | Pipelines, shared automation |

Personal tokens stay available. They follow the access of their user: if the user's access changes, so does what the token can reach. Only the Admin role is portfolio-wide; all other roles are tied to system groups. See [authentication tokens](authentication-tokens.md) for personal tokens.

## Who can create group-level tokens

Admins and Owners of the group. Contributors and Viewers cannot.

## Create a group-level token

1. Go to **Portfolio settings > Structure and access** and open the system group you want to create a token for.
2. Expand the [Access tokens] section and choose [Grant access].
3. Enter a name that describes what the token is used for.
4. Choose an expiry date. The expiration date can be at most one year after the token creation date. If no date is selected, the expiry date will be set to the maximum of one year.
5. Choose [Create].

Sigrid shows the created token **once**. Copy it and store it securely, for example in your CI system's secret store. If you lose it, you cannot retrieve it. Create a new token instead. Sigrid stores only a hashed version of the token and never writes the token to its logs.

<!-- TODO: add a screenshot of the Grant access feature. -->

## What a group-level token can access

The token can access the group it was created for, including all groups and systems below it. Group-level tokens have an associated role, so the exact permissions depend on the role that was configured for the group-level token. A token never gets more access than the group scope it was created with. This stays true even if the creator's own access changes later. A token created on the **portfolio** has access to the entire portfolio. Treat these tokens with extra care, and prefer a token on the smallest group that fits the purpose.

## Using a group-level token

Use a group-level token wherever you would use a personal token, such as in Sigrid CI and the Sigrid REST API. To onboard new systems into the group, see [uploading your source code](upload-instructions.md).

## Manage and revoke tokens

The [Access tokens] section of a group lists the tokens of that group.

- **Revoke:** choose [x] on the right side within a token row to revoke it. It stops working immediately.
- **Expiry:** tokens stop working on their expiry date.
- **If the creator leaves:** nothing happens to the token. Any Admin or Owner of the group can manage or revoke it.
- **If the group is deleted:** this can currently not be done until tokens have been removed from the group first.

## Good practice

- Create one token per purpose (for example one per pipeline), so you can revoke one without affecting others.
- Set the shortest expiry that is practical, and rotate tokens before they expire.
- Never commit tokens to source code.
