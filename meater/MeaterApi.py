import json
from datetime import datetime

class MeaterApi(object):
	"""Meater api object"""
	def __init__(self, aiohttp_session):
		self._jwt = None
		self._session = aiohttp_session
	
	async def get_all_devices(self):
		"""Get all the device states."""
		device_states = await self.__get_raw_state_all()

		devices = []

		for device in device_states:
			devices.append(self.__get_probe_object(device))

		return devices

	async def get_device(self, device_id):
		device_state = await self.__get_raw_state(device_id)
		return self.__get_probe_object(device_state)

	async def __get_raw_state_all(self):
		"""Get raw device state from the Meater API. We have to have authenticated before now."""
		if not self._jwt:
			raise Exception('You need to authenticate before making requests to the API.')

		headers = {'Authorization': 'Bearer ' + self._jwt}

		async with self._session.get('https://public-api.cloud.meater.com/v1/devices', headers=headers) as device_state_request:
			if device_state_request.status != 200:
				raise Exception('Error connecting to Meater')

			device_state_body = await device_state_request.json()
			if len(device_state_body) == 0:
				raise Exception('The server did not return a valid response')

			return device_state_body.get('data').get('devices')
		
	async def __get_raw_state(self, device_id):
		"""Get raw device state from the Meater API. We have to have authenticated before now."""
		if not self._jwt:
			raise Exception('You need to authenticate before making requests to the API.')

		headers = {'Authorization': 'Bearer ' + self._jwt}

		async with self._session.get('https://public-api.cloud.meater.com/v1/devices/' + device_id, headers=headers) as device_state_request:
			if device_state_request.status == 404:
				raise Exception('The specified device could not be found, it might not be connected to Meater Cloud')

			if device_state_request.status != 200:
				raise Exception('Error connecting to Meater')

			device_state_body = await device_state_request.json()
			if len(device_state_body) == 0:
				raise Exception('The server did not return a valid response')

			return device_state_body.get('data')

	async def authenticate(self, email, password):
		"""Authenticate with Meater."""
		
		headers = {'Content-Type':'application/json'}
		body = {'email':email, 'password':password}

		async with self._session.post('https://public-api.cloud.meater.com/v1/login', data = json.dumps(body), headers=headers) as meater_auth_req:
			if meater_auth_req.status != 200:
				raise Exception('Couldn\'t authenticate with the Meater API')

			auth_body = await meater_auth_req.json()
			
			jwt = auth_body.get('data').get('token') # The JWT is valid indefinitely...

			if not jwt:
				raise Exception('Could not authenticate with Meater')

			# Set JWT local variable
			self._jwt = jwt

			return True

	def __get_probe_object(self, device):
		cook = None

		if device.get('cook'):
			target_temp = 0

			cook = MeaterCook(device.get('cook').get('id'), device.get('cook').get('name'), device.get('cook').get('state'), device.get('cook').get('temperature').get('target'), device.get('cook').get('temperature').get('peak'), device.get('cook').get('time').get('remaining'), device.get('cook').get('time').get('elapsed'))

		probe = MeaterProbe(device.get('id'), device.get('temperature').get('internal'), device.get('temperature').get('ambient'), cook, device.get('updated_at'))

		return probe

class MeaterProbe(object):
    def __init__(self, id, internal_temp, ambient_temp, cook, time_updated):
        self.id = id
        self.internal_temperature = float(internal_temp) # Always in degrees celcius
        self.ambient_temperature = float(ambient_temp) # Always in degrees celcius
        self.cook = cook
        self.time_updated = datetime.fromtimestamp(time_updated)

class MeaterCook(object):
    def __init__(self, id, name, state, target_temp, peak_temp, time_remaining, time_elapsed):
        self.id = id
        self.name = name
        self.state = state
        if target_temp:
            self.target_temperature = float(target_temp) # Always in degrees celcius
        if peak_temp:
            self.peak_temperature = float(peak_temp) # Always in degrees celcius
        if time_remaining:
            self.time_remaining = int(time_remaining) # Always in seconds
        if time_elapsed:
            self.time_elapsed = int(time_elapsed) # Always in seconds