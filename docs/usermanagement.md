User management in Sigrid
===========================================

When managing user access to Sigrid we need to consider both Authentication (can you enter?) and Authorisation (what can you can see?). 
- Authentication is the step where users are allowed to enter the platform. After Authenication is succesful, 
- Authorisation defines which user can access the analysis results of which systems.

Sigrid offers 2 ways of managing Authentication and 1 type of Authorisation. 

This page describes the options and the technical setup.


# Authentication mechanisms

## 1. Using the Sigrid user management module

With this module a Sigrid administrator can perform all the basic authentication tasks out of the box. 

### Note:
- Your users will need to set a password and optionally MFA (multi factor authentication)
- you will need to actively revoke access for people that no longer work for you by deleting them from user management manually.

### Sigrid administrator tasks:
- create users based on their email, first and lastname.
- resend lost and temporary passwords.
- check last login and MFA status.
- do authorisation tasks to define 'who can see what' in Sigrid.
- delete users

### Setup customer side
- no setup is needed.


## 2. Using Single Sign On (SSO) with an Identity Management Providor (IdP)

When Sigrid is linked to your SSO the user provisioning is done by the IdP. Sigrid supports SAML or OpenID Connect protocols.

### Note:
- SSO improves the ease of use for your colleagues because there is no Sigrid password to remember 
- improves security because users are created and deleted centrally in your organisation. 
- Sigrid follows the password policy of your organisation.


### Sigrid administrator tasks:
- check last login
- do authorisation tasks to define 'who can see what' in Sigrid

### Setup customer side
- create authentication 'app' in your IdP with the following details: 
- url: https://auth.sigrid-says.com/saml2/idpresponse
 - audience: urn.amazon:cognito:sp:eu-central-1_hwh9zdCY
 - Signature Algorithm: RSA_SHA256
 - Digest Algorithm: SHA256
 - Assertion Encryption: unencrypted (privacy is provided by using https)
 - Saml Single Logout: disabled
 - Attribute statements:

 user.email http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress

 user.firstName http://schemas.xmlsoap.org/ws/2005/05/identity/claims/given_name
 
 user.lastName http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name

- assign groups of users to your Authentication app

### Setup steps on SIG side
- provide SIG the appid of your authentication 'app'. Examples are
metadata URL: https://customername.okta.com/app/<randomidentifier>/sso/saml/metadata

- you will recieve a customer specific url to enter Sigrid like
https://customername.sigrid-says.com


# Authorisation in Sigrid

### types of users
Sigrid has two types of users, the normal users that have acces to a list of systems and there are the administrators that can edit the normal users. 

### system level access
An administrator can specify on system level the access any user in the portfolio has. In order to make the authorisation easier, filters can be applied on team or division to allow for bulk assigments.

### passwords
The administrator can help users by resending a forgotten password or by resending the initial temporary password.
When a user has confirmed their password, they can request a new password themselves

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.
