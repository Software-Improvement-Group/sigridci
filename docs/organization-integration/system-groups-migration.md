# Migrating to system groups

**Upcoming:** system groups will replace the current way of managing access on **30 November 2026**. **This may require action from your side. Please prepare using this page.** With [system groups](system-groups.md), access in Sigrid is no longer tied to individual systems, but to system groups. This page explains what changes for your existing users and roles, and how to prepare.
{: .attention }

## What changes

- At the switch, all your systems sit directly under your portfolio, and existing access carries over: users keep the access they have today. You can then create system groups and move systems into them whenever you are ready.
- User roles are renamed, and their permissions are slightly adjusted to fit in with the new system group features.
- A new Viewer user role is introduced. No users are automatically migrated to this role; this role can be manually set.
- The API endpoints for granting system access directly to individual users and user groups will stop working, as access is now set via system groups. See [System groups API availability](../integrations/sigrid-api-documentation.md#system-groups-api-availability) for the adjusted and new endpoints.

| **Today** | **After the switch** |
| --- | --- |
| Normal user | **Contributor** |
| Maintainer | **Owner** |
| Administrator | **Administrator** (unchanged, portfolio-wide) |
| (does not exist) | **Viewer**: new read-only role |
| One role per user, for the whole portfolio | A user can have a **different role in different system groups** |
| Access granted per system, or in bulk using team, division and supplier metadata | Access granted per system group (and sticky: new systems in a group are accessible automatically) |
| Authorization groups carry system access | **User groups** are collections of users. A user group (or an individual user) is given a role on a system group |

See [roles and access](system-groups-access.md) for the full description.

## How to prepare

1. **Design your hierarchy.** Decide how you want to group your systems, for example by division and team. Remember: up to 6 levels, and group and system names must all be unique across the portfolio.
2. **Decide who needs which role** on which group. Roles cascade down and cannot be lowered further down, so assign them as high in the hierarchy as is appropriate.
3. **Check your automation.** Personal tokens follow the access of their user, so check which of your pipelines and scripts rely on them. Consider [group-level tokens](authentication-tokens-group.md) for automation that should not depend on one person.
4. **Check your API usage.** Scripts that use the user management API endpoints stop working at the switch. See [System groups API availability](../integrations/sigrid-api-documentation.md#system-groups-api-availability) to check which endpoints are available.
5. **After the switch,** create the groups in **Portfolio settings > Structure and access**, add systems, and assign users and user groups.

## Frequently asked questions

- **Is my team and division metadata deleted?** No, this metadata remains available for now. We are looking into removing the team and division metadata fields, since the system groups serve a similar purpose, but if we choose to go ahead with that it will be a separate change which we will communicate timely, with a sufficient transition period.
- **Does moving a system into a group change the system?** No. A system keeps its identity, so Sigrid CI and API integrations keep working.
- **Do I need to reconfigure all my system access permissions?** No. Migration to the new system-group structure is automatically performed – all systems sit directly under the portfolio, and permissions are transferred. Configuring system groups and reorganizing users/user groups across them is optional.
- **Can I keep using the existing API endpoints?** As the access and permission management has fundamentally changed, the old API endpoints for user management and permissions will stop working after the system groups release. See [System groups API availability](../integrations/sigrid-api-documentation.md#system-groups-api-availability) for the adjusted and new endpoints.
