User management in Sigrid
===========================================

When managing user access to Sigrid we need to consider both Authentication (can you enter?) and Authorisation (what can you see?). 
- Authentication is the step where users are allowed to enter the platform. After Authenication is successful, 
- Authorisation defines which user can access the analysis results of which systems.

Sigrid offers two ways of managing Authentication and one type of Authorisation. 

This page describes the options and the technical setup.

# Authentication mechanisms

## 1. Using the Sigrid user management module
With this module, a Sigrid administrator can perform all the basic authentication tasks out of the box.

### Note
- That your users will need to set a password.
- Sigrid support can make the use of MFA (multi-factor authentication) mandatory for your users.
- You will need to actively revoke access for users that have left your company by deleting them from user management.

### Sigrid administrator tasks
- Create users based on their email, first and last name.
- Resend lost and temporary passwords.
- Check the last login and MFA status.
- Do authorisation tasks to define who can see what in Sigrid.
- Delete users

### Setup customer side
- No setup is needed.

## 2. Using Single Sign On (SSO) with an Identity Management Provider (IdP)
When Sigrid is linked to your SSO the user provisioning is done by the IdP. Sigrid supports SAML or OpenID Connect protocols via a service-provider initiated authentication flow. 


### Notes
- With a service-provider initiated authentication flow, users first goto customer.sigrid-says.com, then they get redirected to their Identity management provider, login, and get redirected back to Sigrid
- SSO improves the ease of use for your colleagues because there is no Sigrid password to remember. 
- Improves security because users are created and deleted centrally in your organisation.
- Sigrid follows the password policy of your organisation.

### Sigrid administrator tasks
- Check the last login
- Do authorisation tasks to define who can see what in Sigrid

### Setup on client side
Create an Enterprise application 'app' in your IdP with the following details: 
- Audience or Identifier (Entity) ID: urn:amazon:cognito:sp:eu-central-1_hwh9zdyCY
- Reply URL: https://auth.sigrid-says.com/saml2/idpresponse

With the following Attributes & Claims:

| Your user | Namespace + SAML attribute name as expected by Sigrid |
| ----------- | ----------|
| user email  | http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress |
| user last name   | http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name |
| user first name   | http://schemas.xmlsoap.org/ws/2005/05/identity/claims/given_name |
| unique user identifier | emailaddress |


Other
- Signature Algorithm: RSA_SHA256
- Digest Algorithm: SHA256
- Assertion Encryption: unencrypted (privacy is provided by using HTTPS)
- SAML Single Logout: disabled

Then assign groups of users to your Authentication app.

### Example Active Directory

<img src="../images/azure-saml.png" width="800" />

### Example OneLogin
Please see the separate [OneLogin page](usermanagement-example-onelogin.md).

### Example Okta
Please see the separate [OKTA page](usermanagement-example-okta.md).


### Info to provide to SIG
Provide SIG with the 'App federation MetadataURL' of your authentication app.
The information will include your app's identifier, redirectURL etc.

### Deliverables
SIG will setup SSO for you. You will have your own customer-specific URL Sigrid.
https://customername.sigrid-says.com

# Authorisation in Sigrid
The product team is actively developing the user management pages to cater to more use cases. At the moment the user manages the following functions.

### Two types of users
Sigrid has two types of users, the normal users that have access to a list of 1 to all systems and the Sigrid administrators that can edit all the users including other administrators.

Tasks unique to Administrators beyond User Management include:
- [Setting and using Sigrid Objectives](../capabilities/objectives.md)
- [Adding business context to a system using metadata](metadata.md)

### System level access
An administrator can specify on system level the access any user in the portfolio has. Once access has been granted to a user, they will be able to view all Sigrid content for the selected system. 

#### Bulk assigning system access
When creating or editing a user, it is possible to assign system access in bulk via several new system access controls. These system access controls are based on the metadata supplied for systems, allowing a user to receive access to all systems labeled with Division, Team or Supplier metadata.

<img src="../images/um-bulk-system-access-controls.png" height="600"  />

Upon selection of one of the filters, the user will be presented with a list of system groups based on the assigned metadata. From here you have the ability to add a group as a whole, or expand the group to add specific systems to the user's access.
Important to note is that these bulk assignments are not currently "sticky" for the user, in the sense that if you assign access to a system group to a user, only those systems currently present in the system group will be accessible to the user. If a new system is then added to this group, the user will need to reassign the group as a whole to the user.

This is helpful when trying to assign a logical grouping of systems for a new user, without having to identify and add the systems one by one.

For more information on assigning metadata to systems, please see the separate [Metadata page](metadata.md)

__Note:__ Bulk assignment of system access can be done both when assigning permissions to a single user, as well as when defining permissions for authorization groups.

### Authorisation groups
Administrators also have the ability to specify system access in bulk for groups of users, by creating an authorisation group entity by which users can be added to this group along with a permission set. All users added to a defined authorisation group will inherit access rights to systems authorized for the group. 

#### Creating groups in User Management

You can find the user group table on the User Management page by switching to the "Groups" tab above the User Permissions table.

<img src="../images/um-user-group-table.png" width="600" />

Creating a new user group is simple and follows a very similar process for assigning permissions to users. From the "Groups" tab, simply click the "Add user group" button and this will trigger a new dialog to appear.

From here you can input a descriptive name for the new authorisation group as well as a description of the responsibility of this group.

<img src="../images/um-group-details-dialog.png" width="600" />

Upon saving of the group details, the authorisation group is created. At this state the group will have no users or system access, but the group entity does exist and will populate the User Groups table.

<img src="../images/um-group-created.png" width="600" />

At this point the user is free to delete the group (done via clicking the red "X" icon to the right of the entry in the table) edit the group (via clicking on the pencil icon to the right of the entry in the table).

Switching to the Members section in the edit group dialog, the user can freely allocate group membership to other users within the portfolio. Important to note is that users will only be added to the group when clicking "save", closing the dialog without saving will result in users not being added to the group.

<img src="../images/um-groups-adding-users.png" width="600" />

The final step for the group is to grant system access, which is done via the Permissions section in the Edit User Group dialog. Here you'll find a very familiar process as adding system access for users, the main controls are the same.

System assignment can be done one-by-one, or in bulk using the metadata based bulk assignments. Any system added to the group will be accessible by all group members for the lifetime of the group or until the user is removed from the group. 

<img src="../images/um-groups-assigning-permissions.png" width="600" />

Naturally, any change in the permissions of a group will be reflected in the permissions of all users present in the group. Some key things to keep in mind when assigning permissions via authorisation groups are the following:
- Inherited access rights to systems are in addition to any current rights the a user may have, it does not overwrite existing authorization rights of the user.
- Users can be part of multiple groups, and will inherit all access rights of any groups they are a part of. Again, inheritance of one group's access rights does not overwrite the inheritance another group's access rights, these access rights are simply combined in total. Any overlap in access will simply see the user retain access right to the overlapped system.
- Inherited access rights are not possible to be revoked piece-wise, to remove inherited system access from a group requires the user to be removed from said group.
- System level access for the group is defined in the same manner as it is for an individual, and includes the same ability to bulk assign systems to a group via the use of the access control filters for teams. suppliers or divisions.


### Passwords
The administrator can help users by resending a forgotten password or the initial temporary password.
When a user has confirmed their password, they can request a new password themselves.

# Contact and support
Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.
