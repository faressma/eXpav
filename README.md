### Bluetooth connection
#### First connection
Before using python program to control remote car, you have to firstly pairing your device with your desired car. 
For this purpose, you can either select the desired car with your Bluetooth control panel, or select any solution that can perform it.

On Fedora and Ubuntu distributions, you can use `bluetoothctl` CLI program for example.

###### bluetoothctl
Run `bluetoothctl` in your CLI:
```
bluetoothctl
```

To detect all the bluetooth devices around:

```
scan on
```
To pair with the desired device:
```
pair [MAC address]
```

You can skip scanning step if you already know the MAC address.

If you don't get any trouble, you can exit `bluetoothctl`:
```
exit
```

Then run the python program.

###### Troubleshootings

If you don't succeed to connect (the step after pairing), it might comes from your Bluetooth daemon not running in compatibility mode. 
On Fedora distribution, it's a known problem.

To run your Bluetooth deamon in compatibility mode, open your bluetooth.service configuration file. You can locate it running `systemctl status bluetooth`. Usually, it's located in `/usr/lib/systemd/system/bluetooth.service`.

Your `ExecStart` variable should have the `-C` option at the end of the line:
```
ExecStart=/usr/libexec/bluetooth/bluetoothd -C
```
If not, add it.

Then, restart your Bluetooth daemon:
```
systemctl retsart bluetooth
```