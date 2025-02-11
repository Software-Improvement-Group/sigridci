# Uploading your source code to Sigrid

There are multiple ways to upload your source code. The best and recommended way is to integrate Sigrid into your development environment using Sigrid CI. However, SIG also supports alternative upload channels for situations where Sigrid CI cannot be used.

This documentation covers cloud-based Sigrid. On-premise Sigrid requires integration with your development platform, which is explained in the section about [on-premise analysis configuration](../organization-integration/onpremise-analysis.md).
{: .attention }

<sig-toc></sig-toc>

## Sigrid CI: Pipeline integration

Integrating Sigrid CI into your pipeline allows you to automatically publish your source code to Sigrid after every change. It also allows you to receive feedback from Sigrid within your development environment.

### The general steps to start with CI:

- SIG will create an empty Sigrid and a first user per customer.
- The first user needs to create a [PAT token](../organization-integration/authentication-tokens.md).
- Based on your environment the respective Sigrid CI jobs will need to configured with the above token.
- Please check if your firewall allows outbound traffic to Sigrid-says.com [link to the FAQ page](../capabilities/faq.md)

See the "Sigrid CI" section in the menu for an overview of supported platforms. The documentation also explains how Sigrid CI fits into various [development processes and workflows](../sigridci-integration/development-workflows.md).

## Uploading source code using SFTP

The preferred method to upload source code is Sigrid CI, but SIG also offers SFTP uploads for situations where Sigrid CI cannot be used.

The upload server for SFTP uploads is **portal.sig.eu**. To make sure your uploaded files are secure, you will not receive full shell access to our upload server. Your account is jailed, such that other users of the upload server don't know its existence and cannot access it. Files uploaded to your account will be removed from your account after (at most) 3 days and removed from our backup after (at most) 6 weeks. The backup is encrypted using AES256. The disk your account resides on is encrypted using AES256 as well.

The default folder you connect to is referred to as your home folder. You are free to create new folders in your home folder, but please be aware they will be removed after 3 days, just like uploaded files.

The requirements below must be fulfilled to ensure uploaded files can be processed automatically and correctly:

- Create one ZIP file for each source code snapshot. Refer to the list of [supported file formats](#supported-sftp-file-formats) and [instructions for creating a ZIP file for your ststem](#creating-a-zip-file-for-your-system).
- Keep the internal structure of the ZIP file consistent across snapshots.
- Add the date of the source code snapshot to the file name, in the format `yyyymmdd`.
- Use the following naming convention for files you upload: `<application name>–<date>.zip` (for example: `myportal–20200922.zip`).

### Supported SFTP file formats

- Regular ZIP files
- Password-protected ZIP files (with a file name of `*.pzip`)
- GZIP
- RAR (v1.5 to v4.0)
- TAR
- TAR.GZ

For file formats other than ZIP we do not support password protection. If you want to upload password-protected ZIP files, contact our support at [support@softwareimprovementgroup.com](mailto:support@softwareimprovementgroup.com) to inform us of the password so it can be configured on our side. Your password will be stored in an encrypted format.

### SFTP key authorization

You need to generate an SSH authentication key to connect to the upload server. The public part of this key needs to be whitelisted by the upload server. The SSH key you generate can be either an:

- RSA key (of at least 2048 bits long)
- ECDSA key (of at least 256 bits long)
- ED25519 key (of at least 256 bits long)

When in doubt, please use RSA.

### SFTP/SCP upload server details

You can verify the authenticity of the upload server by checking its public host key fingerprint. This fingerprint should be visible when connecting to the upload server for the first time, and, depending on the type of authentication used, should be equal to one of the following:

- RSA fingerprint: `4096 SHA256:jGf883nbewCO69bbK3lur/0ZAi0T4d6+P1ySc0NRVpU`
- ECDSA fingerprint: `256 SHA256:/TfYO8xzMn0+IqjS70Ig4sHdMfQWjD34FNoIbJxQTZQ`
- ED25519 fingerprint: `256 SHA256:4Ih8DOiO8mj6e8S8GOyK7tjjmHbFkvcpqXRyLWq+jvg`

The SFTP/SCP protocol connects to port 22 on our upload server, so your firewall should allow outbound traffic to port 22.

### SFTP key exchange

To secure this account, please send your SIG contact the following:

- Your name
- Email address
- Phone number (to arrange the key exchange, and in case of problems)
- The public part of an SSH key pair (for each computer you intend to upload from)

Both OpenSSH and SSH2 public keys are supported. Please use one key pair per computer and protect the private part of your key properly. After receiving this information, you will receive an account name linked to the supplied SSH key.

### SFTP key creation

If you are uploading from a Unix, Linux or macOS system, then you probably are in possession of an SSH key already, it's most likely stored in the `id_rsa.pub` file in the `.ssh` folder in the home folder of the account you use to upload your files. You can use `ssh-keygen -t rsa` to create a key if it isn't. It's safe to answer all questions with an 'enter'.

If you are uploading from Windows, you likely need to create a new key. You can, for example, use the [puttygen3](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) application to accomplish this.

### Uploading to portal.sig.eu via scp

Connections to our upload server can be made using an SCP client, such as [WinSCP](http://winscp.net/eng/index.php) for Windows, or the command line utility `scp` for Unix, Linux and macOS, which is part of the [OpenSSH](http://www.openssh.com) suite.

Below an example for the secure copy command, which refers to a private key, the zip file to be uploaded and 'your-upload-account' that you will receive from Sigrid support.

```
scp -i ~/.ssh/id_rsa system-name-<yyyymmdd>.zip your-upload-account@portal.sig.eu:
```

## Manually uploading source code using the SIG Upload Portal

**Note for when you do not have a Sigrid account yet:** In most cases, source code represents a significant financial or strategic value. SIG cannot accept responsibility for received source code without an established NDA or contract. That is why SIG advises to have a Non Disclosure Agreement (NDA) in place before uploading source code. We can send you an NDA upon request.

The process for manual uploads is as follows:

1. Client determines what source code to upload.
2. Client archives all files into a ZIP file. Refer to our [instructions for creating a zip file for your system](#creating-a-zip-file-for-your-system).
3. Client uploads file(s) to SIG using SIG upload facility. See below for details.
4. SIG receives files and validates the upload.
5. SIG informs client and involved SIG employees about successful upload.

### The SIG Upload Portal for manual uploads

The upload facility is a secure website. No login is required. The size of one single upload is limited to 2 GB. The URL is [uploadportal.softwareimprovementgroup.com](https://uploadportal.softwareimprovementgroup.com/).

The usage of the portal is straightforward:

1. Open the portal by typing `https://uploadportal.softwareimprovementgroup.com` in the address bar of your web browser
2. (optional) Check if the connection is indeed secure:
   - Your browser displays a symbol representing a closed lock
   - You may verify that the secure connection is indeed with the Software Improvement Group by checking the validity of the certificate. Should you require assistance in validating the secure connection, please do not hesitate to contact us.
3. Fill in your contact information and the upload details
4. Click on 'Choose file'
5. Select the file you want to upload
6. Click on 'Upload'
7. Wait for the system to finalize the file transfer (this may take some time, depending on network traffic and size of the file)
8. The system returns with a message and provides the opportunity to upload another file

## Creating a ZIP file for your system

If you use Sigrid CI, this ZIP file is created automatically and you can skip this section. If you are using SFTP or manual uploads, you will need to create the ZIP file yourself using these guidelines.

Prefer regular ZIP files, and avoid nested ZIP files. The following example can be used to create a ZIP file on the command line using Linux, MacOS, or WSL:

```
git clone https://github.com/LeaVerou/awesomplete.git code
cd code
git --no-pager log --date=iso --format='@@@;%H;%an;%ae;%cd;%s' --numstat --no-merges > git.log
rm -rf .git
zip -r your-project.zip .
```

The following example can be used with Windows PowerShell to create a ZIP file:

```
git clone https://github.com/LeaVerou/awesomplete.git code
cd code
git --no-pager log --date=iso --format='@@@;%H;%an;%ae;%cd;%s' --numstat --no-merges | Out-File -FilePath git.log -Encoding 'utf8'
Remove-Item -Recurse -Force .git
cd ..
Compress-Archive -Path code\* -DestinationPath .\your-project.zip
```

The only thing you need to change in these examples is to replace the URL of the repository with your own system's URL. 

This will clone a Git repository, and then create a ZIP file containing both the source code and the change history. The latter is used for Sigrid's [architecture quality](../capabilities/architecture-quality.md) analysis. We create a log file containing this change history, and afterwards we deleted the `.git` directory to make the ZIP file smaller and faster to upload. 

Please make sure that you use the UTF-8 character encoding when creating the ZIP file.

## What if something went wrong?

We recommend using Sigrid CI to publish your source code to Sigrid CI, since this approach is automated and therefore less error prone. If you run into issues while publishing your code it's best to [contact SIG's support team directly](#contact-and-support).

If you manually exported your Git history and it's not being picked up by Sigrid, refer to the [frequently asked questions for manually providing this data](../capabilities/faq-architecture.md#troubleshooting-issues-when-manually-publishing-your-repository-history).

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.
