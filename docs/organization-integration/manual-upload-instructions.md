# Manually uploading source code using the SIG Upload Portal

**Note for when you do not have a Sigrid account yet:** In most cases, source code represents a significant financial
or strategic value. SIG cannot accept responsibility for received source code without an established NDA or contract.
That is why SIG advises to have a Non Disclosure Agreement (NDA) in place before uploading source code.
We can send you an NDA upon request.
{: .attention }

The process for manual uploads is as follows:

1. Determine what source code to upload.
2. Archive all files into a ZIP file. Refer to our [instructions for creating a zip file for your system](#creating-a-zip-file-for-your-system).
3. Open the portal by typing `https://uploadportal.softwareimprovementgroup.com` in the address bar of your web browser
4. Check if the connection is indeed secure: Your browser displays a symbol representing a closed lock.
   You may verify that the secure connection is indeed with the Software Improvement Group by checking the validity of the certificate. Should you require assistance in validating the secure connection, please do not hesitate to contact us.
5. Fill in your contact information and the upload details
6. Click on 'Choose file'
7. Select the file you want to upload. The size of one single upload is limited to 2 GB.
8. Click on 'Upload'
9. Wait for the system to finalize the file transfer (this may take some time, depending on network traffic and size of the file)
10. The system returns with a message and provides the opportunity to upload another file
11. SIG receives the files and validates the upload.
12. SIG informs you and involved SIG employees about the successful upload.

## Creating a ZIP file for your system

Prefer regular ZIP files, and avoid nested ZIP files. The following example can be used to create a ZIP file on the
command line using Linux, MacOS, or WSL:

```
git clone https://github.com/LeaVerou/awesomplete.git code
cd code
git --no-pager log --date=iso --format='@@@;%H;%an;%ae;%cn;%ce;%cd;%s' --numstat --no-merges > git.log
git --no-pager log --date=iso --format='@@@MERGE;%H;%an;%ae;%cn;%ce;%cd;%s' --merges >> git.log
rm -rf .git
zip -r your-project.zip .
```

The following example can be used with Windows PowerShell to create a ZIP file:

```
git clone https://github.com/LeaVerou/awesomplete.git code
cd code
git --no-pager log --date=iso --format='@@@;%H;%an;%ae;%cn;%ce;%cd;%s' --numstat --no-merges | Out-File -FilePath git.log -Encoding 'utf8'
git --no-pager log --date=iso --format='@@@MERGE;%H;%an;%ae;%cn;%ce;%cd;%s' --merges | Out-File -FilePath git.log -Encoding 'utf8' -Append
Remove-Item -Recurse -Force .git
cd ..
Compress-Archive -Path code\* -DestinationPath .\your-project.zip
```

The only thing you need to change in these examples is to replace the URL of the repository with your own system's URL.

This will clone a Git repository and then create a ZIP file containing both the source code and the change history.
The latter is used for Sigrid's [architecture quality](../capabilities/architecture-quality.md) analysis.
We create a log file containing this change history, and e deleted the `.git` directory afterwards (to make the
ZIP file smaller and faster to upload).

Please make sure that you use the UTF-8 character encoding when creating the ZIP file.

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you
may have after reading this documentation or when using Sigrid.
