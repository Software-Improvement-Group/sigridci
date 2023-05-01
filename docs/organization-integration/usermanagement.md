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
- Your users will need to set a password and optionally MFA (multi-factor authentication)
- You will need to actively revoke access for people that no longer work for you by deleting them from user management manually.

### Sigrid administrator tasks
- Create users based on their email, first and last name.
- Resend lost and temporary passwords.
- Check the last login and MFA status.
- Do authorisation tasks to define who can see what in Sigrid.
- Delete users

### Setup customer side
- No setup is needed.

## 2. Using Single Sign On (SSO) with an Identity Management Provider (IdP)
When Sigrid is linked to your SSO the user provisioning is done by the IdP. Sigrid supports SAML or OpenID Connect protocols.

### Note
- SSO improves the ease of use for your colleagues because there is no Sigrid password to remember 
- Improves security because users are created and deleted centrally in your organisation.
- Sigrid follows the password policy of your organisation.

### Sigrid administrator tasks
- Check the last login
- Do authorisation tasks to define who can see what in Sigrid

### Setup customer side
Create an authentication 'app' in your IdP with the following details: 
- URL: https://auth.sigrid-says.com/saml2/idpresponse
- Audience: urn.amazon:cognito:sp:eu-central-1_hwh9zdyCY
- Signature Algorithm: RSA_SHA256
- Digest Algorithm: SHA256
- Assertion Encryption: unencrypted (privacy is provided by using HTTPS)
- Saml Single Logout: disabled

With the following attribute statements:
- user.email http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress
- user.firstName http://schemas.xmlsoap.org/ws/2005/05/identity/claims/given_name
- user.lastName http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name

Then assign groups of users to your Authentication app

### Info to provide to SIG
Provide SIG with the MetadataURL of your authentication app.
The information will include your app's identifier, redirectURL etc.

### Deliverables
SIG will setup SSO for you. You will have your own customer-specific URL Sigrid.
https://customername.sigrid-says.com

# Authorisation in Sigrid
The product team is actively developing the user management pages to cater to more use cases. At the moment the user manages the following functions.

### Two types of users
Sigrid has two types of users, the normal users that have access to a list of 1 to all systems and the Sigrid administrators that can edit all the users including other administrators.

### System level access
An administrator can specify on system level the access any user in the portfolio has. In order to make the authorisation easier, filters can be applied on teams or divisions to allow for bulk assignments.

### Passwords
The administrator can help users by resending a forgotten password or the initial temporary password.
When a user has confirmed their password, they can request a new password themselves

# Contact and support
Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.
