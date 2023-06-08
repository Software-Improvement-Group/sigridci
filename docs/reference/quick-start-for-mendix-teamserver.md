Quick start guide for QSM Mendix teamserver
===========================================

This page describes the technical onboarding of a new QSM customer into the Sigrid-says platform. The items that we will address are 'how to onboard users' and 'how to onboard Mendix projects from the teamserver'. After the technical onboarding your QSM environment will be up and running. You will then progress into the next phase during which you will to get to know the functionalities of the platform.

## Default teamserver scenario

Most Mendix customers use the Mendix teamserver to store their projects. Developers code and collaborate on this hosted location. QSM connects to your project just like your developers do. It will retreive the code artefacts (not the production data) from the teamserver. By default QSM retreives the mainline on a daily schedule.

## How to onboard users

During the technical onboarding we will ask you what authorisation you require. QSM offers both a basic version of user management or it can connect to your Identity Provider to obtain Single Sign On. For more information, see the [general instruction on how to set up Sigrid](../organization-integration/onboarding-steps.md), or the [user management](docs/organization-integration/usermanagement.md) page describing this in detail. In either way you will have a first user with administrator rights at your disposal to get the onboarding of users going.

## how to onboard Mendix projects from the teamserver

Mendix offers a self service app to do this. The [addon app](https://addon.mendix.com) helps you onboard new projects in QSM. After 5-10 minutes you will receive an email stating the onboarding was succesful and you will be able to see the results for this project in QSM.

What do you need:

- the name of the Mendix project that you want to onboard in QSM
- your Mendix login, make sure that your access level is at least Scrum Master 
- with that login you create a [Personal Acces Token](https://docs.mendix.com/apidocs-mxsdk/mxsdk/set-up-your-pat/).  When creating the PAT please choose these read only security settings:
 `mx:modelrepository:repo:read Read access to Team Server Git repositories and Team Server API`  
- For scalability you can create a PAT for a system users that has access to all your projects.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.
