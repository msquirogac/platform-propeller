# Propeller for PlatformIO

## Installation

 1. Install [Visual Studio Code](https://code.visualstudio.com/)
 2. Install [PlatformIO Extension for VSCode](https://platformio.org/platformio-ide)
 3. Install Propeller platform:
	* From the GUI
		* Open PlatformIO Home
		* Go to Platforms -> Advanced Installation
		* Paste repository link https://github.com/msquirogac/platform-propeller
		* Click Install
	* From console command
	~~~
	platformio platform install https://github.com/msquirogac/platform-propeller
	~~~

4. Create PlatformIO project and configure a platform option in [platformio.ini](http://docs.platformio.org/page/projectconf.html) file:

### Stable version

```ini
[env:stable]
platform = propeller
board = ...
...
```

### Development version

```ini
[env:development]
platform = https://github.com/msquirogac/platform-propeller
board = ...
...
```

## Examples
* [blank](https://github.com/msquirogac/platform-propeller/tree/master/examples/blank)
* [hello](https://github.com/msquirogac/platform-propeller/tree/master/examples/hello)
* [toggle-c++](https://github.com/msquirogac/platform-propeller/tree/master/examples/c%2B%2B_toggle)
* [toggle-lmm](https://github.com/msquirogac/platform-propeller/tree/master/examples/lmm_toggle)

## TODO

 - [x] Add support for Windows and macOS
 - [ ] Add support for GDB
 - [x] Add SimpleIDE version of the compiler tools
 - [ ] Add support for **spin** to **C** convertion tools
 - [ ] Improve documentation

## Configuration

~~Please navigate to [documentation](http://docs.platformio.org/page/platforms/propeller.html).~~ TODO


