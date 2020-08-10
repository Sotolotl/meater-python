# meater-python

Python wrapper for the Apption Labs Meater cooking probe using v1 of their public API.

## Installation

`meater-python` can be installed from either PyPi or can be installed manually by cloning the GitHub repository.

### TL;DR installation

```pip install meater-python```

### Manual installation

First, clone the GitHub repository:
```git clone https://github.com/Sotolotl/meater-python.git```

Enter the newly created `meater-python` directory and run:
```pip install .```

This should install `meater-python` on your system. You can use it in your own Python scripts like so:

```python
import meater
```

## Usage

To get started, first import the `MeaterApi` class from `meater`.

### Initializing

```python
from meater import MeaterApi
api = MeaterApi()
```

The code above initializes the cooker into the `api` variable. Before any information can be obtained, you need to authenticate with the api. In the current version of `meater-python`, only email/password authentication is supported. You can authenticate with the API like so:

```python
api.authenticate('<your email address>','<your password>')
```

### Getting Probe States

Once you have authentiated with the API, you can get information about all available probes like so:

```python
devices = api.get_all_devices()
```

This will populate the `devices` variable with a list of all the available device objects.

**NOTE**: Only devices that are actively connected to Meater Cloud are available through the API. Once a probe has been disconnected for a few minutes, it is no longer returned by the API.

A specific device can be queried by the API like so:

```python
device = api.get_device('<your device ID>')
```

The device ID should be a 65 character long alphanumeric string. To obtain the device ID, make a call to `api.get_all_devices` while the device is connected.

**NOTE**: This method will throw an exception if the device cannot be found. This includes if the device is currently offline.

### MeaterProbe Object Attributes

The following arrtibutes are available on the MeaterProbe object
| Attribute | Type | Description |
| --- | --- | --- |
| `id` | str | The ID of the device |
| `internal_temperature` | float | The internal temperature reading of the probe in ℃ |
| `ambient_temperature` | float | The ambient temperature reading of the probe in ℃ |
| `time_updated` | datetime | The time that the probes values were last sent to the Meater cloud |
| `cook` | MeaterCook (see below) | A MeaterCook class containing information about the current cook. If no cook is running, this will be `None` |

The following attributes are available on the MeaterCook object
| Attribute | Type | Description |
| --- | --- | --- |
| `id` | str | The ID of the cook |
| `name` | str | The name of the cook |
| `state` | str | The current state of the cook |
| `target_temperature` | float | The target temperature for this cook in ℃ |
| `peak_temperature` | float | The peak temperature so far for this cook in ℃ |
| `time_remaining` | int | The time remaining for this cook in seconds |
| `time_elapsed` | int | How long has elapsed since the start of the cook in seconds |

## Troubleshooting

Devices will only be returned after the following criteria is met. There may be a delay between the MEATER Cloud seeing your device and it being returned in this endpoint.

* Device must be seen by the MEATER Cloud. Ensure you've completed a cook while connected to MEATER Cloud.
* The MEATER app or Block must have an active Bluetooth connection with the device.
* The MEATER app or Block must have an active MEATER Cloud connection.

If you make requests to the Meater API too quickly, you may be subject to rate-limiting. The reccomended rate is 2 requests per 60 seconds, and the maximum is 60 requests per 60 seconds.

Requests are automatically slowed down once 10% of rate limit is reached, to 1.0 second per request.
