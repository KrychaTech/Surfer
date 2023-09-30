# Surfer
Surfer is a web browser, written in Python. It uses PyQT5 WebEngine to display websites, and the keyboard module to recognize hotkeys.
The core philosophy of this browser is _Keyboard-driven Minimalism._ This browser also has a customizable website blocking list, which is configured to block
websites that destroy a workflow.<br />

  
![Screenshot](minimalist_browser1.png)
## Arguments
This browser should be launched from the terminal. When launching the browser, the user can specify arguments. The list of acceptable arguments can be found below.
| Argument      | Short Name | Function                                                                              |
| ------------- |------------| --------------------------------------------------------------------------------------|
| --url URL     | -u         | Launches the specified URL in the browser.                                            |
| --query QUERY | -q         | Searches for the specified query on the specified search engine [default: duckduckgo] |
| --dark_mode   | -dm        | Forces Dark Mode on all websites.                                                     |
| --google      | -g         | Makes Google the default search engine for this session.                              |
| --windowed    | -w         | Runs the browser in Windowed mode, rather than in fullscreen.                         |
| --tabbed      | -t         | Adds the ability to add tabs. [EXPERIMENTAL!]                                         |
| --incognito   | -i         | Makes the browser launch a clear profile.                                             |

## Shortcuts
This browser uses keyboard shortcuts to control the program. The default modifier key is "win" (Windows Key). As such, this list is for a shortcut of win+key.
| Key         | Function                                                                                              |
| ----------- |-------------------------------------------------------------------------------------------------------|
| J           | Makes the browser go back one page.                                                                   |
| X           | Closes the browser.                                                                                   |
| R           | Goes back to the search engine page.                                                                  |
| Left Arrow  | If tabbed is set to True, this shortcut makes the browser go to a previous tab.                       |
| Right Arrow | If tabbed is set to True, this shortcut makes the browser go to the next tab.                         |
| T           | if tabbed is set to True, this shortcut creates a tab which adds the current website to the tab list. |
| Y           | if tabbed is set to True, this shortcut clears the tab list.                                          |
| U           | Copies the current URL into the clipboard.                                                            |

Since release v1.1.0 this shortcuts can be customized by editing config.ini.

## Compile your own PyQt5 or expect hell!
_Well, the term hell isn't really spot on,_ however if you dont compile your own PyQt5 Webengine, you can expect that videos will not play on websites. A guide on how to do so can be found [here](https://doc.bccnsoft.com/docs/PyQt5/installation.html). Compiling PyQT5 on Windows is a nightmare of itself, yet you need to do it for the sake of video playback.

### Like this project? consider buying me some tea!
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/G2G0POBDD)
