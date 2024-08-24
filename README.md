# Pass Tangle
```Pass Tangle``` is password managing, ```GUI``` software. It keeps your passwords safe with ```AES``` encrypting in user-friendly form factor, and retro styled interface.

<br>

```markdown
+ NOTE, works only in Windows OS
```

<br>

- Automatic opened software recognition

> Pass Tangle automatically detect current opened software and provide avalaible saved login credentials for this software
- Automatic browser tab recognition for 12 most popular web browsers

> Pass Tangle automatically recognise opened sites, for example if Facebook is opened in Google Chrome, software will recognise it, and asssign credentials to correct site

> Supported browsers: ```Google Chrome```, ```Chrominium```, ```Microsoft Edge```, ```Opera```, ```Opera GX```, ```Firefox```, ```Vivaldi```, ```Brave```, ```Tor Browser```, ```Duck Duck Go```, ```Maxthon```, ```Yandex Browser```

> NOTE, You can add more browsers on your own by modifying 10th, and 12th line in ```taskGrabber.py```
- Strong Encryption

> AES encryption from cryptography Python module. Encryption key stored on external USB drive, later referred as encryption key
- Fully offline

> That means, only you have credentials data. ```No one else!``` All data is encrypted on your own drive

> Don't worry, you can [copy your credentials to another devices](#transfer-or-copy-credentials-data), so you won't loose them, if your PC goes down.

# Setup
To use ```Pass Tangle``` you need to download and install [python](https://www.python.org/downloads/).

After installing ```python```, run following commands to install required dependencies
```
pip install PyQt5
pip install pywin32
pip install pywinauto
```

Run **```setup.pyw```** and setup the ```USB key``` to start using ```Pass Tangle```

> It's recomended to choose more than one ```USB Key``` in the setup. If you forget to do this, you can also [add the key manually](#manually)

# Usage
To use ```Pass Tangle``` just run **```pass_tangle.pyw```**

You will we presented with this window, which always stays on top

![](https://github.com/sbartoszuk/pass-tangle/blob/main/readme_images/1.png?raw=true)

- Drag the window by grabbing it by the black part
- Click the lock to show or hide the ```main panel```

![](https://github.com/sbartoszuk/pass-tangle/blob/main/readme_images/2.png?raw=true)

In this panel you will see current focused program / browser tab, and some buttons

> if the opened program window isn't written here, try just clicking on this window

<br>

- ```Show button```
- ```Add button```

<br>

Theese buttons refer to program / browser tab written above.

> ```Show button``` will show only credentials for this specific platform. Eg. If "gmail" is displayied in main panel, show button will only show credentials for "gmail", no for other platforms

<br>

> ```Add button``` will add credentials assigned to program / browser tab displayied above. You can add as many login credentials as you want to each platform. Eg. you can add 10 different logins and passwords to Gmail accounts

<br>

- ```More button```

<br>

This button refer to all programs / browser tabs

> ```More button``` shows you all credentials to all platforms, with ability to delete them, or edit them

## Creating More USB Keys
It's safe to create more than one ```USB Key``` (if you loose your only one, you can't access encrypted credentials)

With following methods each key will be automatically recognised, and work like normal ```USB key```

### ```Automatically```
In setup proceess you can select multiple usb's to make a key to, that's the ```RECOMENDED``` method.

### ```Manually```
On your ```USB Key``` you will find **```decrypt.cdk```** file

Copy it to another USB drive and you're good to go

<br>

- ```NOTE``` the drive to use must be ```USB```! Hard drive won't work

## Transfer or Copy Credentials Data
You can easily create a backup for your credentials data or move it across different devices with ```Pass Tangle``` on it

All credentials data is located at ```data``` folder in location as presented below

```markdown
pass_tangle/
|
├── assets/
|
├── data/              <------- here
|
├── modules/
|
├── pass_tangle.pyw
|
└── setup.pyw
```

### Create Backup
Copy **```data```** folder with all it's contents to a safe place (recomended to a different drive)

### Transfer to another device
Transfer the **```data```** floder with all it's contents to another device with ```Pass Tangle``` in a folder scheme presented above (in pass_tangle folder)
