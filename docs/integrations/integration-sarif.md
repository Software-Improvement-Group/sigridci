# Importing custom findings into Sigrid using SARIF

Sigrid is capable of combining findings from multiple sources. In addition to Sigrid's own findings and existing
third party tool integrations, it is also possible to import your own custom findings into Sigrid. This is done using
the [SARIF](https://sarifweb.azurewebsites.net) format, which is a standard file format commonly used for
interoperability between tools.

Sigrid will automatically import custom findings from all files that meet the following conditions:

- The file is located in the `.sigrid` directory, relative to the root of the repository.
- The file name ends with `.sarif`.

You would typically generate these SARIF files with custom findings in your pipeline. Because Sigrid also runs in
your pipeline, it will automatically pick up these files and will publish them to Sigrid.

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues 
you may have after reading this documentation or when using Sigrid.
