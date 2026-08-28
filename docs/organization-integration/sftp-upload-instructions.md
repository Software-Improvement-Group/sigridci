# Uploading source code to Sigrid via SFTP

The upload server for SFTP uploads is **upload.sigrid-says.com**. To make sure your uploaded files are secure, you
will not receive full shell access to our upload server. Your account is jailed, such that other users of the upload
server don't know its existence and cannot access it.

Files uploaded to your account will be removed from your account after (at most) 3 days and removed from our backup
after (at most) 6 weeks. The backup is encrypted using AES256. The disk your account resides on is encrypted using
AES256 as well.

The default folder you connect to is referred to as your home folder. You are free to create new files in your home
folder, please be aware that we will keep the files for the last 4 upload dates.

The requirements below must be fulfilled to ensure uploaded files can be processed automatically and correctly:

- Create one ZIP file for each source code snapshot. Refer to the list of [supported file formats](#supported-sftp-file-formats) and [instructions for creating a ZIP file for your ststem](#creating-a-zip-file-for-your-system).
- Keep the internal structure of the ZIP file consistent across snapshots.
- Add the date of the source code snapshot to the file name, in the format `yyyymmdd`.
- Use the following naming convention for files you upload: `<application name>–<date>.zip` (for example: `myportal–20200922.zip`).

The following file formats are supported:

- Regular ZIP files
- GZIP
- RAR (v1.5 to v4.0)
- TAR
- TAR.GZ

## SFTP key creation

You need to generate an SSH authentication key to connect to the upload server. The public part of this key needs to be whitelisted by the upload server. You can send it to [SIG's support department](mailto:support@softwareimprovementgroup.com)

The SSH key you generate can be either an:
- RSA key (of at least 2048 bits long)
- ECDSA key (of at least 256 bits long)
- ED25519 key (of at least 256 bits long)

Please note we do not support the 'ssh-rsa' public key signature algorithm. Please use a modern SSH implementation that supports stronger algorithms such as:
- rsa-sha2-256
- rsa-sha2-512
- ssh-ed25519

## SFTP/SCP upload server details

You can verify the authenticity of the upload server by checking its public host key fingerprint. This fingerprint should be visible when connecting to the upload server for the first time, and, depending on the type of authentication used, should be equal to one of the following:

- RSA fingerprint: `4096 SHA256:1WMnU9ZOxldY+wfMoybHEQTknQJWd/SSGm0sv92TBDg`
- ECDSA fingerprint: `256 SHA256:fETp+2EViXNquhE5SxRJ5YBqwiTchFCo0Za0Z+yyv1o`
- ED25519 fingerprint: `256 SHA256:7AgpHOklx1QpkH88C2nbKFIyDuLhLQzUUnDrD95qF44`

The SFTP/SCP protocol connects to port 22 on our upload server, so your firewall should allow outbound traffic to port 22.

## SFTP key exchange

To secure this account, please send your SIG contact the following:

- Your name
- Email address
- Phone number (to arrange the key exchange, and in case of problems)
- The public part of an SSH key pair (for each computer you intend to upload from)

Both OpenSSH and SSH2 public keys are supported. Please use one key pair per computer and protect the private part of your key properly. After receiving this information, you will receive an account name linked to the supplied SSH key.

## SFTP key creation

If you are uploading from a Unix, Linux or macOS system, then you probably are in possession of an SSH key already, it's most likely stored in the `id_rsa.pub` file in the `.ssh` folder in the home folder of the account you use to upload your files. You can use `ssh-keygen -t rsa` to create a key if it isn't. It's safe to answer all questions with an 'enter'.

If you are uploading from Windows, you likely need to create a new key. You can, for example, use the [puttygen3](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) application to accomplish this.

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

## Uploading to upload.sigrid-says.com via scp

Connections to our upload server can be made using an SCP client, such as [WinSCP](http://winscp.net/eng/index.php) for Windows, or the command line utility `scp` for Unix, Linux and macOS, which is part of the [OpenSSH](http://www.openssh.com) suite.

An example of the secure copy command scp, which refers to a private key, the zip file to be uploaded and 'your-upload-account' that you will receive from Sigrid support. If you’re leaving out the remote file name, the ‘:’ at the end of ‘upload.sigrid-says.com’ is essential. The warning 'scp: remote fsetstat: Operation unsupported' is harmless.

```
scp -i ~/.ssh/id_rsa system-name-<yyyymmdd>.zip your-upload-account@upload.sigrid-says.com:
```

An example of sftp

```
% sftp <account>@upload.sigrid-says.com: <<< $'put <file>'
Connected to upload.sigrid-says.com.
Changing to: /.
sftp> put <file>
Uploading <file> to /<file>
<file>
```
### Viewing the uploaded files
- After uploading you can view the uploaded files to verify that the upload succeeded.
- Your uploads will be kept for 30 days. Uploads older than 30 days will be removed.


### Upload.sigrid-says.com is powered by SFTPGo
Link to the source code of [SFTPGo](https://github.com/drakkan/sftpgo)

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you
may have after reading this documentation or when using Sigrid.
