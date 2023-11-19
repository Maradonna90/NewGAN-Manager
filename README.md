![MacOS](https://github.com/imfulee/NewGAN-Manager/workflows/MacOS/badge.svg)
![Linux](https://github.com/imfulee/NewGAN-Manager/workflows/Linux/badge.svg)
![Windows](https://github.com/imfulee/NewGAN-Manager/workflows/Windows/badge.svg)

> The Linux build would build but I still couldn't make all the dependecies work well. 

# Main Contributors
**[Maradonna](https://community.sigames.com/profile/50821-maradonna/) (gestalt)**: Initiator, Coding, Image Generation  
**Samaroy**: Coordination, Image Generation  
**[HRiddick](https://sortitoutsi.net/user/profile/137954)**: Image Cleaning, Post Processing  
**[Krysler76](https://community.sigames.com/profile/157461-krysler76/)**: FM View Hacking  
**Ayal**: Image Generation  
**[Zealand](https://www.youtube.com/user/FMBaseOfficial)**: Image Generation  
**ZeBurgs**: Image Generation  

Most of us are active on several FM platforms under the same Nicknames.

# Support Me!
[![Donate with PayPal](https://i.imgur.com/CKweDND.png)](https://www.paypal.com/paypalme/marcojott90)

# Installation Guide
I tried to make the whole installation process as much one-click and go as possible. Unfortunately providing a cross-platform app without managing a codebase for every supported platform is impossible to me. Therefore some small adjustments may be needed, depending on your system.

## Windows
1. Download the Installer unzip it and run the .msi. Go through the installtion process
2. Move the `views\` and `filters/` folder to your Football Manager userfolder `My Documents\Sports Interactive\Football Manager 20XX\`

## Linux
1. Download the .zip file and extract it.
2. Give the AppImage executable rights with `sudo chmod +x *.AppImage`
3. Move the `views\` and `filters/` folder to your Football Manager userfolder.

## Mac
1. Find the downloaded file, which usually ends up in your `Desktop` or `Downloads` folder.
2. Double-click the `NewGAN-Manager-vX.X.X.DMG` file to mount it. A new `Finder` window showing its contents should appear.
3. If the window also contains a shortcut icon to `Applications`, drag and drop the app onto the shortcut.
4. If not, double-click the mounted volume on your desktop and drag the app icon from there to the `Applications` icon in the `Finder` sidebar.
5. In your `Finder` window add the Football Manager user folder (default: `~/Library/Application Support/Sports Interactive/Football Manager 20XX` to favorites
6. Move the `views\` and `filters/` folder to your Football Manager userfolder.


# Troubleshooting
If the app crashes for some reason open an issue and please provide the `newgan.log` file. It helps to figure where exactly the app crashed combined with your description.

## newgan.log on Windows
On Windows the log file is created in the installation directory. It should be under `%localappdata%\Programs\NewGAN-Manager\`

## newgan.log on Linux
On Linux the log file is created wherever you place the `NewGAN_Manager-*.AppImage` file and execute it.

## newgan.log on Mac
On Mac the log file is located at `/Applications/NewGAN-Manager.app/Contents/Resources/app_packages/`
