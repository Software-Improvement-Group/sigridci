Quick start guide

QSM Mendix teamserver
========================

This page describes the technical onboarding of a new QSM customer into the Sigrid-says platform. The items that we will address are 'how to onboard users' and 'how to onboard Mendix projects from the teamserver'. After the technical onboarding your QSM environment will be up and running. You will then progress into the next phase during which you will to get to know the functionalities of the platform.

# Default teamserver scenario

Most Mendix customers use the Mendix teamserver to store their projects. Developers code and collaborate on this hosted location. QSM connects to your project just like your developers do. It will retreive the code artefacts (not the production data) from the teamserver. By default QSM retreives the mainline on a daily schedule.

## how to onboard users

During the technical onboarding we will ask you what authorisation you require. QSM offers both a basic version of user management or it can connect to your Identity Provider to obtain Single Sign On. There is a [user management](link) page describing this in detail. In either way you will have a first user with administrator rights at your disposal to get the onboarding of users going.

## how to onboard Mendix projects from the teamserver

Mendix offers a self servive app to do this. The [addon app](https://addon.mendix.com) helps you onboard new projects in QSM. After 5 minutes you will receive an email stating the onboarding was succesful and you will be able to see the results for this project in QSM.

what do you need:

- your mendix login
- the name of the mendix project you want to onboard
- with that login you create a [Personal Acces Token](https://docs.mendix.com/apidocs-mxsdk/mxsdk/set-up-your-pat/).  When creating the pat please choose `mx:modelrepository:repo:read Read access to Team Server Git repositories and Team Server API`  
Also make sure that the PAT is bound to a Mendix developer that has access to the project with a minimum os Scrum Master. For scalability you can create a PAT for a system users that has access to all your projects.






## Available end points


## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.
