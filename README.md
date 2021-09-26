# wlt_connector
中科大网络通授权脚本

## Initialization
Before using this script, you should edit `[user]` field in `connect.ini` with your own wlt account.

You can also edit `[set]` field in it to set your own preference. 

After your editing, you can use `python connect.py -l` to find out if there is any error in your settings.

**Note: Configurations will also be displayed with `-h/--help` command, but error checking will only run with`-l/--list` command**

## Usage
If you fully configured all settings you want online or in `connect.ini`, you can easily use this script by simply `python connect.py`.

Meanwhile, all fields in `connect.ini` are supported in command line for temporarily use. You can use `python connect.py -h` to see more.
