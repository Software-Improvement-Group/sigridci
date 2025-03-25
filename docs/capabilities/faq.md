Sigrid: Frequently Asked Questions
==================================

### Sigrid Security

See [Sigrid Security: Frequently Asked Questions](faq-security.md).

### Sigrid Architecture Quality

See [Sigrid Architecture Quality: Frequently Asked Questions](faq-architecture.md).

## Usage questions

### Do you support pull request integration?

Yes! There are basically two usage scenarios for Sigrid CI, and you would typically use them both.

The first Sigrid CI use case is to *publish* your project's source code to Sigrid, which makes the analysis results accessible on [https://sigrid-says.com](https://sigrid-says.com). You would typically use this for your project's main branch, which can be `main`, `master`, or something project-specific. This is known as the *baseline version*.

The second use case is to use Sigrid CI for feedback during code reviews on pull requests. This wil compare the contents of the pull request agains the baseline version, allowing you to identify improvement areas in the new and changed code.

The [platform-specific documentation and examples](../README.md) cover instructions for both scenarios. We generally recommend to use Sigrid CI for both scenarios, although it's also perfectly fine to use Sigrid CI for one scenario but not the other.

### Does Sigrid CI fit in my workflow?

Different development teams use different workflows. Our [workflow documentation](../sigridci-integration/development-workflows.md) covers different development/branch/CI workflows, and how Sigrid CI would fit into those workflows.

### Which technologies do you support?

Sigrid supports almost 300 different technologies, so we are pretty confident that we are able to support most projects out-of-the-box. Moreover, we are constantly adding support for new technologies, and extending our support for existing ones. This even includes some pretty specific technologies with a focused group of target users, such as proprietary programming languages developed in-house at our clients. 

If you are using a technology that you believe we do not support, please contact us using the contact information below, and we'll see what we can do.

### What is my system name?

You will find the system name in the url of the monitor in Sigrid. The structure is https://sigrid-says.com/customer/systemname/-/maintainability

### How to get a token and account?

Follow the instructions on how to create your personal token [here](../organization-integration/authentication-tokens.md)

### What target quality should we use?

Avoid setting an unreasonably high target quality level. While it seems appealing to be ambitious, this can be demotivating or frustrating to people, as it's not always possible to achieve such a high level in every single change.

For systems implemented in modern technologies, we recommend a target quality level of 3.5 stars. This strikes a balance between ambition and practicality. Note that 3.5 is already above the benchmark average of 3.0 stars, so this level is already asking developers to outperform the industry as a whole, and is therefore quite a high target.

For legacy systems, the target quality should be in line with the system's current quality. If the system as a whole is currently at 2.1 stars, it's not realistic to ask every single code change to rate 4.0 stars or higher. The same applies to systems in domains where the technology makes it harder to write maintainable code, for example when using low-level languages like C.

### Where can I find more information about your metrics?

Sigrid itself includes a brief explanation of all metrics in the "refactoring candidates" page. If you need more information, you can find the [Guidance for producers](https://www.softwareimprovementgroup.com/wp-content/uploads/SIG-TUViT-Evaluation-Criteria-Trusted-Product-Maintainability-Guidance-for-producers.pdf) on our website, which provides more details on what is measured and why.

For training purposes, SIG also published a book on [building maintainable software](https://www.amazon.com/Building-Maintainable-Software-Java-Future-Proof/dp/1491953527/ref=sr_1_7?dchild=1&qid=1610456817&refinements=p_27%3AJoost+Visser&s=books&sr=1-7&text=Joost+Visser), which contains detailed explanations on the metrics. It is not necessary to read the book to use Sigrid, but having training material available can be useful when training new or junior developers.

### How can I use Sigrid to improve my code maintainability?
To improve a system's maintainability you will need to understand some context of [our approach to maintainability](../getting-started/approach.md), and e.g. the [paragraph with an overview on interpreting metrics](../getting-started/approach.md#further-reading-and-interpreting-metrics). Understanding on the used metrics is required [see the SIG quality model page](../reference/sig-quality-models.md). Because you will have a better idea of what the metrics are measuring conceptually, how it will help your maintenance, and what you should pay attention to. [The system maintainability page](system-maintainability.md) offers you an overview for navigating and understanding maintainability in Sigrid. 

Depending on how you are using Sigrid (CI-integrated or web interface), you will see different levels of detail and follow a different order of activities (e.g. see the workflows:[general Agile process](../workflows/agile-development-process.md), [Architect](../workflows/architect.md), [Developer](../workflows/developer.md), [Product Owner](../workflows/product-owner.md) or [(Development) Manager](../workflows/manager.md)). 

### What is the maximum upload size for Sigrid CI?

Sigrid CI is limited to uploads of 500 MB. This is mainly for performance reasons, since uploading and unpacking huge files takes some time, which endangers Sigrid CI's goal of providing quick feedback. Note that based on our experience 99% of repositories easily fit within this limit. Also, Sigrid will only measure the actual source code maintained by your development team. Other artifacts, such as libraries, binaries, or other non-source files are excluded.

### Can I exclude certain files from being uploaded?

Yes. In general, we only need to receive the actual source code, configuration and data is not required to perform the analysis and can be excluded from the upload.

Some files and directories are already excluded by default, based on common conventions for common technologies. For example, the following would be excluded automatically:

- The `node_modules` directory is excluded by default as it contains [NPM](https://www.npmjs.com) libraries
- The `target` directory is excluded as it contains build output from [Maven](https://maven.apache.org)

In addition to that, you can also exclude files and directories specifically for your project. This is done using the `--exclude` parameter, which is explained in the [configuration documentation](../sigridci-integration/integration.md) page.

### Do Sigrid CI uploads get added to the Sigrid dashboard?

No. This is intentional: Sigrid CI tends to operate on pull requests, which are often branches that are a work-in-progress and still need to be reviewed. Adding every single build to the Sigrid dashboard would create a lot of noise, which makes it harder to use the dashboard for spotting trends and reporting. This is why there are two separate streams of uploads: one used for Sigrid CI (based on branches/pull requests), and one used to feed the Sigrid dashboard (based on a relatively stable branch, such as main).

Of course, one size doesn't fit all. Post-beta versions of Sigrid CI will at least give the *option* to also publish uploads to the Sigrid dashboard, so that every team can decide for themselves which uploads should be visible in the dashboard and which should not.

### What branch or commit does Sigrid CI compare against?

Feedback is based on comparing the source code against the current baseline in Sigrid. In other words, this depends on the branch you're using to populate the Sigrid dashboard. This would typically be the main branch, though for some teams the baseline could also be based on a release branch, the development branch, or an improvement branch. The baseline therefore depends on the team's way of working and branching strategy. 

### Why am I being penalized for problems that were already there?

We created Sigrid CI to be used during code reviews, so the feedback is based on only the files you touched during your pull request, not the whole system. 

However, we do consider the *entire* contents of those files, not only the lines that you personally wrote. This is because of the [boy scout rule](https://www.oreilly.com/library/view/97-things-every/9780596809515/ch08.html): *"Always leave the campground cleaner than you found it."*. Refactoring and regular work are not two separate activities, they belong together. Having separate tickets to refactor certain areas is OK, but it indicates that something went wrong earlier in the process, that led to those issues being introduced in the first place. Ideally, small refactorings should be done *during* regular tickets. That means that any tickets affecting existing files should not *only* consist of implementing the new behavior. You should also strive to make small refactorings that relate to the code you're currently working on. You have the files open anyway! 

This concurrent approach to technical debt is also described in the [agile development process workflow](../workflows/agile-development-process.md#for-maintainability-focus-on-technical-debt-that-is-affecting-you-right-now).

### Why are architecture metrics excluded from Sigrid CI?

There are limits to the amount of refactoring you can do in the context of a single ticket. It's probably not a good idea to change the entire architecture while working on a bug fix. This is why Sigrid CI reports on a subset of [SIG's maintainability quality model](https://www.softwareimprovementgroup.com/methodologies/iso-iec-25010-2011-standard/): the code-level metrics are in scope, but the architecture-level metrics are not. This is due to the difference in *local* versus *global* refactorings. Making some changes in the context of a file tend to be fairly local, in that they don't affect a lot of other people. This is why those types of refactoring are fine to work on during regular development work. In contrast, architectural refactoring will have a big impact on a lot of people, so this is something that needs more consideration and needs to be planned separately.

Let us know if you believe we *should* provide feedback on architecture metrics in Sigrid CI, as we are considering to offer it as an option in a future version.

### Should we fail the build if the Sigrid CI check fails?

That's obviously your decision and something that depends on your development process. However, if you're asking our advice, we would say a failing Sigrid CI check should produce a warning rather than an error. That might seem like ridiculous advice coming from a company that creates software quality tooling, but we can explain.

One of Sigrid's key goals is making software quality advice *reasonable*. It's easy to invent a thousand quality checks and making them all mandatory, failing the build as soon as a single violation is found. It's obviously possible to fix every single issue, but it's probably not worth it considering what you get in return. Sigrid focuses on a relatively limited set of metrics, to avoid overloading developers with tons of instructions. Moreover, a small amount of non-conformities is tolerated, as long as the overall quality doesn't drop below a certain level. 

We therefore believe in a comply-or-explain model. Obviously, you should still strive to pass the Sigrid CI check in the overwhelming majority of cases. However, in the rare cases the check fails, it's perfectly OK for the reviewer to overrule the check and accept the pull request, as long as the reviewer finds that the author had good reasons for deviating from the best practice in that particular case.

### Why does deleted code not influence the rating?

In general, deleting code improves maintainability. The less code you have, the less you have to maintain. Having less code also makes it easier to make structural changes, since such changes will require less effort. So if you navigate in Sigrid, you may find its effects. The exact consequences depend on how "good or bad" the deleted code was compared to the rest of the codebase, since volume is the common denominator for the maintainability metrics ([See for more details the technical documentation](../reference/sig-quality-models.md)).

So why does Sigrid CI only give ratings based on new and changed code, but doesn't reward you for deleting code? This is mostly to keep the rating simple: combining code quality and deleted code into a single metric would make it hard to understand. Also, the majority of pull requests are about adding new code or changing existing code, deleting code is less common, so we have chosen to not optimize for that scenario.

### We have a multi-repo project, can I still use Sigrid CI?

Yes. In some situations, the view of your project/system in Sigrid might differ from your repository structure. For example, you might have separate repositories for your back-end and front-end, yet Sigrid combines them into one big system. 

There are two ways to use Sigrid CI in such a situation. 

- You can change the structure in Sigrid to match your repositories. This is the simplest option, but different roles
  can have different opinions on what is a suitable structure in Sigrid (though development teams tend to prefer Sigrid
  matching their repositories).
- Even when *not* changing the Sigrid structure, it is still possible to run Sigrid CI for your repository. You can use
  the `--subsystem` option to explain Sigrid CI how your repository structure should be matched to your Sigrid
  configuration. This option is explained in [using the Sigrid CI client script](../reference/client-script-usage.md).

## Why are there differences between the directory structure as we see it in our IDE and Sigrid components?

Your system may be defined/scoped in a different way than simply mapping directories as components. Scoping choices als allows for specific filtering and componentization. See the [scope configuration page](../reference/analysis-scope-configuration.md). If there are any differences you will notice them in the [Code Explorer](../capabilities/system-code-explorer.md#different-views-directory-or-component-structure).

### Can I see which files are uploaded to Sigrid?

Yes. You can add the `--showupload` option when calling the [client script](../reference/client-script-usage.md). This will add log output for every file that is included in the upload that is submitted to Sigrid.

### Why do you have both publish and publishonly options, what is the difference?

The [list of Sigrid CI options](../reference/client-script-usage.md) lists two options with similar names and descriptions, `--publish` and `--publishonly`. These options support slightly different scenarios:

- `--publish` publishes your project's source code to Sigrid, *and* provides feedback on your changes within your Continuous Integration environment.
- `--publishonly` also publishes your code to Sigrid, but it *does not* provide feedback within the Continuous Integration environment.

So which one should you use? That depends on your development process. If you use pull requests, you can use `--publishonly`. In this scenario, you've already received feedback for your pull request, so there is no need to receive the same feedback again when you merge your changes to your main/master branch. If you *do not* use pull requests, or if you are not sure, it is best to use `--publish` since it will give you the most feedback.

## Common problems

### What to do when the script does not work?

The Sigrid CI Python script is currently under active development, which means that its subject to change, and namely, its dependencies are subject to change as we add new functionality.
Sigrid CI requires Python 3.7 or higher. 
In some cases multiple python versions are installed in the environment and the wrong one (below 3.7) may be selected automatically. If that is the case, please make sure that the highest version is set to be the default.
When not using Docker to run the script, this requires that the dependencies in the environment in which the script is being ran are in sync with the actual code, and, in order to do that, you can run either `pip install -r requirement.txt` or `pipenv install`, when using Python virtual environments.

### I'm receiving an error message that certificate verification failed

In some cases, the Sigrid CI client script might produce an error message `[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate`. This indicates that Python is unable to access the system's certificate store. Sigrid CI does not need any special or custom certificates, access to the regular system certificates is sufficient. 

If your environment requires a certificate store in a custom location, the environment variables `openssl_cafile_env` and `openssl_capath_envz` can be used to point Python to the correct location. Refer to the [Python documentation on OpenSSL](https://docs.python.org/3/library/ssl.html) for more information

### I used the subsystem option and see results from other subsystems

If your repository is part of a larger system you can use subsystem to only get feedback on your repository. This is
done on a best effort basis, and if multiple pipelines run at the same time for the same system this might influence the results.
To give you feedback on your changes Sigrid CI uses both the source code and measurement results from the last published
measurement. If new results are published while we retrieve these measurements, some discrepancies might occur. If this
happens, try running Sigrid CI again, preferably at a quieter moment. If it is a recurring issue,
please [contact us](mailto:support@softwareimprovementgroup.com).

### Where do I find the Sigrid CI output ?

The results of the SigridCI run are logged in the terminal output and optional as a html artefact. For the artefact to be stored you will need to specify the Sigrid CI output path in your yml. Check out the examples for GitHub and GitLab. 

### I started using Sigrid CI, and now I suddenly see more code in Sigrid

Sigrid supports multiple ways to upload source code. This documentation covers Sigrid CI, but we also support uploads via SFTP. If you previously used SFTP and then switch to Sigrid CI, you might see some differences. For example, you might suddenly see extra code, or extra components. This is caused by differences in how the upload is created. Unfortunately that means there is no "quick fix" outside of updating your configuration. We are happy to help you with identifying the changes, so please [contact us](mailto:support@softwareimprovementgroup.com) and we'll try to help you out.

This also means that we recommend you to either use Sigrid CI or SFTP uploads, but not both. Using two ways of uploading means both uploads need to be consistent, otherwise you'll end up with expected changes in Sigrid. In practice this is not always convenient, so if you're using Sigrid CI we recommend you stop using SFTP and just Sigrid CI for all uploading/publishing to Sigrid.

### I'm receiving an error message about UnicodeEncodeError

In some environments, Sigrid CI can produce the following error:

    UnicodeEncodeError: 'charmap' codec can't encode characters
    
This happens when Sigrid CI tried to provide command line output that includes UTF-8 characters, but `stdout` is unable to display such errors. This can be solved by adding the `export PYTHONIOENCODING=utf8` environment variable.

### I'm receiving an error message about dubious ownership in repository

This message occurs when the (Linux) user that cloned your Git repository is different from the (Linux) user that is running the CI job. This scenario is pretty uncommon, in the majority of cases the entire CI pipeline is performed with the same user. If you see this error, you can add `git config --global --add safe.directory <repository-dir>` to tell Git it is safe to trust the directory to which the repository was cloned. Note you need to provide the directory's absolute path, Git will not allow `.`.

## Infrastructure and security questions

### How do you protect our source code?

SIG is ISO/IEC 27001 certified, to ensure information security management and appropriate levels of confidentiality, integrity, and availability of your data.

You can find more information on SIG's infrastructure and security protections in the [Information Security Policy](https://www.softwareimprovementgroup.com/wp-content/uploads/SIG_Information_Security_Policy.pdf).

### Where is your service hosted?

Sigrid, including Sigrid CI, is hosted on Amazon Web Services. If you have specific questions on our infrastructure, please [contact us](mailto:support@softwareimprovementgroup.com). 

### Do we need to update our firewall settings?

Possibly. As mentioned above, Sigrid is hosted on AWS. This means your firewall needs to allow outgoing traffic in order to submit your project's source code to Sigrid. In practical terms this means the following:

- Allow outbound traffic to `sigrid-says.com` on port 443
- Allow outbound traffic to `auth.sigrid-says.com` on port 443
- Allow outbound traffic to `sig-sigrid-ci-upload.s3.eu-central-1.amazonaws.com` on port 443

[Contact SIG](mailto:support@softwareimprovementgroup.com) if you need specific information on this setup.

### Do you support people using their own certificates or certificate authority?

Yes, but you will need to explicitly tell Python to trust your certificates. 

- First, make sure your certificate `pem` files are accessible from where you are running Sigrid CI.
  - If you are running Sigrid CI from your own environment, simply make sure the location is accessible from your pipeline.
    - In this scenario, Python will automatically pick up certificates from your operating system's certificate store, meaning you should not need manual configuration.
    - If the above does not work for your particular operating system, you can also use the environment variables from the next option.
  - If you are using Docker-based Sigrid CI, you will need to mount this location to make it available to the Docker container.
    - Next, point Python to where to find your PEM files by updating the following environment variables:
      - `SSL_CERT_FILE: /path/to/mounted/cert.pem`
      - `REQUESTS_CA_BUNDLE: /path/to/mounted/cert.pem`

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.
