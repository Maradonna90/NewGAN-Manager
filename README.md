![MacOS](https://github.com/Maradonna90/NewGAN-Manager/workflows/MacOS/badge.svg)
![Linux](https://github.com/Maradonna90/NewGAN-Manager/workflows/Linux/badge.svg)
![Windows](https://github.com/Maradonna90/NewGAN-Manager/workflows/Windows/badge.svg)

# Main Contributors to NewGAN
[Maradonna](https://community.sigames.com/profile/50821-maradonna/) (gestalt): Coding and image generation  
[HRiddick](https://sortitoutsi.net/user/profile/137954): Image cleaning and post processing  
[Krysler76](https://community.sigames.com/profile/157461-krysler76/): FM views hacking  

Most of us are active on several FM platforms under the same Nicknames.

# Installation Guide
I tried to make the whole installation process as much one-click and go as possible. Unfortunately providing a cross-platform app without managing a codebase for every supported platform is impossible to me. Therefore some small adjustments may be needed, depending on your system.

## Windows
1. Download the .msi Installer and go through the installtion process
2. Go to the NewGAN installation folder (e.g `C:\Program Files (x86)/NewGAN Manager`)
	1. Move the `app\.config\` folder to the NewGAN installation folder from step 2.
	2. Move the `app\views\` folder to your Football Manager userfolder `My Documents\Sports Interactive\Football Manager 20XX\`

## Linux
1. Download the .zip file and extract it.
2. give the AppImage executable rights with `sudo chmod +x *.AppImage`

## Mac
TBD

# Troubleshooting
If the app crashes for some reason open an issue and please provide the `newgan.log` file. It helps to figure where exactly the app crashed combined with your description.

## newgan.log on Windows
On Windows the log file is created in the installation directory. It should be under `C:\Program Files (x86)/NewGAN Manager`

## newgan.log on Linux
On Linux the log file is created wherever you place the `NewGAN_Manager-*.AppImage` file and execute it.

## newgan.log on Mac
TBD

# Roadmap
* [ ] integrate Kryslers view for better mapping
