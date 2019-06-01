# BFU - Better File Upload - Desktop

## Installation

Requirements:
- Windows
- Python 3.x
- Admin privileges

In order for the desktop hooks to be registered, BFU-Desktop needs to add 3 keys to the Windows registry. To perform this **YOU NEED ADMIN PRIVILEGES**. Follow the following steps:
1. Clone/Download this repository
2. Move the whole directory to the place, in which you want it installed. **Keep all files in the same directory**
3. Right-click the *install.bat* -> Run as administrator
4. Confirm the prompt
5. **Done**

If there were no error during the installation, you should see two new options popping up when right-clicking files, and one new options when right-clicking folder:

- BFU - Upload (Uploads the given file, copies the download URL to your clipbaord)
- BFU - Copy path (Copies the file/folder path to your clipboard)

After uploading your first file, a settings file will be generated. In that settings file you may change the API Key from the default public key to a private one, which you can aquire from here:  
https://file-upload.vi-home.de/api_key.php  
The API Key needs to have upload privileges, obviously.

## Access

All files submitted via the public API Key will be visible on:  
https://file-upload.vi-home.de/download?fid=\<fileID\>
