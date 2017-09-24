# API

The ember API is a HTTPs endpoint that returns data in JSON. The base URL is https://ember.ephcontrols.com/api. This will be referred to as $ENDPOINT for the rest of the document. 

Note: I have no connection with EPHControls and this API may be subject to change. Use of this API is at your own risk.

Some of the basic calls are described below:

## Login

Initial login uses the email and password you used to register with the system. Subsequent requests are then authenticated using an access token that is returned during the initial login.

You can use any valid user for this but it would be a good idea to not use the super user for your home and have a dedicated API user

### Request

To login for the first time send a POST to $ENDPOINT/account/directlogin with your email and password.

```
POST /api/account/directlogin HTTP/1.1
Accept	application/json
Content-Type	application/x-www-form-urlencoded
Content-Length	70
Host	ember.ephcontrols.com
```

The form data to POST is

```
Email=me%40email.com&Password=mypassword&RememberMe=True
```


### Response

The response is JSON in the format

```
{
	"token": {
		"emailAddress": "me@email.com",
		"userId": 1000,
		"firstName": "My",
		"lastName": "Name",
		"accessToken": "really_long_access_token",
		"profilePicture": null,
		"issuedOn": "2017-09-21T00:00:00Z",
		"expiresOn": "2017-12-19T00:00:00Z",
		"homeIds": [
		2000],
		"currentHomeId": 2000,
		"fullName": "My Name"
	},
	"isSuccess": true,
	"message": null
}
```

The accessToken is required for subsequent requests so it is important to keep this, this should be sent in the Authorization header as a bearer token for all other requests. 

The homeIds are used to perform actions on your home so should be noted for future requests. 

## Refresh Auth Token

Once you have an auth token from initial login it says it will last approximately 3 months. However, their app refreshes the token on each usage. This API call uses the last received token to request a new one.

### Request

To request a new token send a GET to $ENDPOINT/Account/RefreshToken

```
GET /api/Account/RefreshToken HTTP/1.1
Authorization	bearer really_long_access_token
Accept	application/json
Content-Length	0
Host	ember.ephcontrols.com
```

### Response

The response is quite similar to the initial login response and is JSON in the format

```
{
	"emailAddress": "me@email.com",
	"userId": 1000,
	"firstName": "My",
	"lastName": "Name",
	"accessToken": "new_really_long_access_token",
	"profilePicture": null,
	"issuedOn": "2017-09-20T00:00:00Z",
	"expiresOn": "2017-12-19T00:00:00Z",
	"homeIds": [
	2000],
	"currentHomeId": 2000,
	"fullName": "My Name"
}
```

## Get Home Details

To get details of your home (e.g. zones, temperature), you should use the homeId returned from your initial login.

### Request

The request is a GET to the URL $ENDPOINT/Home/GetHomeById passing the homeId as a query parameter.

```
GET /api/Home/GetHomeById?homeId=2000 HTTP/1.1
Authorization	bearer really_long_access_token
Accept	application/json
Content-Length	0
Host	ember.ephcontrols.com
```

### Response

The response is a JSON Blob describing the home. The below example shows a 2 zone system with one for heating and one for hot water.

```
{
	"data": {
		"homeId": 2000,
		"name": "Home",
		"gatewayId": "0123456789",
		"isOnline": true,
		"gatewayDateTime": "2017-09-21T16:05:21",
		"lastRefreshed": "2017-09-21T15:05:23.2673013Z",
		"users": [{
			"homeId": 2000,
			"homeName": "Home",
			"userId": 1000,
			"userFullName": "My Name",
			"roleId": 3,
			"roleName": "Home Super Admin",
			"roleStaticName": "HOME SUPER ADMIN",
			"accessPermissions": {
				"homeUserAccessId": 1001,
				"homeUserId": 1001,
				"homeManagement": true,
				"areaManagement": true,
				"schedulesManagement": true,
				"scenarioManagement": true,
				"eventManagement": true,
				"holidays": true,
				"boost": true
			},
			"favouriteScenarios": null
		}],
		"receivers": [{
			"receiverId": 1100,
			"homeId": 2000,
			"hardwareId": "AAAAAAAA",
			"isOnline": true,
			"zones": [{
				"zoneId": 3000,
				"receiverId": 1100,
				"receiverHardwareId": "AAAAAAAA",
				"hardwareId": "0",
				"name": "Heating",
				"currentTemperature": 21.4,
				"targetTemperature": 22.0,
				"mode": 0,
				"isHotWater": false,
				"isOnline": true,
				"isBoostActive": false,
				"isAdvanceActive": false,
				"isDemo": false,
				"isTargetTemperatureReached": true,
				"isCurrentlyActive": false,
				"nextEventDate": "2017-09-21T18:00:00Z",
				"boostBaseDate": null,
				"programme": {
					"zoneId": 3000,
					"monday": {
						"dayPeriodId": 22333,
						"period1": {
							"periodId": 77767,
							"startTime": "06:30:00",
							"endTime": "08:30:00",
							"type": 0,
							"isEnabled": true
						},
						"period2": {
							"periodId": 77768,
							"startTime": "12:00:00",
							"endTime": "12:00:00",
							"type": 0,
							"isEnabled": true
						},
						"period3": {
							"periodId": 77769,
							"startTime": "18:00:00",
							"endTime": "23:00:00",
							"type": 0,
							"isEnabled": true
						}
					},
					"tuesday": {
						"dayPeriodId": 22337,
						"period1": {
							"periodId": 77779,
							"startTime": "06:30:00",
							"endTime": "08:30:00",
							"type": 0,
							"isEnabled": true
						},
						"period2": {
							"periodId": 77780,
							"startTime": "12:00:00",
							"endTime": "12:00:00",
							"type": 0,
							"isEnabled": true
						},
						"period3": {
							"periodId": 77781,
							"startTime": "18:00:00",
							"endTime": "23:00:00",
							"type": 0,
							"isEnabled": true
						}
					},
					"wednesday": {
						"dayPeriodId": 22338,
						"period1": {
							"periodId": 77782,
							"startTime": "06:30:00",
							"endTime": "08:30:00",
							"type": 0,
							"isEnabled": true
						},
						"period2": {
							"periodId": 77783,
							"startTime": "12:00:00",
							"endTime": "12:00:00",
							"type": 0,
							"isEnabled": true
						},
						"period3": {
							"periodId": 77784,
							"startTime": "18:00:00",
							"endTime": "23:00:00",
							"type": 0,
							"isEnabled": true
						}
					},
					"thursday": {
						"dayPeriodId": 22336,
						"period1": {
							"periodId": 77776,
							"startTime": "06:30:00",
							"endTime": "08:30:00",
							"type": 0,
							"isEnabled": true
						},
						"period2": {
							"periodId": 77777,
							"startTime": "12:00:00",
							"endTime": "12:00:00",
							"type": 0,
							"isEnabled": true
						},
						"period3": {
							"periodId": 77778,
							"startTime": "18:00:00",
							"endTime": "23:00:00",
							"type": 0,
							"isEnabled": true
						}
					},
					"friday": {
						"dayPeriodId": 22332,
						"period1": {
							"periodId": 77764,
							"startTime": "06:30:00",
							"endTime": "08:30:00",
							"type": 0,
							"isEnabled": true
						},
						"period2": {
							"periodId": 77765,
							"startTime": "12:00:00",
							"endTime": "12:00:00",
							"type": 0,
							"isEnabled": true
						},
						"period3": {
							"periodId": 77766,
							"startTime": "18:00:00",
							"endTime": "23:00:00",
							"type": 0,
							"isEnabled": true
						}
					},
					"saturday": {
						"dayPeriodId": 22334,
						"period1": {
							"periodId": 77770,
							"startTime": "08:30:00",
							"endTime": "10:00:00",
							"type": 0,
							"isEnabled": true
						},
						"period2": {
							"periodId": 77771,
							"startTime": "12:00:00",
							"endTime": "12:00:00",
							"type": 0,
							"isEnabled": true
						},
						"period3": {
							"periodId": 77772,
							"startTime": "18:00:00",
							"endTime": "23:00:00",
							"type": 0,
							"isEnabled": true
						}
					},
					"sunday": {
						"dayPeriodId": 22335,
						"period1": {
							"periodId": 77773,
							"startTime": "08:30:00",
							"endTime": "10:00:00",
							"type": 0,
							"isEnabled": true
						},
						"period2": {
							"periodId": 77774,
							"startTime": "12:00:00",
							"endTime": "12:00:00",
							"type": 0,
							"isEnabled": true
						},
						"period3": {
							"periodId": 77775,
							"startTime": "18:00:00",
							"endTime": "23:00:00",
							"type": 0,
							"isEnabled": true
						}
					}
				},
				"areaId": null,
				"areaName": null,
				"boostActivations": [{
					"zoneBoostActivationId": 55555,
					"zoneId": 3000,
					"zoneName": "Heating",
					"userId": 1000,
					"activatedByUserName": "My",
					"numberOfHours": 1,
					"targetTemperature": 28.00,
					"activatedOn": "2017-09-19T16:14:00.537",
					"finishDateTime": "2017-09-19T16:14:34.17",
					"expiryTime": "2017-09-19T17:14:00.537",
					"wasCancelled": true,
					"comments": null
				}, {
					"zoneBoostActivationId": 55556,
					"zoneId": 3000,
					"zoneName": "Heating",
					"userId": 1000,
					"activatedByUserName": "My",
					"numberOfHours": 1,
					"targetTemperature": 28.00,
					"activatedOn": "2017-09-19T16:46:55.413",
					"finishDateTime": "2017-09-19T17:46:55.413",
					"expiryTime": "2017-09-19T17:46:55.413",
					"wasCancelled": true,
					"comments": null
				}, {
					"zoneBoostActivationId": 55557,
					"zoneId": 3000,
					"zoneName": "Heating",
					"userId": 1000,
					"activatedByUserName": "My",
					"numberOfHours": 1,
					"targetTemperature": 28.00,
					"activatedOn": "2017-09-19T16:46:58.787",
					"finishDateTime": "2017-09-19T16:48:05.677",
					"expiryTime": "2017-09-19T17:46:58.787",
					"wasCancelled": true,
					"comments": null
				}, {
					"zoneBoostActivationId": 55558,
					"zoneId": 3000,
					"zoneName": "Heating",
					"userId": 1000,
					"activatedByUserName": "My",
					"numberOfHours": 1,
					"targetTemperature": 28.00,
					"activatedOn": "2017-09-21T08:08:34.823",
					"finishDateTime": "2017-09-21T08:08:50.387",
					"expiryTime": "2017-09-21T09:08:34.823",
					"wasCancelled": true,
					"comments": null
				}, {
					"zoneBoostActivationId": 55559,
					"zoneId": 3000,
					"zoneName": "Heating",
					"userId": 1000,
					"activatedByUserName": "My",
					"numberOfHours": 1,
					"targetTemperature": 28.00,
					"activatedOn": "2017-09-21T12:20:31.113",
					"finishDateTime": "2017-09-21T12:20:34.47",
					"expiryTime": "2017-09-21T13:20:31.113",
					"wasCancelled": true,
					"comments": null
				}, {
					"zoneBoostActivationId": 55560,
					"zoneId": 3000,
					"zoneName": "Heating",
					"userId": 1000,
					"activatedByUserName": "My",
					"numberOfHours": 1,
					"targetTemperature": 28.00,
					"activatedOn": "2017-09-21T12:41:47.907",
					"finishDateTime": "2017-09-21T12:41:58.443",
					"expiryTime": "2017-09-21T13:41:47.907",
					"wasCancelled": true,
					"comments": null
				}]
			}, {
				"zoneId": 3001,
				"receiverId": 1100,
				"receiverHardwareId": "AAAAAAAA",
				"hardwareId": "1",
				"name": "Hot Water",
				"currentTemperature": 21.5,
				"targetTemperature": 65.0,
				"mode": 0,
				"isHotWater": true,
				"isOnline": true,
				"isBoostActive": false,
				"isAdvanceActive": false,
				"isDemo": false,
				"isTargetTemperatureReached": true,
				"isCurrentlyActive": false,
				"nextEventDate": "2017-09-21T17:00:00Z",
				"boostBaseDate": null,
				"programme": {
					"zoneId": 3001,
					"monday": {
						"dayPeriodId": 26630,
						"period1": {
							"periodId": 77788,
							"startTime": "06:30:00",
							"endTime": "08:30:00",
							"type": 0,
							"isEnabled": true
						},
						"period2": {
							"periodId": 77789,
							"startTime": "12:00:00",
							"endTime": "12:00:00",
							"type": 0,
							"isEnabled": true
						},
						"period3": {
							"periodId": 79890,
							"startTime": "17:00:00",
							"endTime": "18:00:00",
							"type": 0,
							"isEnabled": true
						}
					},
					"tuesday": {
						"dayPeriodId": 26634,
						"period1": {
							"periodId": 79900,
							"startTime": "06:30:00",
							"endTime": "08:30:00",
							"type": 0,
							"isEnabled": true
						},
						"period2": {
							"periodId": 79901,
							"startTime": "12:00:00",
							"endTime": "12:00:00",
							"type": 0,
							"isEnabled": true
						},
						"period3": {
							"periodId": 79902,
							"startTime": "17:00:00",
							"endTime": "18:00:00",
							"type": 0,
							"isEnabled": true
						}
					},
					"wednesday": {
						"dayPeriodId": 26635,
						"period1": {
							"periodId": 79903,
							"startTime": "06:30:00",
							"endTime": "08:30:00",
							"type": 0,
							"isEnabled": true
						},
						"period2": {
							"periodId": 79904,
							"startTime": "12:00:00",
							"endTime": "12:00:00",
							"type": 0,
							"isEnabled": true
						},
						"period3": {
							"periodId": 79905,
							"startTime": "17:00:00",
							"endTime": "18:00:00",
							"type": 0,
							"isEnabled": true
						}
					},
					"thursday": {
						"dayPeriodId": 26633,
						"period1": {
							"periodId": 79897,
							"startTime": "06:30:00",
							"endTime": "08:30:00",
							"type": 0,
							"isEnabled": true
						},
						"period2": {
							"periodId": 79898,
							"startTime": "12:00:00",
							"endTime": "12:00:00",
							"type": 0,
							"isEnabled": true
						},
						"period3": {
							"periodId": 79899,
							"startTime": "17:00:00",
							"endTime": "18:00:00",
							"type": 0,
							"isEnabled": true
						}
					},
					"friday": {
						"dayPeriodId": 22339,
						"period1": {
							"periodId": 77785,
							"startTime": "06:30:00",
							"endTime": "08:30:00",
							"type": 0,
							"isEnabled": true
						},
						"period2": {
							"periodId": 77786,
							"startTime": "12:00:00",
							"endTime": "12:00:00",
							"type": 0,
							"isEnabled": true
						},
						"period3": {
							"periodId": 77787,
							"startTime": "17:00:00",
							"endTime": "18:00:00",
							"type": 0,
							"isEnabled": true
						}
					},
					"saturday": {
						"dayPeriodId": 26631,
						"period1": {
							"periodId": 79891,
							"startTime": "07:30:00",
							"endTime": "10:00:00",
							"type": 0,
							"isEnabled": true
						},
						"period2": {
							"periodId": 79892,
							"startTime": "12:00:00",
							"endTime": "12:00:00",
							"type": 0,
							"isEnabled": true
						},
						"period3": {
							"periodId": 79893,
							"startTime": "17:00:00",
							"endTime": "18:30:00",
							"type": 0,
							"isEnabled": true
						}
					},
					"sunday": {
						"dayPeriodId": 26632,
						"period1": {
							"periodId": 79894,
							"startTime": "07:30:00",
							"endTime": "10:00:00",
							"type": 0,
							"isEnabled": true
						},
						"period2": {
							"periodId": 79895,
							"startTime": "12:00:00",
							"endTime": "12:00:00",
							"type": 0,
							"isEnabled": true
						},
						"period3": {
							"periodId": 79896,
							"startTime": "17:00:00",
							"endTime": "23:00:00",
							"type": 0,
							"isEnabled": true
						}
					}
				},
				"areaId": null,
				"areaName": null,
				"boostActivations": []
			}]
		}],
		"holiday": {
			"homeId": 2000,
			"startDate": null,
			"endDate": null,
			"status": 0,
			"scheduledByUserId": 1000
		},
		"inviteCode": "ABCDE",
		"weatherLocation": "Dublin, IE",
		"weatherLocationId": "123456789",
		"backlightModeIsActive": false,
		"frostProtectionEnabled": false,
		"frostProtectionTemperature": 5.0,
		"isFrostProtectionActive": false,
		"holidayModeActive": false,
		"activeZoneBoosts": [{
			"zoneBoostActivationId": 66666,
			"zoneId": 3000,
			"zoneName": "Heating",
			"userId": 1000,
			"activatedByUserName": "My",
			"numberOfHours": 1,
			"targetTemperature": 28.00,
			"activatedOn": "2017-09-19T16:14:00.537",
			"finishDateTime": "2017-09-19T16:14:34.17",
			"expiryTime": "2017-09-19T17:14:00.537",
			"wasCancelled": true,
			"comments": null
		}, {
			"zoneBoostActivationId": 66667,
			"zoneId": 3000,
			"zoneName": "Heating",
			"userId": 1000,
			"activatedByUserName": "My",
			"numberOfHours": 1,
			"targetTemperature": 28.00,
			"activatedOn": "2017-09-19T16:46:55.413",
			"finishDateTime": "2017-09-19T17:46:55.413",
			"expiryTime": "2017-09-19T17:46:55.413",
			"wasCancelled": true,
			"comments": null
		}, {
			"zoneBoostActivationId": 66668,
			"zoneId": 3000,
			"zoneName": "Heating",
			"userId": 1000,
			"activatedByUserName": "My",
			"numberOfHours": 1,
			"targetTemperature": 28.00,
			"activatedOn": "2017-09-19T16:46:58.787",
			"finishDateTime": "2017-09-19T16:48:05.677",
			"expiryTime": "2017-09-19T17:46:58.787",
			"wasCancelled": true,
			"comments": null
		}, {
			"zoneBoostActivationId": 66669,
			"zoneId": 3000,
			"zoneName": "Heating",
			"userId": 1000,
			"activatedByUserName": "My",
			"numberOfHours": 1,
			"targetTemperature": 28.00,
			"activatedOn": "2017-09-21T08:08:34.823",
			"finishDateTime": "2017-09-21T08:08:50.387",
			"expiryTime": "2017-09-21T09:08:34.823",
			"wasCancelled": true,
			"comments": null
		}, {
			"zoneBoostActivationId": 66670,
			"zoneId": 3000,
			"zoneName": "Heating",
			"userId": 1000,
			"activatedByUserName": "My",
			"numberOfHours": 1,
			"targetTemperature": 28.00,
			"activatedOn": "2017-09-21T12:20:31.113",
			"finishDateTime": "2017-09-21T12:20:34.47",
			"expiryTime": "2017-09-21T13:20:31.113",
			"wasCancelled": true,
			"comments": null
		}, {
			"zoneBoostActivationId": 66671,
			"zoneId": 3000,
			"zoneName": "Heating",
			"userId": 1000,
			"activatedByUserName": "My",
			"numberOfHours": 1,
			"targetTemperature": 28.00,
			"activatedOn": "2017-09-21T12:41:47.907",
			"finishDateTime": "2017-09-21T12:41:58.443",
			"expiryTime": "2017-09-21T13:41:47.907",
			"wasCancelled": true,
			"comments": null
		}]
	},
	"isSuccess": true,
	"message": null
}
```

There is quite a bit of information here but it shows most of the information you would care about. The `receivers[zone]` array contains all zones in the house, and each zone contains information on it's active state, temperature, schedule, type, and recent changes.

This request was obtained by a super user account. It is possible that less information is available on restricted accounts.

## Turn On Boost

When turning on the boost you pass the zoneId that you would like to boost. This can be aquired from the previous GetHomeById command.

### Request

The request is a POST to the URL $ENDPOINT/Home/ActivateZoneBoost, passing up JSON data with the required information.

```
POST /api/Home/ActivateZoneBoost HTTP/1.1
Authorization	bearer really_long_access_token
Accept	application/json
Content-Type	application/json
Content-Length	59
Host	ember.ephcontrols.com
```

The JSON data to pass up is

```
{
	"ZoneIds": [3000],
	"NumberOfHours": 1,
	"TargetTemperature": 23
}
```

The data structure makes it seem like it is possible to boost multiple zones at the same time but I haven't tried this as it doesn't make sense for a heating / water 2 zone system.

# Response

The respones is a simple JSON structure with isSuccess and message variables.

```
{
	"isSuccess": true,
	"message": "Boost activated"
}
```

## Turn Off Boost

When turning off the boost you pass the zoneId that you would like to deactivate. This can be aquired from the previous GetHomeById command.

### Request

The request is a POST to the URL $ENDPOINT/Home/DeActivateZoneBoost, passing up JSON data with the required information.

```
POST /api/Home/DeActivateZoneBoost HTTP/1.1
Authorization	bearer really_long_access_token
Accept	application/json
Content-Type	application/json
Content-Length	59
Host	ember.ephcontrols.com
```

The JSON data to pass up is simply a list of ZoneIds

```
[3000]
```

The data structure makes it seem like it is possible to boost multiple zones at the same time but I haven't tried this as it doesn't make sense for a heating / water 2 zone system.

# Response

The respones is a simple JSON structure with isSuccess and message variables.

```
{
	"isSuccess": true,
	"message": "Boost deactivated"
}
```

## Set Zone Target Temperature

Sets the target temperature for a zone.

### Request

The request is a POST to the URL $ENDPOINT/Home/ZoneTargetTemperature, passing up JSON data with the required information.

```
POST /api/Home/ZoneTargetTemperature HTTP/1.1
Authorization	bearer really_long_access_token
Accept	application/json
Content-Type	application/json
Content-Length	59
Host	ember.ephcontrols.com
```

The JSON data to pass up includes the ZoneId and the tempetature.

```
{
	"ZoneId": 3000,
	"TargetTemperature": 21
}
```

# Response

The respones is a simple JSON structure with isSuccess and message variables.

```
{
	"isSuccess": true,
	"message": null
}
```

## Update the programme times for a zone

This call will update the programmed times for a zone. 

### Request

The request is a POST to the URL $ENDPOINT/Home/ZoneTargetTemperature, passing up JSON data with the required information.

```
POST /api/Home/UpdateZoneProgramme HTTP/1.1
Authorization	bearer really_long_access_token
Accept	application/json
Content-Type	application/json
Content-Length	59
Host	ember.ephcontrols.com
```

The JSON data to pass up includes the ZoneId and period information for the change.

```
{
	"ZoneId": 3000,
	"Monday": {
		"DayPeriodId": 22333,
		"Period1": {
			"PeriodId": 77767,
			"StartTime": "07:50:00",
			"EndTime": "08:10:00",
			"Type": 0,
			"IsEnabled": true
		},
		"Period2": {
			"PeriodId": 77768,
			"StartTime": "12:00:00",
			"EndTime": "12:00:00",
			"Type": 0,
			"IsEnabled": true
		},
		"Period3": {
			"PeriodId": 77769,
			"StartTime": "18:40:00",
			"EndTime": "19:10:00",
			"Type": 0,
			"IsEnabled": true
		}
	},
	"Tuesday": {
		"DayPeriodId": 22337,
		"Period1": {
			"PeriodId": 77779,
			"StartTime": "07:50:00",
			"EndTime": "08:10:00",
			"Type": 0,
			"IsEnabled": true
		},
		"Period2": {
			"PeriodId": 77780,
			"StartTime": "12:00:00",
			"EndTime": "12:00:00",
			"Type": 0,
			"IsEnabled": true
		},
		"Period3": {
			"PeriodId": 77781,
			"StartTime": "18:40:00",
			"EndTime": "19:10:00",
			"Type": 0,
			"IsEnabled": true
		}
	},
	"Wednesday": {
		"DayPeriodId": 22338,
		"Period1": {
			"PeriodId": 77782,
			"StartTime": "07:50:00",
			"EndTime": "08:10:00",
			"Type": 0,
			"IsEnabled": true
		},
		"Period2": {
			"PeriodId": 77783,
			"StartTime": "12:00:00",
			"EndTime": "12:00:00",
			"Type": 0,
			"IsEnabled": true
		},
		"Period3": {
			"PeriodId": 77784,
			"StartTime": "18:40:00",
			"EndTime": "19:10:00",
			"Type": 0,
			"IsEnabled": true
		}
	},
	"Thursday": {
		"DayPeriodId": 22336,
		"Period1": {
			"PeriodId": 77776,
			"StartTime": "07:50:00",
			"EndTime": "08:10:00",
			"Type": 0,
			"IsEnabled": true
		},
		"Period2": {
			"PeriodId": 77777,
			"StartTime": "12:00:00",
			"EndTime": "12:00:00",
			"Type": 0,
			"IsEnabled": true
		},
		"Period3": {
			"PeriodId": 77778,
			"StartTime": "18:40:00",
			"EndTime": "19:10:00",
			"Type": 0,
			"IsEnabled": true
		}
	},
	"Friday": {
		"DayPeriodId": 22332,
		"Period1": {
			"PeriodId": 77764,
			"StartTime": "07:50:00",
			"EndTime": "08:10:00",
			"Type": 0,
			"IsEnabled": true
		},
		"Period2": {
			"PeriodId": 77765,
			"StartTime": "12:00:00",
			"EndTime": "12:00:00",
			"Type": 0,
			"IsEnabled": true
		},
		"Period3": {
			"PeriodId": 77766,
			"StartTime": "18:40:00",
			"EndTime": "19:10:00",
			"Type": 0,
			"IsEnabled": true
		}
	},
	"Saturday": {
		"DayPeriodId": 22334,
		"Period1": {
			"PeriodId": 77770,
			"StartTime": "08:50:00",
			"EndTime": "09:20:00",
			"Type": 0,
			"IsEnabled": true
		},
		"Period2": {
			"PeriodId": 77771,
			"StartTime": "14:30:00",
			"EndTime": "15:00:00",
			"Type": 0,
			"IsEnabled": true
		},
		"Period3": {
			"PeriodId": 77772,
			"StartTime": "20:00:00",
			"EndTime": "21:00:00",
			"Type": 0,
			"IsEnabled": true
		}
	},
	"Sunday": {
		"DayPeriodId": 22335,
		"Period1": {
			"PeriodId": 77773,
			"StartTime": "09:00:00",
			"EndTime": "09:30:00",
			"Type": 0,
			"IsEnabled": true
		},
		"Period2": {
			"PeriodId": 77774,
			"StartTime": "14:30:00",
			"EndTime": "15:00:00",
			"Type": 0,
			"IsEnabled": true
		},
		"Period3": {
			"PeriodId": 77775,
			"StartTime": "20:00:00",
			"EndTime": "21:00:00",
			"Type": 0,
			"IsEnabled": true
		}
	}
}
```

It appears that you have to update every period even if only changing one. I am unsure how the PeriodId and DayPeriodId variables are calculated.

This structure is very similar to the one returned in the `programme` map during the getHome call. However, it appears the capatilisation of variable names is different. I have not tested if this matters. If it does it would be trivial to change between `camelCase` and `PascalCase`.

# Response

The respones is a simple JSON structure with isSuccess and message variables.

```
{
	"isSuccess": true,
	"message": "The Zone programme was successfully updated"
}
```

## Other API Calls

Some other calls that I have seen but not investigated include:

### Weather

```GET /api/Weather/WeatherConditionsForLocationId?locationId=12345```

Return the weather for the specified location. Weather includes temperature and an icon for the weather type (e.g. rain, sunny)

### Device

```POST /api/Account/UpdateDevice ```

Post details of your device (uuid, model, OS) to their service. This may also be used to set push notifications.

Devices associated with your account can be viewed through their [web app](https://ember.ephcontrols.com)
