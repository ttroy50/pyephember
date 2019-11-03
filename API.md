# API

The ember API is a HTTPs endpoint that returns data in JSON. The base URL is https://eu-https.topband-cloud.com/ember-back. This will be referred to as $ENDPOINT for the rest of the document. 

Note: I have no connection with EPHControls and this API may be subject to change. Use of this API is at your own risk.

Some of the basic calls are described below:

## Login

Initial login uses the email and password you used to register with the system. Subsequent requests are then authenticated using an access token that is returned during the initial login.

You can use any valid user for this but it would be a good idea to not use the super user for your home and have a dedicated API user

### Request

To login for the first time send a POST to $ENDPOINT/appLogin/login with a JSON request containing your username and password.

```
POST /ember-back/appLogin/login HTTP/1.1
Accept	application/json
Content-Type	application/json;charset=utf-8
```

The form data to POST is

```
{
	"password": "password",
	"model": "iPhone 7",
	"os": "13.1.3",
	"userName": "user@email.com"
}
```

### Response

The response is JSON in the format

```
{
	"data": {
		"refresh_token": "long_refresh_token",
		"token": "long_token"
	},
	"message": null,
	"status": 0,
	"timestamp": 1572386460000
}
```

The `token` is required for subsequent requests so it is important to keep this, this should be sent in the Authorization header for all other requests. 

## Refresh Auth Token

To refresh your access token, send a GET to `$ENDPOINT/appLogin/refreshAccessToken` using the `refresh_token` from your login request in the Authorization header 

It is unclear how long an access token last for however, it looks to last at least 1 hour. 

```
GET /ember-back/appLogin/refreshAccessToken HTTP/1.1
Accept	application/json
Authorization	long_refresh_token
```

### Request

The response contains the new authorization and refresh tokens.

```
{
	"data": {
		"refresh_token": "new_long_refresh_token",
		"token": "new_long_token"
	},
	"message": null,
	"status": 0,
	"timestamp": 1572718395062
}
```

## Get Available Homes

To get the list of available homes 

### Request

The request is a GET to the URL $ENDPOINT/homes/list.

```
GET /ember-back/homes/list HTTP/1.1
Authorization	long_token
Accept	application/json
Content-Length	0
```

### Response

The response is a JSON Blob describing the homes available to your account.

```
{
	"data": [{
		"deviceType": 1,
		"gatewayid": "gwid1234",
		"invitecode": "ABDC",
		"name": "Home",
		"uid": null,
		"zoneCount": 2
	}],
	"message": "succ.",
	"status": 0,
	"timestamp": 1572386460293
```

The `gatewayid` is required for later requests to identify the home that is being controlled.


## Get Home Details

To get details of your home, you should use the `gatewayid` returned from the `homes/list` request above.

### Request

The request is a POST to the URL `$ENDPOINT/homes/detail` passing the `gatewayid` in a JSON request

```
GET /ember-back/homes/detail HTTP/1.1
Authorization	long_token
Accept	application/json
```

The JSON to send is:

```
{
	"gateWayId": "gwid1234"
}
```

### Response

The response is JSON 

```
{
	"data": {
		"settings": {
			"holidaymodescheduled": false,
			"newuserhasjoinedhome": true,
			"userhaslefthome": true,
			"userid": 1001,
			"zoneboostactivated": false,
			"zonescheduleupdated": false
		},
		"curAccess": {
			"areamanagement": true,
			"boost": true,
			"eventmanagement": true,
			"holidays": true,
			"homemanagement": true,
			"homeuserid": 1000,
			"roleId": 3,
			"scenariomanagement": true,
			"schedulesmanagement": true
		},
		"homes": {
			"addoffsettogetlocal": true,
			"addoffsettogetutc": false,
			"backlightmodeisactive": false,
			"deviceType": 1,
			"frostprotectionenabled": true,
			"frostprotectiontemperature": 5.00,
			"gatewaydatetime": "2019-10-29 22:33:58.000",
			"gatewayid": "gwid1234",
			"holidayStatus": 0,
			"holidaymodeactive": false,
			"homeid": 2000,
			"invitecode": "ABCD",
			"isfrostprotectionactive": false,
			"isonline": true,
			"lastrefreshed": "2019-10-29 22:33:58.000",
			"name": "Home",
			"portnumber": 0,
			"quickboosttemperature": 23.00,
			"receivers": [],
			"sysTemType": "EMBER-PS",
			"utctimeoffset": "00:59:58.8658310",
			"weatherlocation": "Dublin, IE",
			"weatherlocationid": "1234578",
			"zoneCount": 2
		}
	},
	"message": "succ.",
	"status": 0,
	"timestamp": 1572386462651
}
```

## Get Zone List

To get list of zones for your home, you should use the `gatewayid` returned from the `homes/list` request above.

### Request

The request is a POST to the URL `$ENDPOINT/homes/zoneList` passing the `gatewayid` in a JSON request

```
GET /ember-back/homes/zoneList HTTP/1.1
Authorization	long_token
Accept	application/json
```

The JSON to send is:

```
{
	"gateWayId": "gwid1234"
}
```

### Response

```
{
	"data": [{
		"areaid": null,
		"boostActivations": null,
		"boostTime1": null,
		"boostTime2": null,
		"boostTime3": null,
		"currenttemperature": 22.00,
		"hardwareid": "0",
		"homeName": null,
		"isadvanceactive": false,
		"isboostactive": false,
		"ishotwater": false,
		"isonline": true,
		"mode": 0,
		"name": "Heating",
		"prefix": null,
		"programmes": null,
		"receiverid": 3000,
		"scenarioScenarioid": null,
		"status": 2,
		"storedtargettemperature": 24.00,
		"targettemperature": 24.00,
		"zoneid": 7000
	}, {
		"areaid": null,
		"boostActivations": null,
		"boostTime1": null,
		"boostTime2": null,
		"boostTime3": null,
		"currenttemperature": 50.50,
		"hardwareid": "1",
		"homeName": null,
		"isadvanceactive": false,
		"isboostactive": false,
		"ishotwater": true,
		"isonline": true,
		"mode": 0,
		"name": "Hot Water",
		"prefix": null,
		"programmes": null,
		"receiverid": 3000,
		"scenarioScenarioid": null,
		"status": 1,
		"storedtargettemperature": 55.00,
		"targettemperature": 55.00,
		"zoneid": 7100
	}],
	"message": "succ.",
	"status": 0,
	"timestamp": 1572386493495
}
```

## Turn On Boost

When turning on the boost you pass the `zoneId` that you would like to boost. This can be retrieved from the previous `zones/list` command.

### Request

```
POST /ember-back/zones/boost HTTP/1.1
Authorization	long_token
Accept	application/json
```

The JSON to send is:

```
{
	"hours": "1",
	"zoneid": "7000",
	"temperature": "24.0"
}
```
# Response

```
{
	"data": null,
	"message": "succ.",
	"status": 0,
	"timestamp": 1572386496332
}
```

## Turn Off Boost

When turning off the boost you pass the `zoneId` that you would like to deactivate to `zones/cancelBoost`.

### Request

```
POST /ember-back/zones/cancelBoost HTTP/1.1
Authorization	long_token
Accept	application/json
```

The JSON to send is:

```
{
	"zoneid": "7000"
}
```
# Response

```
{
	"data": null,
	"message": "succ.",
	"status": 0,
	"timestamp": 1572386496332
}
```

## Get Boost Status

To get the status of the boost for a zone you can POST the `zoneid` to `zones/getBoostFirstTime`

### Request

```
POST /ember-back/zones/getBoostFirstTime HTTP/1.1
Authorization	long_token
Accept	application/json
```

The JSON to send is:

```
{
	"zoneid": "7000"
}
```
# Response

```
{
	"data": {
		"areaid": null,
		"boostActivations": {
			"activatedon": "2019-11-02 13:20:37.669",
			"comments": null,
			"dispayFinishdatetime": "2019-11-02 14:20:37.669",
			"finishdatetime": "2019-11-02 14:20:37.669",
			"numberofhours": 1,
			"targettemperature": 24.00,
			"userid": 1000,
			"wascancelled": false,
			"zoneboostactivationid": 1344098,
			"zoneid": 7000
		},
		"boostTime1": null,
		"boostTime2": null,
		"boostTime3": null,
		"currenttemperature": 22.40,
		"hardwareid": "0",
		"homeName": null,
		"isadvanceactive": false,
		"isboostactive": true,
		"ishotwater": false,
		"isonline": true,
		"mode": 0,
		"name": "Heating",
		"prefix": null,
		"programmes": {
			"friday": {
				"dayperiodid": 51822,
				"p1": {
					"endtime": "08:10",
					"periodid": 155464,
					"starttime": "07:20"
				},
				"p2": {
					"endtime": "19:00",
					"periodid": 155465,
					"starttime": "18:00"
				},
				"p3": {
					"endtime": "23:00",
					"periodid": 155466,
					"starttime": "21:30"
				}
			},
			"fridayDayperiodid": 51822,
			"monday": {
				"dayperiodid": 51823,
				"p1": {
					"endtime": "09:20",
					"periodid": 155467,
					"starttime": "08:30"
				},
				"p2": {
					"endtime": "14:30",
					"periodid": 155468,
					"starttime": "14:00"
				},
				"p3": {
					"endtime": "19:30",
					"periodid": 155469,
					"starttime": "19:00"
				}
			},
			"mondayDayperiodid": 51823,
			"saturday": {
				"dayperiodid": 51824,
				"p1": {
					"endtime": "09:20",
					"periodid": 155470,
					"starttime": "08:30"
				},
				"p2": {
					"endtime": "14:30",
					"periodid": 155471,
					"starttime": "14:00"
				},
				"p3": {
					"endtime": "19:30",
					"periodid": 155472,
					"starttime": "19:00"
				}
			},
			"saturdayDayperiodid": 51824,
			"sunday": {
				"dayperiodid": 51825,
				"p1": {
					"endtime": "09:40",
					"periodid": 155473,
					"starttime": "08:40"
				},
				"p2": {
					"endtime": "17:00",
					"periodid": 155474,
					"starttime": "15:30"
				},
				"p3": {
					"endtime": "23:10",
					"periodid": 155475,
					"starttime": "22:50"
				}
			},
			"sundayDayperiodid": 51825,
			"thursday": {
				"dayperiodid": 51826,
				"p1": {
					"endtime": "08:10",
					"periodid": 155476,
					"starttime": "06:40"
				},
				"p2": {
					"endtime": "19:00",
					"periodid": 155477,
					"starttime": "17:40"
				},
				"p3": {
					"endtime": "23:00",
					"periodid": 155478,
					"starttime": "21:30"
				}
			},
			"thursdayDayperiodid": 51826,
			"tuesday": {
				"dayperiodid": 51827,
				"p1": {
					"endtime": "08:10",
					"periodid": 155479,
					"starttime": "06:40"
				},
				"p2": {
					"endtime": "19:00",
					"periodid": 155480,
					"starttime": "17:40"
				},
				"p3": {
					"endtime": "23:00",
					"periodid": 155481,
					"starttime": "21:30"
				}
			},
			"tuesdayDayperiodid": 51827,
			"wednesday": {
				"dayperiodid": 51828,
				"p1": {
					"endtime": "08:10",
					"periodid": 155482,
					"starttime": "07:20"
				},
				"p2": {
					"endtime": "19:00",
					"periodid": 155483,
					"starttime": "18:00"
				},
				"p3": {
					"endtime": "23:00",
					"periodid": 155484,
					"starttime": "21:30"
				}
			},
			"wednesdayDayperiodid": 51828,
			"zoneid": 7000
		},
		"receiverid": 3000,
		"scenarioScenarioid": null,
		"status": 1,
		"storedtargettemperature": 24.00,
		"targettemperature": 24.00,
		"zoneid": 7000
	},
	"message": "succ.",
	"status": 0,
	"timestamp": 1572700843920
}
```

In the above example boost is active. If boost is not active the `boostActivations` map is null and the `boostTime` variables contain boost time options like `1 hour (on until 14:20)`. 

## Set Zone Target Temperature

Sets the target temperature for a zone.

### Request


```
POST /ember-back/zones/setTargetTemperature HTTP/1.1
Authorization	long_token
Accept	application/json
```

JSON

```
{
	"zoneid": "0000",
	"temperature": 24.5
}
```

# Response

```
{
	"data": null,
	"message": "succ.",
	"status": 0,
	"timestamp": 1572386482517
}
```

## Get Details of Zones

To get the details of the zones post the `gatewayid` to `zones/polling`

```
POST /ember-back/zones/polling HTTP/1.1
Authorization	long_token
Accept	application/json
```

JSON

```
{
	"gateWayId": "gwid1234"
}
```

# Response

```
{
	"data": [{
		"areaid": null,
		"boostActivations": {
			"activatedon": "2019-10-29 22:01:36.357",
			"comments": null,
			"dispayFinishdatetime": "2019-10-30 00:00:00.000",
			"finishdatetime": "2019-10-30 00:00:00.000",
			"numberofhours": 1,
			"targettemperature": 24.00,
			"userid": 1000,
			"wascancelled": false,
			"zoneboostactivationid": 1330995,
			"zoneid": 7000
		},
		"boostTime1": null,
		"boostTime2": null,
		"boostTime3": null,
		"currenttemperature": 22.40,
		"hardwareid": "0",
		"homeName": null,
		"isadvanceactive": false,
		"isboostactive": false,
		"ishotwater": false,
		"isonline": true,
		"mode": 0,
		"name": "Heating",
		"prefix": "This zone is off until 14:00",
		"programmes": {
			"friday": {
				"dayperiodid": 51822,
				"p1": {
					"endtime": "08:10",
					"periodid": 155464,
					"starttime": "07:20"
				},
				"p2": {
					"endtime": "19:00",
					"periodid": 155465,
					"starttime": "18:00"
				},
				"p3": {
					"endtime": "23:00",
					"periodid": 155466,
					"starttime": "21:30"
				}
			},
			"fridayDayperiodid": 51822,
			"monday": {
				"dayperiodid": 51823,
				"p1": {
					"endtime": "09:20",
					"periodid": 155467,
					"starttime": "08:30"
				},
				"p2": {
					"endtime": "14:30",
					"periodid": 155468,
					"starttime": "14:00"
				},
				"p3": {
					"endtime": "19:30",
					"periodid": 155469,
					"starttime": "19:00"
				}
			},
			"mondayDayperiodid": 51823,
			"saturday": {
				"dayperiodid": 51824,
				"p1": {
					"endtime": "09:20",
					"periodid": 155470,
					"starttime": "08:30"
				},
				"p2": {
					"endtime": "14:30",
					"periodid": 155471,
					"starttime": "14:00"
				},
				"p3": {
					"endtime": "19:30",
					"periodid": 155472,
					"starttime": "19:00"
				}
			},
			"saturdayDayperiodid": 51824,
			"sunday": {
				"dayperiodid": 51825,
				"p1": {
					"endtime": "09:40",
					"periodid": 155473,
					"starttime": "08:40"
				},
				"p2": {
					"endtime": "17:00",
					"periodid": 155474,
					"starttime": "15:30"
				},
				"p3": {
					"endtime": "23:10",
					"periodid": 155475,
					"starttime": "22:50"
				}
			},
			"sundayDayperiodid": 51825,
			"thursday": {
				"dayperiodid": 51826,
				"p1": {
					"endtime": "08:10",
					"periodid": 155476,
					"starttime": "06:40"
				},
				"p2": {
					"endtime": "19:00",
					"periodid": 155477,
					"starttime": "17:40"
				},
				"p3": {
					"endtime": "23:00",
					"periodid": 155478,
					"starttime": "21:30"
				}
			},
			"thursdayDayperiodid": 51826,
			"tuesday": {
				"dayperiodid": 51827,
				"p1": {
					"endtime": "08:10",
					"periodid": 155479,
					"starttime": "06:40"
				},
				"p2": {
					"endtime": "19:00",
					"periodid": 155480,
					"starttime": "17:40"
				},
				"p3": {
					"endtime": "23:00",
					"periodid": 155481,
					"starttime": "21:30"
				}
			},
			"tuesdayDayperiodid": 51827,
			"wednesday": {
				"dayperiodid": 51828,
				"p1": {
					"endtime": "08:10",
					"periodid": 155482,
					"starttime": "07:20"
				},
				"p2": {
					"endtime": "19:00",
					"periodid": 155483,
					"starttime": "18:00"
				},
				"p3": {
					"endtime": "23:00",
					"periodid": 155484,
					"starttime": "21:30"
				}
			},
			"wednesdayDayperiodid": 51828,
			"zoneid": 7000
		},
		"receiverid": 3000,
		"scenarioScenarioid": null,
		"status": 1,
		"storedtargettemperature": 24.00,
		"targettemperature": 24.00,
		"zoneid": 7000
	}, {
		"areaid": null,
		"boostActivations": {
			"activatedon": "2019-10-31 21:52:57.419",
			"comments": null,
			"dispayFinishdatetime": "2019-10-31 22:52:57.419",
			"finishdatetime": "2019-10-31 22:52:57.419",
			"numberofhours": 1,
			"targettemperature": 55.00,
			"userid": 1000,
			"wascancelled": false,
			"zoneboostactivationid": 1339296,
			"zoneid": 7100
		},
		"boostTime1": null,
		"boostTime2": null,
		"boostTime3": null,
		"currenttemperature": 47.00,
		"hardwareid": "1",
		"homeName": null,
		"isadvanceactive": false,
		"isboostactive": false,
		"ishotwater": true,
		"isonline": true,
		"mode": 0,
		"name": "Hot Water",
		"prefix": "This zone is off until 14:00",
		"programmes": {
			"friday": {
				"dayperiodid": 51829,
				"p1": {
					"endtime": "07:50",
					"periodid": 155485,
					"starttime": "07:00"
				},
				"p2": {
					"endtime": "18:30",
					"periodid": 155486,
					"starttime": "18:00"
				},
				"p3": {
					"endtime": "19:00",
					"periodid": 155487,
					"starttime": "19:00"
				}
			},
			"fridayDayperiodid": 51829,
			"monday": {
				"dayperiodid": 51830,
				"p1": {
					"endtime": "09:20",
					"periodid": 155488,
					"starttime": "08:30"
				},
				"p2": {
					"endtime": "14:30",
					"periodid": 155489,
					"starttime": "14:00"
				},
				"p3": {
					"endtime": "19:30",
					"periodid": 155490,
					"starttime": "19:00"
				}
			},
			"mondayDayperiodid": 51830,
			"saturday": {
				"dayperiodid": 51831,
				"p1": {
					"endtime": "09:20",
					"periodid": 155491,
					"starttime": "08:30"
				},
				"p2": {
					"endtime": "14:30",
					"periodid": 155492,
					"starttime": "14:00"
				},
				"p3": {
					"endtime": "19:30",
					"periodid": 155493,
					"starttime": "19:00"
				}
			},
			"saturdayDayperiodid": 51831,
			"sunday": {
				"dayperiodid": 51832,
				"p1": {
					"endtime": "09:20",
					"periodid": 155494,
					"starttime": "08:30"
				},
				"p2": {
					"endtime": "14:30",
					"periodid": 155495,
					"starttime": "14:00"
				},
				"p3": {
					"endtime": "19:30",
					"periodid": 155496,
					"starttime": "19:00"
				}
			},
			"sundayDayperiodid": 51832,
			"thursday": {
				"dayperiodid": 51833,
				"p1": {
					"endtime": "07:50",
					"periodid": 155497,
					"starttime": "07:00"
				},
				"p2": {
					"endtime": "18:30",
					"periodid": 155498,
					"starttime": "18:00"
				},
				"p3": {
					"endtime": "19:00",
					"periodid": 155499,
					"starttime": "19:00"
				}
			},
			"thursdayDayperiodid": 51833,
			"tuesday": {
				"dayperiodid": 51834,
				"p1": {
					"endtime": "07:50",
					"periodid": 155500,
					"starttime": "07:00"
				},
				"p2": {
					"endtime": "18:30",
					"periodid": 155501,
					"starttime": "18:00"
				},
				"p3": {
					"endtime": "19:00",
					"periodid": 155502,
					"starttime": "19:00"
				}
			},
			"tuesdayDayperiodid": 51834,
			"wednesday": {
				"dayperiodid": 51835,
				"p1": {
					"endtime": "07:50",
					"periodid": 155503,
					"starttime": "07:00"
				},
				"p2": {
					"endtime": "18:30",
					"periodid": 155504,
					"starttime": "18:00"
				},
				"p3": {
					"endtime": "19:00",
					"periodid": 155505,
					"starttime": "19:00"
				}
			},
			"wednesdayDayperiodid": 51835,
			"zoneid": 7100
		},
		"receiverid": 3000,
		"scenarioScenarioid": null,
		"status": 1,
		"storedtargettemperature": 55.00,
		"targettemperature": 55.00,
		"zoneid": 7100
	}],
	"message": "succ.",
	"status": 0,
	"timestamp": 1572700800195
}
```

## Get Data for Zone

To get the data for a single zone POST the `zoneid` to `zones/data`.

### Request

```
POST /ember-back/zones/data HTTP/1.1
Authorization	long_token
Accept	application/json
```

JSON

```
{
	"zoneid": "7000"
}
```

# Response

```
{
	"data": {
		"areaid": null,
		"boostActivations": {
			"activatedon": "2019-10-29 22:01:36.357",
			"comments": null,
			"dispayFinishdatetime": "2019-10-30 00:00:00.000",
			"finishdatetime": "2019-10-30 00:00:00.000",
			"numberofhours": 1,
			"targettemperature": 24.00,
			"userid": 1000,
			"wascancelled": false,
			"zoneboostactivationid": 1330995,
			"zoneid": 7000
		},
		"boostTime1": null,
		"boostTime2": null,
		"boostTime3": null,
		"currenttemperature": 22.40,
		"hardwareid": "0",
		"homeName": "Home",
		"isadvanceactive": false,
		"isboostactive": false,
		"ishotwater": false,
		"isonline": true,
		"mode": 0,
		"name": "Heating",
		"prefix": "This zone is off until 14:00",
		"programmes": {
			"friday": {
				"dayperiodid": 51822,
				"p1": {
					"endtime": "08:10",
					"periodid": 155464,
					"starttime": "07:20"
				},
				"p2": {
					"endtime": "19:00",
					"periodid": 155465,
					"starttime": "18:00"
				},
				"p3": {
					"endtime": "23:00",
					"periodid": 155466,
					"starttime": "21:30"
				}
			},
			"fridayDayperiodid": 51822,
			"monday": {
				"dayperiodid": 51823,
				"p1": {
					"endtime": "09:20",
					"periodid": 155467,
					"starttime": "08:30"
				},
				"p2": {
					"endtime": "14:30",
					"periodid": 155468,
					"starttime": "14:00"
				},
				"p3": {
					"endtime": "19:30",
					"periodid": 155469,
					"starttime": "19:00"
				}
			},
			"mondayDayperiodid": 51823,
			"saturday": {
				"dayperiodid": 51824,
				"p1": {
					"endtime": "09:20",
					"periodid": 155470,
					"starttime": "08:30"
				},
				"p2": {
					"endtime": "14:30",
					"periodid": 155471,
					"starttime": "14:00"
				},
				"p3": {
					"endtime": "19:30",
					"periodid": 155472,
					"starttime": "19:00"
				}
			},
			"saturdayDayperiodid": 51824,
			"sunday": {
				"dayperiodid": 51825,
				"p1": {
					"endtime": "09:40",
					"periodid": 155473,
					"starttime": "08:40"
				},
				"p2": {
					"endtime": "17:00",
					"periodid": 155474,
					"starttime": "15:30"
				},
				"p3": {
					"endtime": "23:10",
					"periodid": 155475,
					"starttime": "22:50"
				}
			},
			"sundayDayperiodid": 51825,
			"thursday": {
				"dayperiodid": 51826,
				"p1": {
					"endtime": "08:10",
					"periodid": 155476,
					"starttime": "06:40"
				},
				"p2": {
					"endtime": "19:00",
					"periodid": 155477,
					"starttime": "17:40"
				},
				"p3": {
					"endtime": "23:00",
					"periodid": 155478,
					"starttime": "21:30"
				}
			},
			"thursdayDayperiodid": 51826,
			"tuesday": {
				"dayperiodid": 51827,
				"p1": {
					"endtime": "08:10",
					"periodid": 155479,
					"starttime": "06:40"
				},
				"p2": {
					"endtime": "19:00",
					"periodid": 155480,
					"starttime": "17:40"
				},
				"p3": {
					"endtime": "23:00",
					"periodid": 155481,
					"starttime": "21:30"
				}
			},
			"tuesdayDayperiodid": 51827,
			"wednesday": {
				"dayperiodid": 51828,
				"p1": {
					"endtime": "08:10",
					"periodid": 155482,
					"starttime": "07:20"
				},
				"p2": {
					"endtime": "19:00",
					"periodid": 155483,
					"starttime": "18:00"
				},
				"p3": {
					"endtime": "23:00",
					"periodid": 155484,
					"starttime": "21:30"
				}
			},
			"wednesdayDayperiodid": 51828,
			"zoneid": 7000
		},
		"receiverid": 3000,
		"scenarioScenarioid": null,
		"status": 1,
		"storedtargettemperature": 24.00,
		"targettemperature": 24.00,
		"zoneid": 7000
	},
	"message": "succ.",
	"status": 0,
	"timestamp": 1572700832616
}
```

## Update Zone Data / Programmes

To update the zone run times / programmes. POST the following to `zones/updateData`

### Request

```
POST /ember-back/zones/updateData HTTP/1.1
Authorization	long_token
Accept	application/json
```

JSON

```
{
	"data": [{
		"zoneid": "7000",
		"programmes": {
			"saturdayDayperiodid": 51831,
			"sunday": {
				"dayperiodid": 51832,
				"period3id": 0,
				"p3": {
					"endtime": "19:30",
					"type": 0,
					"periodid": 155496,
					"starttime": "19:00"
				},
				"p1": {
					"endtime": "09:20",
					"type": 0,
					"periodid": 155494,
					"starttime": "08:30"
				},
				"period1id": 0,
				"period2id": 0,
				"p2": {
					"endtime": "14:30",
					"type": 0,
					"periodid": 155495,
					"starttime": "14:00"
				}
			},
			"sundayDayperiodid": 51832,
			"mondayDayperiodid": 51830,
			"saturday": {
				"dayperiodid": 51831,
				"period3id": 0,
				"p3": {
					"endtime": "19:30",
					"type": 0,
					"periodid": 155493,
					"starttime": "18:50"
				},
				"p1": {
					"endtime": "09:20",
					"type": 0,
					"periodid": 155491,
					"starttime": "08:30"
				},
				"period1id": 0,
				"period2id": 0,
				"p2": {
					"endtime": "14:30",
					"type": 0,
					"periodid": 155492,
					"starttime": "14:00"
				}
			},
			"fridayDayperiodid": 51829,
			"thursday": {
				"dayperiodid": 51833,
				"period3id": 0,
				"p3": {
					"endtime": "19:00",
					"type": 0,
					"periodid": 155499,
					"starttime": "19:00"
				},
				"p1": {
					"endtime": "07:50",
					"type": 0,
					"periodid": 155497,
					"starttime": "07:00"
				},
				"period1id": 0,
				"period2id": 0,
				"p2": {
					"endtime": "18:30",
					"type": 0,
					"periodid": 155498,
					"starttime": "18:00"
				}
			},
			"friday": {
				"dayperiodid": 51829,
				"period3id": 0,
				"p3": {
					"endtime": "19:00",
					"type": 0,
					"periodid": 155487,
					"starttime": "19:00"
				},
				"p1": {
					"endtime": "07:50",
					"type": 0,
					"periodid": 155485,
					"starttime": "07:00"
				},
				"period1id": 0,
				"period2id": 0,
				"p2": {
					"endtime": "18:30",
					"type": 0,
					"periodid": 155486,
					"starttime": "18:00"
				}
			},
			"tuesdayDayperiodid": 51834,
			"monday": {
				"dayperiodid": 51830,
				"period3id": 0,
				"p3": {
					"endtime": "19:30",
					"type": 0,
					"periodid": 155490,
					"starttime": "19:00"
				},
				"p1": {
					"endtime": "09:20",
					"type": 0,
					"periodid": 155488,
					"starttime": "08:30"
				},
				"period1id": 0,
				"period2id": 0,
				"p2": {
					"endtime": "14:30",
					"type": 0,
					"periodid": 155489,
					"starttime": "14:00"
				}
			},
			"tuesday": {
				"dayperiodid": 51834,
				"period3id": 0,
				"p3": {
					"endtime": "19:00",
					"type": 0,
					"periodid": 155502,
					"starttime": "19:00"
				},
				"p1": {
					"endtime": "07:50",
					"type": 0,
					"periodid": 155500,
					"starttime": "07:00"
				},
				"period1id": 0,
				"period2id": 0,
				"p2": {
					"endtime": "18:30",
					"type": 0,
					"periodid": 155501,
					"starttime": "18:00"
				}
			},
			"wednesdayDayperiodid": 51835,
			"thursdayDayperiodid": 51833,
			"zoneid": "7100",
			"wednesday": {
				"dayperiodid": 51835,
				"period3id": 0,
				"p3": {
					"endtime": "19:00",
					"type": 0,
					"periodid": 155505,
					"starttime": "19:00"
				},
				"p1": {
					"endtime": "07:50",
					"type": 0,
					"periodid": 155503,
					"starttime": "07:00"
				},
				"period1id": 0,
				"period2id": 0,
				"p2": {
					"endtime": "18:30",
					"type": 0,
					"periodid": 155504,
					"starttime": "18:00"
				}
			}
		}
	}]
}
```

# Response

```
{
	"data": null,
	"message": "succ.",
	"status": 0,
	"timestamp": 1572701190148
}
```

## Set Zone Mode / Run Selection

Modes control when your heating controls will be turn on. The supported modes are

* Off - 3 - Always off
* On - 2 - Always on
* All Day - 1 - Starts at start time of period 1 and ends at the end time of period 3
* Auto - 0 - Based on the times you have configured.

This is equalivent to the "Run Selection" setting in the app.

### Request

```
POST /ember-back/zones/setModel HTTP/1.1
Authorization	long_token
Accept	application/json
```

JSON

```
{
	"model": "0",
	"zoneid": "7000"
}
```

# Response

```
{
	"data": null,
	"message": "succ.",
	"status": 0,
	"timestamp": 1572701190148
}
```


## Advance the Zone

Advancing the zone moves it to the next configured run selection. To advance a zone pass the `zoneId` to `zones/adv`

### Request

```
POST /ember-back/zones/adv HTTP/1.1
Authorization	long_token
Accept	application/json
```

The JSON to send is:

```
{
	"zoneid": "7000"
}
```
# Response

```
{
	"data": null,
	"message": "succ.",
	"status": 0,
	"timestamp": 1572386496332
}
```

## Cancel Advance

To cancel advance you pass the `zoneId` that you would like to deactivate to `zones/cancelAdv`.

### Request

```
POST /ember-back/zones/cancelBoost HTTP/1.1
Authorization	long_token
Accept	application/json
```

The JSON to send is:

```
{
	"zoneid": "7000"
}
```
# Response

```
{
	"data": null,
	"message": "succ.",
	"status": 0,
	"timestamp": 1572386496332
}
```


## Other API Calls

Some other calls that I have seen but not investigated include:

### Weather

```
GET /ember-back/homes/weathInfo HTTP/1.1
Authorization	long_token
Accept	application/json
```

JSON

```
{
	"gateWayId": "gwid1234"
}
```

Response

{
	"data": null,
	"message": "succ.",
	"status": 0,
	"timestamp": 1572386471743
}


### Frost Protection

```
GET /ember-back/homes/changeFrostProtection HTTP/1.1
Authorization	long_token
Accept	application/json
```

JSON

```
{
	"button": "off",
	"gateWayId": "gwid1234"
}
```
To above will turn off frost protection. To turn on frost protection set `button` to `on`.

Response

{
	"data": null,
	"message": "succ.",
	"status": 0,
	"timestamp": 1572386471743
}

