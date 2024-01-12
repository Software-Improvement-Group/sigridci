Configuring Sigrid Single Sign-on with OKTA
===============================================

This page describes an example of the technical setup for Sigrid customers using OKTA as their Identity Management Provider.

## Creating an Application for Sigrid SSO
As OKTA administrator, add a SAML app.

### General SAML Settings

- Single sign-on URL : https://auth.sigrid-says.com/saml2/idpresponse
- Audience URI : urn:amazon:cognito:sp:eu-central-1_hwh9zdyCY

### Attribute statements

- Sigrid needs 3: email, first and last name

| Name | Value |
| ----------- | ----------|
| http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress  | user.email  |
| http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name   | user.lastName  |
| http://schemas.xmlsoap.org/ws/2005/05/identity/claims/given_name   | user.firstName  |




<img src="../images/okta-attribute-statements.png" width="800" /><br />

### Saved Saml app

<img src="../images/okta-saml-settings.png" width="800" /><br />


# Contact and support
Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.
