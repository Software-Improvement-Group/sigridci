Changing the analysis scope configuration
=========================================

You can change Sigrid's configuration for your project, to make Sigrid's feedback as useful and actionable as possible. We call this configuration "the scope".

By default, Sigrid will try to automatically detect the technologies you use, the component structure, and files/directories that should be excluded from the analysis. However, you can override this standard configuration with your project-specific configuration. To do this, create a file called `sigrid.yaml` and add it to the root of your repository. When you merge changes to `sigrid.yaml`, Sigrid will pick up the new configuration and apply it to subsequent scans.

<iframe width="560" height="315" src="https://www.youtube.com/embed/Uomc7hUbRTw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

The following example shows a typical example of the `sigrid.yaml` configuration file:

```
component_depth: 1
exclude:
  - ".*/simulator/.*"
languages:
  - name: java
  - name: python
  - name: typescript
```


## General configuration

| Field              | Required | Description                                                                                                    |
|--------------------|----------|----------------------------------------------------------------------------------------------------------------|
| `model`            | No       | Version of the SIG quality model that should be used to analyze your project. Default is latest model version. |

## Excluding files and directories

Sigrid will exclude common patterns by default. For example, directories like `build`, `dist`, and `target` typically contain build output and are not part of the source code. Directories like `node_modules` contain open source libraries and are not part of the application's own source code. Those directories are therefore ignored during the analysis.

It is possible to extend this list with project-specific files and directories that should also be excluded. The `exclude` section in the YAML file contains a list of regular expressions for paths to ignore. For example, `.*[.]out[.]js` will exclude all files with a name ending in `.out.js` from the analysis. Adding `.*/simulator/.*` will exclude everything in the directory `simulator`.

Note that it is not necessary to exclude files and directories that would not be analyzed anyway. 

## Technology support

See the [list of supported technologies](technology-support.md) for the names that can be used inside the `languages` section of the YAML file.

### Overriding automatic technology-, and test code detection

When you add a technology to your scope file, Sigrid will try to locate the corresponding files based on file and directory name conventions. This includes automatic detection of test code. For example, Java-based projects typically use `src/main/java` for production code and `src/test/java` for test code.

This automatic detection is usually sufficient for the majority of projects. However, if you are using less common frameworks or a custom naming convention, you will need to tell Sigrid where it can find the test code. Like other parts of the scope file, this is done using regular expressions:

```
languages:
  - name: Java
    production:
    test:
      include:
        - ".*/our-smoke-tests/.*[.]java"
```

This example will classify all Java code in the `our-smoke-tests` directory as test code.

## Defining components

Component detection is based on the project's directory structure. What "components" mean depends on the technology. In Java, components are usually based on Maven modules. In C, components are often simply the project's top-level directories.

Components can be defined in two ways. The simple option is to simply base the components on directory depth. The following example will use the project's top-level directories as components.

    component_depth: 1
    
In some projects, using directory depth will not accurately reflect the actual component structure. The more advanced options allows you to define components explicitly:


**Advanced Option 1** (short)

    component_base_dirs:
      - "modules"
      - "modules/specific"
      - "" \[This includes the root directory as a separate component\]

**Advanced Option 2** (can be more specific, but also harder to maintain)

    components:
      - name: "Back-end"
        include:
          - ".*[.]java"
      - name: "Log"
        include:
          - ".*/cs/findbugs/log/.*"
          
In this example, regular expressions are used to define what files and directories belong to each component. The syntax is identical to the patterns used in the `exclude` section.

### A note about writing regular expression patterns
* The full file path must always be matched instead of (part of) a filename. This generally requires some wildcards.
  - The engine starts searching starting with the first "/". So if you are fairly certain that the first level folder structure is stable you could hardcode that in the pattern, such as
```
name: “frontend”
include:
  - “/frontend/.*[.]jsx”
```
* All patterns are case-sensitive. This is relevant in case you are specifically searching for naming in camelCase or PascalCase. It is then useful to search for files like /SomeTest.java.
<!--Note SR: to show 2 backslashes you have to write 3 backslashes-->
* Escape special groups with an extra backslash. This is because yaml interprets “\” as an escape character (so does GitHub, by the way). So a regular expression searching for a space character needs 2 backslashes like so: “\\\s” or a word character (defined as [a-zA-Z0-9_]) as “\\\w”.
  - If you want to express a literal dot “.” use "[.]". This means: 1 character in a group where only “.” is permitted. This is more readable than , “\\\.”.
* Matching "positive" patterns is far easier than trying with negative lookaheads "(?!)" because catching the full file path becomes difficult. There are cases where patterns may work such as "((?![unwanted string]).)+", but these are hard to get right/debug.
  - Also, negative lookbehinds (?<!) are not recommended. They need to be fixed length and immediately precede the pattern to work (wildcards tend to break the pattern).
* There may be cases where you need to add test files manually. This may ask for precise pattern because not all files ending with “test” will be tests (for example,“latest”).
  - “.\*/[^/]*Test(s)?.java"  (anything in the last folder/after the last “/” ending with Test.java or Tests.java)
  - “.\*/[a-z0-9-_]*Test[.]java” (camelCase in the final folder)


## Open Source Health

**Note: This requires a [Sigrid license for Open Source Health](https://www.softwareimprovementgroup.com/capabilities/sigrid-open-source-health/). Without this license, you will not be able to see security results in Sigrid.**

Open Source Health allows you to scan all open sources libraries used by your system, and identify risks such as security vulnerabilities or heavily outdated libraries.

    dependencychecker:
      enabled: true
      blocklist: []
      transitive: false
      exclude:
        - ".*/scripts/.*"
        
The `dependencychecker` section supports the following options:

| Option name  | Required? | Description                                                                                    |
|--------------|-----------|------------------------------------------------------------------------------------------------|
| `enabled`    | Yes       | Set to `true` to enable Open Source Health analysis.                                           |
| `blocklist`  | Yes       | List of library names that should not be scanned. Typically used to ignore internal libraries. |
| `transitive` | No        | When true, also scans the dependencies of your dependencies. Defaults to false.                |
| `exclude`    | No        | List of file/directory patterns that should be excluded from the Open Source Health analysis.  |

## Security

**Note: This requires a [Sigrid license for Software Security](https://www.softwareimprovementgroup.com/solutions/sigrid-software-security/). Without this license, you will not be able to see security results in Sigrid.**

Sigrid uses a combination of its own security checks and security checks performed by third party tools. It then combines the results, benchmarks them, and reports on the overall results.

    thirdpartyfindings:
      enabled: true
      exclude:
        - ".*/scripts/.*[.]sh"
          
The `thirdpartyfindings` section supports the following options:

| Option name | Required? | Description                                                                         |
|-------------|-----------|-------------------------------------------------------------------------------------|
| `enabled`   | Yes       | Set to `true` to enable security analysis.                                          |
| `exclude`   | No        | List of file/directory patterns that should be excluded from the security analysis. |

## Architecture Quality

**Note: This requires an Architecture Quality license, which is currently restricted to a limited customer beta. Without this license, you will not be able to see security results in Sigrid.**

    architecture:
      enabled: true
      
Architecture Quality also requires the repository history to be included in the upload. This requires the `--include-history` option to be enabled in the [Sigrid CI client script](client-script-usage.md).
      
The `architecture` section supports the following options:

| Option name           | Required? | Description                                                                                    |
|-----------------------|-----------|------------------------------------------------------------------------------------------------|
| `enabled`             | Yes       | Set to `true` to enable architecture quality analysis.                                         |
| `model`               | No        | Version of the SIG Architecture Quality Model to use. Defaults to latest version.              |
| `exclude`             | No        | List of exclude patterns that applies only to Architecture Quality, not globally.              |
| `add_dependencies`    | No        | List of manually added dependencies on top of the ones detected automatically by the analysis. |
| `remove_dependencies` | No        | List of dependencies that manually overrides the analysis and removes them from the results.   |

The `add_dependencies` and `remove_dependencies` fields expect a value in the format `name -> name`. You can use the same name that you see in Sigrid. This works for both file dependencies and component dependencies.

## Sigrid metadata

`sigrid.yaml` is used for *analysis* configuration. It is also possible to configure Sigrid *metadata*. See the [Sigrid metadata](../organization-integration/metadata.md) section for the various ways you can update this metadata.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.
