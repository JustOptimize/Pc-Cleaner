# PC Cleaner
PC Cleaner is a simple tool to clean your PC from junk files. It is written in Python and uses a configuration file to determine which files/directories or registry keys to delete.

## Installation
1. Clone this repository
2. Edit the configuration file `config.json` to your needs
3. Run `python cleanUp.py`

## Configuration
### Files
The `files` section of the configuration file contains a list of files and directories to delete. The paths are relative to the current working directory. The `files` section looks like this:
```json
"files": [
{
	"item": "%APPDATA%\\Microsoft\\Windows\\Recent\\",
	"type": "REMOVESELF"
}]
```
The `item` key contains the path to the file or directory. The `type` key contains the type of the item. The following types are supported:
- `REMOVESELF`: Remove the file or directory itself
- `RECURSE`: Remove the file or directory and all its contents
- `WILDCARD`: Remove all files matching the wildcard pattern

### Services
The `services` section of the configuration file contains a list of services to stop before the cleanup (in order to delete files that are in use).

The `services` section looks like this:
```json
"services": [
	"Windows Search"
]
```

### Registry
The `registry` section of the configuration file contains a list of registry keys to delete. The `registry` section looks like this:
```json
"regKeys": [
	"HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU"
]
```

### Other
- cleanJournals: If set to `true`, the Windows Event Logs will be cleared
- restartPc: If set to `true`, the PC will be restarted after the cleanup