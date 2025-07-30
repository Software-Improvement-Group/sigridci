# Copyright Software Improvement Group
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
from zipfile import ZipFile, ZIP_DEFLATED

from .publish_options import PublishOptions
from .repository_history_exporter import RepositoryHistoryExporter
from .upload_log import UploadLog


class SystemUploadPacker:
    MAX_UPLOAD_SIZE_MB = 500
    ALWAYS_INCLUDE = (RepositoryHistoryExporter.LIGHTWEIGHT_HISTORY_EXPORT_FILE)
    EXCLUDE_EXTENSIONS = (".7z", ".amr", ".avi", ".bil", ".bmp", ".db", ".dmp", ".doc", ".docx", ".exe", ".f4v", ".gif",
                          ".gz", ".heic", ".ico", ".ipa", ".iso", ".jpeg", ".jpg", ".m4a", ".mkv", ".mpeg", ".mpg", ".mpl",
                          ".mov", ".mp3", ".mp4", ".msi", ".odf", ".odp", ".ods", ".odt", ".otf", ".pdb", ".pdf", ".png",
                          ".ppt", ".pptx", ".rar", ".rtf", ".sbn", ".shx", ".shp", ".svg", ".swf", ".tar", ".tgz", ".tiff",
                          ".ttf", ".wmv", ".woff", ".woff2", ".xls", ".xlsm", ".xlsx", ".zip")

    DEFAULT_EXCLUDES = [
        "$tf/",
        "coverage/",
        "build/",
        "dist/",
        "node_modules/",
        "sigridci/",
        "sigrid-ci-output/",
        "target/",
        ".angular/",
        ".git/",
        ".gitattributes",
        ".gitignore",
        ".gradle/",
        ".idea/",
        ".m2/",
        "m2/repo/",
        ".mendix-cache/",
        ".nx/",
        ".pip-cache/",
        ".pip-packages/",
        ".terraform/",
        ".yarn/"
    ]

    def __init__(self, options: PublishOptions):
        self.options = options

    def prepareUpload(self, outputFile):
        zipFile = ZipFile(outputFile, "w", ZIP_DEFLATED)
        hasContents = False

        if self.options.includeHistory:
            historyExporter = RepositoryHistoryExporter()
            historyExporter.exportHistory(self.options.sourceDir)

        for root, dirs, files in os.walk(self.options.sourceDir):
            for file in sorted(files):
                filePath = os.path.join(root, file)
                if (
                    file != outputFile
                    and os.path.exists(filePath)
                    and not self.isExcluded(filePath)
                    and self.isIncluded(filePath)
                ):
                    relativePath = os.path.relpath(os.path.join(root, file), self.options.sourceDir)
                    hasContents = True
                    if self.options.showUploadContents:
                        UploadLog.log(f"Adding file to upload: {relativePath}")
                    zipFile.write(filePath, relativePath)

        zipFile.close()

        self.checkUploadContents(outputFile, hasContents)

    def checkUploadContents(self, outputFile, hasContents):
        uploadSizeBytes = os.path.getsize(outputFile)
        uploadSizeMB = max(round(uploadSizeBytes / 1024 / 1024), 1)
        UploadLog.log(f"Upload size is {uploadSizeMB} MB")

        if uploadSizeMB > self.MAX_UPLOAD_SIZE_MB:
            raise Exception(f"Upload exceeds maximum size of {self.MAX_UPLOAD_SIZE_MB} MB")
        elif not hasContents:
            print(f"No code found to upload, please check the directory used for --source")
            sys.exit(1)
        elif uploadSizeBytes < 50000:
            UploadLog.log("Warning: Upload is very small, source directory might not contain all source code")

    def isExcluded(self, filePath):
        normalizedPath = filePath.replace("\\", "/")

        if normalizedPath.lower().endswith(self.EXCLUDE_EXTENSIONS):
            return True

        excludePatterns = self.DEFAULT_EXCLUDES + (self.options.excludePatterns or [])
        return any(exclude for exclude in excludePatterns if exclude != "" and exclude.strip() in normalizedPath)

    def isIncluded(self, filePath):
        includePatterns = self.options.includePatterns or []
        if len(includePatterns) == 0 or includePatterns == [""] or filePath.endswith(self.ALWAYS_INCLUDE):
            return True
        normalizedPath = filePath.replace("\\", "/")
        return any(include for include in includePatterns if include != "" and include.strip() in normalizedPath)
