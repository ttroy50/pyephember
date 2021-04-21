# API

Note: I have no connection with EPHControls and this API may be subject to change. Use of this API is at your own risk.

## API versions

The ember API was updated in January 2021 and users are slowly being moved to the new API. The document describing the old API from 2020 is available from [here](AIP_2020.md)

## Intro

The ember API is a dual HTTPs and MQTT endpoint. 

HTTP with JSON is used for authentication, admin, and getting zone information. 

MQTT with JSON is used for reading and updating some zone information (e.g. target temperature)

## URLS

### HTTP

The base HTTP URL is https://eu-https.topband-cloud.com/ember-back. This will be referred to as $HTTP_ENDPOINT for the rest of the document. 

### MQTT

The MQTT URL used is eu-base-mqtt.topband-cloud.com:18883 and uses TLS to encrypt the traffic. This will be referred to as $MQTT_ENDPOINT for the rest of the document.


# HTTP API Calls

## Login

Initial login uses the email and password you used to register with the system. Subsequent requests are then authenticated using an access token that is returned during the initial login.

You can use any valid user for this but it would be a good idea to not use the super user for your home and have a dedicated API user

### Request

To login for the first time send a POST to $HTTP_ENDPOINT/appLogin/login with a JSON request containing your username and password.

```
POST /ember-back/appLogin/login HTTP/2.0
Accept	application/json
Content-Type	application/json;charset=utf-8
```

The form data to POST is

```
{
	"password": "password",
	"model": "iPhone XS",
	"os": "13.5",
	"type": 2,
	"appVersion": "2.0.4",
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
	"timestamp": 1615150233365
}
```

The `token` is required for subsequent requests so it is important to keep this, this should be sent in the Authorization header for all other requests. 

The `refresh_token` can be used to update the authorization token and should be kept if you are planning on having longer sessions.

## Refresh Auth Token

To refresh your access token, send a GET to `$HTTP_ENDPOINT/appLogin/refreshAccessToken` using the `refresh_token` from your login request in the Authorization header 

It is unclear how long an access token last for however, it looks to last at least 1 hour. 

```
GET /ember-back/appLogin/refreshAccessToken HTTP/2.0
Accept	application/json
Authorization	long_refresh_token
```

### Response

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

## Report Token

The report token message is sent after login. It is unknown that this message does but I don't believe it is required for general usage of the API.

### Request

The request is a POST to `$HTTP_ENDPOING/user/reportToken` 

```
GET /ember-back/user/reportToken HTTP/2.0
Authorization	long_token
Accept	application/json
```

With the following JSON

```
{
	"os": "ios",
	"phoneToken": "really_long_phone_token",
	"type": 1,
	"appVersion": "2.0.4"
}
```

### Response

The response is the following JSON.

```
{
	"data": null,
	"message": null,
	"status": 0,
	"timestamp": 1615150233469
}
```


## Select User

After login the select user call is made to get user information for the app. 


To make a call to select user send a GET request to `$HTTP_ENDPOING/user/selectUser` with the token in the Authourization header. 

### Request

```
GET /ember-back/user/selectUser HTTP/2.0
Authorization	long_token
Accept	application/json
```

### Response

The response is a JSON message that includes information about the user.


```

{
	"data": {
		"accessfailedcount": 0,
		"appVersion": "2.0.4",
		"areacode": null,
		"email": "user@email.com",
		"emailconfirmed": true,
		"firstname": "Me",
		"id": 1111,
		"ip": null,
		"lastname": "Me",
		"lockoutenabled": true,
		"lockoutenddateutc": null,
		"model": "iPhone XS",
		"newsmarketing": false,
		"os": "13.5",
		"phonenumber": "0871234567",
		"phonenumberconfirmed": false,
		"primaryexternalloginprovider": null,
		"profilepictureuri": null,
		"profilepicurelastsynced": null,
		"protocolstatus": 1,
		"registrationtime": null,
		"securitystamp": "f9e3098b-7b99-45a0-bc23-7f4b399edde6",
		"synchroniseprofilepicture": false,
		"systemmaintenance": false,
		"twofactorenabled": false,
		"type": 2,
		"useprimaryexternalproviderpicture": false,
		"username": "user@email.com"
	},
	"message": "The query is successful",
	"status": 0,
	"timestamp": 1615150233473
}
```

## Get Available Homes

To get the list of available homes 

### Request

The request is a GET to the URL `$ENDPOINT/homes/list`.

```
GET /ember-back/homes/list HTTP/2.0
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
		"invitecode": "ABCD",
		"name": "Home",
		"productId": null,
		"uid": null,
		"zoneCount": 2
	}, {
		"deviceType": 3,
		"gatewayid": "gwid1111",
		"invitecode": "DDDD",
		"name": "Home",
		"productId": "1234abcd",
		"uid": "011011",
		"zoneCount": 1
	}],
	"message": "succ.",
	"status": 0,
	"timestamp": 1615150233565
}
```

The `gatewayid` is required for later requests to identify the home that is being controlled.


## Get Home Details

To get details of your home, you should use the `gatewayid` returned from the `homes/list` request above.

### Request

The request is a POST to the URL `$ENDPOINT/homes/detail` passing the `gatewayid` in a JSON request

```
GET /ember-back/homes/detail HTTP/2.0
Authorization	long_token
Accept	application/json
```

The JSON to send is:

```
{
	"gateWayId": "gwid1111"
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
			"userid": 1111,
			"zoneboostactivated": false,
			"zonescheduleupdated": false
		},
		"curAccess": {
			"areamanagement": true,
			"boost": true,
			"eventmanagement": true,
			"holidays": true,
			"homemanagement": false,
			"homeuserid": "homeuserid980",
			"roleId": 5,
			"scenariomanagement": true,
			"schedulesmanagement": true
		},
		"wifiVersion": 100116,
		"homes": {
			"deviceType": 3,
			"frostprotectionenabled": null,
			"gatewayid": "gwid1111",
			"holidaymodeactive": null,
			"invitecode": "59A64",
			"name": "Home",
			"pointDataList": [{
				"createTime": "2021-01-29 14:01:55",
				"delFlag": 0,
				"deviceId": "deviceidc99999",
				"id": "id444",
				"pointAttribute": null,
				"pointIndex": 6,
				"pointName": "FrostEnable",
				"pointType": 1,
				"productId": "productid135",
				"uid": "uid011",
				"updateTime": "2021-01-29 14:01:55",
				"value": "1"
			}, {
				"createTime": "2021-01-29 14:01:55",
				"delFlag": 0,
				"deviceId": "deviceid07",
				"id": "pdlidc3ce",
				"pointAttribute": null,
				"pointIndex": 8,
				"pointName": "FrostSetTemp",
				"pointType": 1,
				"productId": "productid135",
				"uid": "uid011",
				"updateTime": "2021-01-29 14:01:55",
				"value": "5"
			}, {
				"createTime": "2021-01-29 14:01:25",
				"delFlag": 0,
				"deviceId": "deviceidc99999",
				"id": "pdlidf4a8",
				"pointAttribute": null,
				"pointIndex": 10,
				"pointName": "HolidayEndTime",
				"pointType": 5,
				"productId": "productid135",
				"uid": "uid011",
				"updateTime": "2021-01-29 14:01:25",
				"value": "0"
			}, {
				"createTime": "2021-01-29 14:01:55",
				"delFlag": 0,
				"deviceId": "deviceidc99999",
				"id": "pdlid209b",
				"pointAttribute": null,
				"pointIndex": 2,
				"pointName": "WifiRssi",
				"pointType": 1,
				"productId": "productid135",
				"uid": "uid011",
				"updateTime": "2021-01-29 14:01:55",
				"value": "100"
			}, {
				"createTime": "2021-01-29 14:01:25",
				"delFlag": 0,
				"deviceId": "deviceidc99999",
				"id": "pdlid6782a",
				"pointAttribute": null,
				"pointIndex": 4,
				"pointName": "HolidayFlag",
				"pointType": 1,
				"productId": "productid135",
				"uid": "uid011",
				"updateTime": "2021-01-29 14:01:25",
				"value": "0"
			}, {
				"createTime": "2021-01-29 14:01:25",
				"delFlag": 0,
				"deviceId": "deviceidc99999",
				"id": "pdlid2498",
				"pointAttribute": null,
				"pointIndex": 5,
				"pointName": "HolidayCnt",
				"pointType": 5,
				"productId": "productid135",
				"uid": "uid011",
				"updateTime": "2021-01-29 14:01:25",
				"value": "0"
			}, {
				"createTime": "2021-01-29 14:01:25",
				"delFlag": 0,
				"deviceId": "deviceidc99999",
				"id": "pdlid5aa6",
				"pointAttribute": null,
				"pointIndex": 9,
				"pointName": "HolidayStartTime",
				"pointType": 5,
				"productId": "productid135",
				"uid": "uid011",
				"updateTime": "2021-01-29 14:01:25",
				"value": "0"
			}, {
				"createTime": "2021-01-29 14:01:55",
				"delFlag": 0,
				"deviceId": "deviceidc99999",
				"id": "pdlidcbf8",
				"pointAttribute": null,
				"pointIndex": 7,
				"pointName": "NoFrostStatus",
				"pointType": 1,
				"productId": "productid135",
				"uid": "uid011",
				"updateTime": "2021-01-29 14:01:55",
				"value": "0"
			}],
			"productId": "productid135",
			"quickboosttemperature": 20.00,
			"sysTemType": "EMBER-PS",
			"uid": "uid011",
			"weatherlocation": null,
			"zoneCount": 1
		},
		"mcuVersion": 0
	},
	"message": "succ.",
	"status": 0,
	"timestamp": 1615150236340
}
```

### Notes

This response contains information about the home and of particular for us is looking at the `pointDataList`. 

Point Data is used as part of later JSON responses, and also as part of the MQTT requests and responses. The information from this requests can be used to help us find the index, type and initial value for a particular data list.


## Get Zones Information

To get details of your available zones, you should send the `gatewayid` to the `homesVT/zoneProgram` endpoint.

### Request

The request is a POST to the URL `$ENDPOINT/homesVT/zoneProgram` passing the `gatewayid` in a JSON request

```
GET /ember-back/homesVT/zoneProgram HTTP/2.0
Authorization	long_token
Accept	application/json
```

The JSON to send is:

```
{
	"gateWayId": "gwid1111"
}
```

### Response

The response is JSON 

```
{
	"data": [{
		"deviceDays": [{
			"dayType": 0,
			"deviceId": "productid135",
			"id": "devicedayiddb17",
			"p1": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 70,
				"id": "programidb5c1",
				"startTime": 70,
				"updateTime": "2021-03-07 20:45:07.000"
			},
			"p2": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 120,
				"id": "programid2b84d",
				"startTime": 120,
				"updateTime": "2021-03-07 20:45:07.000"
			},
			"p3": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 170,
				"id": "programid273ea",
				"startTime": 170,
				"updateTime": "2021-03-07 20:45:07.000"
			}
		}, {
			"dayType": 1,
			"deviceId": "productid135",
			"id": "devicedayid57efb",
			"p1": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 80,
				"id": "programida7c41",
				"startTime": 80,
				"updateTime": "2021-03-07 20:45:07.000"
			},
			"p2": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 120,
				"id": "programid8ea2e",
				"startTime": 120,
				"updateTime": "2021-03-07 20:45:07.000"
			},
			"p3": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 213,
				"id": "programid0b9a",
				"startTime": 170,
				"updateTime": "2021-03-07 20:45:07.000"
			}
		}, {
			"dayType": 2,
			"deviceId": "productid135",
			"id": "devicedayidb8b59",
			"p1": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 80,
				"id": "programid9e9f0",
				"startTime": 80,
				"updateTime": "2021-03-07 20:45:07.000"
			},
			"p2": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 120,
				"id": "programidb169c8",
				"startTime": 120,
				"updateTime": "2021-03-07 20:45:07.000"
			},
			"p3": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 213,
				"id": "programided6f",
				"startTime": 170,
				"updateTime": "2021-03-07 20:45:07.000"
			}
		}, {
			"dayType": 3,
			"deviceId": "productid135",
			"id": "devicedayidf99",
			"p1": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 80,
				"id": "programid76158",
				"startTime": 80,
				"updateTime": "2021-03-07 20:45:07.000"
			},
			"p2": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 120,
				"id": "programidbfb",
				"startTime": 120,
				"updateTime": "2021-03-07 20:45:07.000"
			},
			"p3": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 213,
				"id": "programid15319",
				"startTime": 170,
				"updateTime": "2021-03-07 20:45:07.000"
			}
		}, {
			"dayType": 4,
			"deviceId": "productid135",
			"id": "devicedayid446b",
			"p1": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 80,
				"id": "programid4a789",
				"startTime": 80,
				"updateTime": "2021-03-07 20:45:07.000"
			},
			"p2": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 120,
				"id": "programid468e2",
				"startTime": 120,
				"updateTime": "2021-03-07 20:45:07.000"
			},
			"p3": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 213,
				"id": "programidaa4e2",
				"startTime": 170,
				"updateTime": "2021-03-07 20:45:07.000"
			}
		}, {
			"dayType": 5,
			"deviceId": "productid135",
			"id": "devicedayid8341e",
			"p1": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 80,
				"id": "programid44f5c",
				"startTime": 80,
				"updateTime": "2021-03-07 20:45:07.000"
			},
			"p2": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 120,
				"id": "programidde00",
				"startTime": 120,
				"updateTime": "2021-03-07 20:45:07.000"
			},
			"p3": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 213,
				"id": "programid3754",
				"startTime": 170,
				"updateTime": "2021-03-07 20:45:07.000"
			}
		}, {
			"dayType": 6,
			"deviceId": "productid135",
			"id": "devicedayid97c5e",
			"p1": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 70,
				"id": "programid840a5",
				"startTime": 70,
				"updateTime": "2021-03-07 20:45:07.000"
			},
			"p2": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 120,
				"id": "programid7c333",
				"startTime": 120,
				"updateTime": "2021-03-07 20:45:07.000"
			},
			"p3": {
				"createTime": "2021-01-29 14:01:54.000",
				"delFlag": 0,
				"endTime": 170,
				"id": "programid911ee",
				"startTime": 170,
				"updateTime": "2021-03-07 20:45:07.000"
			}
		}],
		"deviceType": 2,
		"isonline": true,
		"mac": "acacacac",
		"name": "home",
		"pointDataList": [{
			"pointIndex": 11,
			"value": "0"
		}, {
			"pointIndex": 3,
			"value": "12"
		}, {
			"pointIndex": 4,
			"value": "0"
		}, {
			"pointIndex": 13,
			"value": "1"
		}, {
			"pointIndex": 10,
			"value": "1"
		}, {
			"pointIndex": 14,
			"value": "205"
		}, {
			"pointIndex": 8,
			"value": "0"
		}, {
			"pointIndex": 7,
			"value": "0"
		}, {
			"pointIndex": 5,
			"value": "192"
		}, {
			"pointIndex": 9,
			"value": "0"
		}, {
			"pointIndex": 6,
			"value": "200"
		}],
		"productId": "productid135",
		"systemType": "EMBER-PS",
		"uid": "uid011",
		"zoneid": "zoneid9b"
	}],
	"message": "succ.",
	"status": 0,
	"timestamp": 1615150236609
}
```

### Notes

This request is one of the brand new requests from the new API. It includes information from all zones including the zone

  * Timer schedule. 
  * Point data information

The point data here contains the index and value type. The value type depends on the index. A full list of the index and value information will be provided later in the document. 

## Get Zone Program

To get details of your a single zones, you should send the `zoneid` to the `homesVT/zoneViewProgram` endpoint.

### Request

The request is a POST to the URL `$ENDPOINT/homesVT/zoneViewProgram` passing the `zoneid` in a JSON request

```
GET /ember-back/homesVT/zoneViewProgram HTTP/2.0
Authorization	long_token
Accept	application/json
```

The JSON to send is:

```
{
	"zoneid": "zoneid9b"
}
```

### Response

The response is JSON 

```
{
    "data": {
    	"deviceDays": [{
            "dayType": 0,
            "deviceId": "productid135",
            "id": "devicedayiddb17",
            "p1": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 70,
                "id": "programidb5c1",
                "startTime": 70,
                "updateTime": "2021-03-07 20:45:07.000"
            },
            "p2": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 120,
                "id": "programid2b84d",
                "startTime": 120,
                "updateTime": "2021-03-07 20:45:07.000"
            },
            "p3": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 170,
                "id": "programid273ea",
                "startTime": 170,
                "updateTime": "2021-03-07 20:45:07.000"
            }
        }, {
            "dayType": 1,
            "deviceId": "productid135",
            "id": "devicedayid57efb",
            "p1": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 80,
                "id": "programida7c41",
                "startTime": 80,
                "updateTime": "2021-03-07 20:45:07.000"
            },
            "p2": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 120,
                "id": "programid8ea2e",
                "startTime": 120,
                "updateTime": "2021-03-07 20:45:07.000"
            },
            "p3": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 213,
                "id": "programid0b9a",
                "startTime": 170,
                "updateTime": "2021-03-07 20:45:07.000"
            }
        }, {
            "dayType": 2,
            "deviceId": "productid135",
            "id": "devicedayidb8b59",
            "p1": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 80,
                "id": "programid9e9f0",
                "startTime": 80,
                "updateTime": "2021-03-07 20:45:07.000"
            },
            "p2": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 120,
                "id": "programidb169c8",
                "startTime": 120,
                "updateTime": "2021-03-07 20:45:07.000"
            },
            "p3": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 213,
                "id": "programided6f",
                "startTime": 170,
                "updateTime": "2021-03-07 20:45:07.000"
            }
        }, {
            "dayType": 3,
            "deviceId": "productid135",
            "id": "devicedayidf99",
            "p1": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 80,
                "id": "programid76158",
                "startTime": 80,
                "updateTime": "2021-03-07 20:45:07.000"
            },
            "p2": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 120,
                "id": "programidbfb",
                "startTime": 120,
                "updateTime": "2021-03-07 20:45:07.000"
            },
            "p3": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 213,
                "id": "programid15319",
                "startTime": 170,
                "updateTime": "2021-03-07 20:45:07.000"
            }
        }, {
            "dayType": 4,
            "deviceId": "productid135",
            "id": "devicedayid446b",
            "p1": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 80,
                "id": "programid4a789",
                "startTime": 80,
                "updateTime": "2021-03-07 20:45:07.000"
            },
            "p2": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 120,
                "id": "programid468e2",
                "startTime": 120,
                "updateTime": "2021-03-07 20:45:07.000"
            },
            "p3": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 213,
                "id": "programidaa4e2",
                "startTime": 170,
                "updateTime": "2021-03-07 20:45:07.000"
            }
        }, {
            "dayType": 5,
            "deviceId": "productid135",
            "id": "devicedayid8341e",
            "p1": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 80,
                "id": "programid44f5c",
                "startTime": 80,
                "updateTime": "2021-03-07 20:45:07.000"
            },
            "p2": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 120,
                "id": "programidde00",
                "startTime": 120,
                "updateTime": "2021-03-07 20:45:07.000"
            },
            "p3": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 213,
                "id": "programid3754",
                "startTime": 170,
                "updateTime": "2021-03-07 20:45:07.000"
            }
        }, {
            "dayType": 6,
            "deviceId": "productid135",
            "id": "devicedayid97c5e",
            "p1": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 70,
                "id": "programid840a5",
                "startTime": 70,
                "updateTime": "2021-03-07 20:45:07.000"
            },
            "p2": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 120,
                "id": "programid7c333",
                "startTime": 120,
                "updateTime": "2021-03-07 20:45:07.000"
            },
            "p3": {
                "createTime": "2021-01-29 14:01:54.000",
                "delFlag": 0,
                "endTime": 170,
                "id": "programid911ee",
                "startTime": 170,
                "updateTime": "2021-03-07 20:45:07.000"
            }
        }],
        "deviceType": 2,
        "isonline": true,
        "mac": "acacacac",
        "name": "home",
        "pointDataList": [{
            "pointIndex": 11,
            "value": "0"
        }, {
            "pointIndex": 3,
            "value": "12"
        }, {
            "pointIndex": 4,
            "value": "0"
        }, {
            "pointIndex": 13,
            "value": "1"
        }, {
            "pointIndex": 10,
            "value": "1"
        }, {
            "pointIndex": 14,
            "value": "205"
        }, {
            "pointIndex": 8,
            "value": "0"
        }, {
            "pointIndex": 7,
            "value": "0"
        }, {
            "pointIndex": 5,
            "value": "192"
        }, {
            "pointIndex": 9,
            "value": "0"
        }, {
            "pointIndex": 6,
            "value": "200"
        }],
        "productId": "productid135",
        "systemType": "EMBER-PS",
        "uid": "uid011",
        "zoneid": "zoneid9b"
    },
    "message": "succ.",
    "status": 0,
    "timestamp": 1613335284263
}
```

### Notes

The information here is the same as a single zone information from the previous zoneProgram information.

# MQTT API Calls

## MQTT Basics

MQTT is a pub/sub protocol for sending messages between a client and server.

A client can subscribed to a topic that lets them receive messages about a topic.

A client can also publish messages to a topic to inform other entities about a change.

## Connect

The first thing the client does after connecting is to send a `Connect Command` 

### Request


```
MQ Telemetry Transport Protocol, Connect Command
    Header Flags: 0x10, Message Type: Connect Command
    Msg Len: 102
    Protocol Name Length: 4
    Protocol Name: MQTT
    Version: MQTT v3.1.1 (4)
    Connect Flags: 0xca, User Name Flag, Password Flag, QoS Level: At least once delivery (Acknowledged deliver), Clean Session Flag
        1... .... = User Name Flag: Set
        .1.. .... = Password Flag: Set
        ..0. .... = Will Retain: Not set
        ...0 1... = QoS Level: At least once delivery (Acknowledged deliver) (1)
        .... .0.. = Will Flag: Not set
        .... ..1. = Clean Session Flag: Set
        .... ...0 = (Reserved): Not set
    Keep Alive: 60
    Client ID Length: 18
    Client ID: 1111_1613126074181
    User Name Length: 36
    User Name: app/really_long_refresh_token
    Password Length: 32
    Password: really_long_refresh_token
```

The client ID is the `id` returned from `selectUser` request followed by token. `<id>_<other>`. The other part of the id appears to be a unix timestamp.

The User Name is the refresh token from the HTTP Login request with `app/` prefixed.

The Password is the same refresh token.

### Respoonse

The response is a `Connect Ack`

```
MQ Telemetry Transport Protocol, Connect Ack
    Header Flags: 0x20, Message Type: Connect Ack
    Msg Len: 2
    Acknowledge Flags: 0x00
    Return Code: Connection Accepted (0)

```

## Subscriptions

When starting the client subscribes to the following topics.

### Point Data

```
MQ Telemetry Transport Protocol, Subscribe Request
    Header Flags: 0x82, Message Type: Subscribe Request
    Msg Len: 87
    Message Identifier: 2
    Topic Length: 82
    Topic: productid135/uid011/upload/pointdata
    Requested QoS: At most once delivery (Fire and Forget) (0)
```

The topic is made up of information from your home. This is the `productid` and `uid` from the `homes/detail` request in the HTTP API


### Notification App

```
MQ Telemetry Transport Protocol, Subscribe Request
    Header Flags: 0x82, Message Type: Subscribe Request
    Msg Len: 65
    Message Identifier: 3
    Topic Length: 60
    Topic: id7a55/1111/notificationApp/update
    Requested QoS: At most once delivery (Fire and Forget) (0)

```

The notificaiton app topic includes an `<id>/<client id>/notificationApp/update`

 * `<id>` - TODO - figure out what this is
 * `<client id>` - client ID from selectUser request.


### Device Remove 1


```
MQ Telemetry Transport Protocol, Subscribe Request
    Header Flags: 0x82, Message Type: Subscribe Request
    Msg Len: 56
    Message Identifier: 5
    Topic Length: 51
    Topic: productid135/1111/device/remove
    Requested QoS: At most once delivery (Fire and Forget) (0)

```

The notificaiton app topic includes an `<product id>/<client id>/device/remove`

 * `<product id>` - Product ID from the `homes/detail` response.
 * `<client id>` - client ID from selectUser request.

### Device Remove 2


```
MQ Telemetry Transport Protocol, Subscribe Request
    Header Flags: 0x82, Message Type: Subscribe Request
    Msg Len: 56
    Message Identifier: 6
    Topic Length: 51
    Topic: id27b5/1111/device/remove
    Requested QoS: At most once delivery (Fire and Forget) (0)

```

The notificaiton app topic includes an `<id>/<client id>/device/remove`

 * `<id>` - TODO - figure out what this is
 * `<client id>` - client ID from selectUser request.

### Responses

Each subscribe request has a `Subscribe Ack` response for the message identifier.

```
MQ Telemetry Transport Protocol, Subscribe Ack
    Header Flags: 0x90, Message Type: Subscribe Ack
    Msg Len: 3
    Message Identifier: 2
    Granted QoS: At most once delivery (Fire and Forget) (0)
```

## Publish to Upload Point Data

The upload point data publish message sends a message with JSON data to the `upload/pointdata` topic. The topic name includes the `productid` and `uid` in the topic as `productid135/uid011/upload/pointdata`

TODO - figure out when this is sent. Client -> server or server -> client

### Request


```
MQ Telemetry Transport Protocol, Publish Message
    Header Flags: 0x30, Message Type: Publish Message, QoS Level: At most once delivery (Fire and Forget)
    Msg Len: 269
    Topic Length: 82
    Topic: productid135/uid011/upload/pointdata
    Message: json_data

```

The JSON data is as follows
```
{
  "common":{
    "serial":7870,
    "productId":"productid135",
    "uid":"uid011",
    "timestamp":1623115
  },
  "data":{
    "mac":"acacacac",
    "pointData":"AAYEAL4="
  }
}
```
 * `serial` - TODO - figure out what this is
 * `productId` - as per the topic
 * `uid` - as per the topic
 * `mac` indicates the zone that this data is from and can be found in the `zoneProgram` or `zoneViewProgram` data.
 * `pointData` is base64 encoded binary data that indicates the point data information


In this example the point data `AAYEAL4=` decodes to `00000000 00000110 00000100 00000000 10111110`. 

If you break this up the first 2 bytes are the point index, the next one is the point type and the final bytes are the value.

For this example we have:

 * index - 6
 * type - 4
 * value - 190

If you look at this compared to the `zoneProgram`, we can see that the zone program `pointDataList` contains:

```
{
    pointIndex": 6,
    "value": "190"
}
```

This matches up to the target temperature for the zone. 

More information on the Point Data list is available later in this document.  

### Response

The upload point data is a fire and forget message and there is no ack message or response.

## Publish to Download Point Data


The download point data publish message sends a message with JSON data to the `download/pointdata` topic. The topic name includes the `productid` and `uid` in the topic as `productid135/uid011/download/pointdata`

TODO - figure out when this is sent. Client -> server or server -> client


### Request

```
MQ Telemetry Transport Protocol, Publish Message
    Header Flags: 0x32, Message Type: Publish Message, QoS Level: At least once delivery (Acknowledged deliver)
    Msg Len: 296
    Topic Length: 84
    Topic: productid135/uid011/download/pointdata
    Message Identifier: 8
    Message: json_data

```

```
{
  "data":{
    "mac":"acacacac",
    "pointData":"AAYEALk="
  },
  "common":{
    "timestamp":1615749905466,
    "serial":905466,
    "productId":"productid135",
    "uid":"uid011",
    "userId":"1111"
  }
}
```

 * `serial` - TODO - figure out what this is
 * `productId` - as per the topic
 * `uid` - as per the topic
 * `mac` indicates the zone that this data is from and can be found in the `zoneProgram` or `zoneViewProgram` data.
 * `pointData` is base64 encoded binary data that indicates the point data information
 * `userId` - The client id from the selectUser request

### Response

The response is a `Publish Ack` message

```
MQ Telemetry Transport Protocol, Publish Ack
    Header Flags: 0x40, Message Type: Publish Ack
    Msg Len: 2
    Message Identifier: 8
```

## Ping Request

The client seems to regurarly send a ping request to the server as a keep alive.

### Request

```
MQ Telemetry Transport Protocol, Ping Request
    Header Flags: 0xc0, Message Type: Ping Request
    Msg Len: 0
```

### Response

```
MQ Telemetry Transport Protocol, Ping Response
    Header Flags: 0xd0, Message Type: Ping Response
    Msg Len: 0
```

## Disconnect Request

When closing the client sends a disconnect request

### Request

```
MQ Telemetry Transport Protocol, Disconnect Req
    Header Flags: 0xe0, Message Type: Disconnect Req
    Msg Len: 0
```


# Point Data

The point data information is the way to transmit data about parts of the system. Point data is used in a number of messages and seems to relate to two different types of elements:

 * Home Details
 * Zone Details

## Homes Details

```
"pointDataList": [{
		"createTime": "2021-01-29 14:01:55",
		"delFlag": 0,
		"deviceId": "deviceidc99999",
		"id": "id444",
		"pointAttribute": null,
		"pointIndex": 6,
		"pointName": "FrostEnable",
		"pointType": 1,
		"productId": "productid135",
		"uid": "uid011",
		"updateTime": "2021-01-29 14:01:55",
		"value": "1"
	}, {
		"createTime": "2021-01-29 14:01:55",
		"delFlag": 0,
		"deviceId": "deviceid07",
		"id": "pdlidc3ce",
		"pointAttribute": null,
		"pointIndex": 8,
		"pointName": "FrostSetTemp",
		"pointType": 1,
		"productId": "productid135",
		"uid": "uid011",
		"updateTime": "2021-01-29 14:01:55",
		"value": "5"
	}, {
		"createTime": "2021-01-29 14:01:25",
		"delFlag": 0,
		"deviceId": "deviceidc99999",
		"id": "pdlidf4a8",
		"pointAttribute": null,
		"pointIndex": 10,
		"pointName": "HolidayEndTime",
		"pointType": 5,
		"productId": "productid135",
		"uid": "uid011",
		"updateTime": "2021-01-29 14:01:25",
		"value": "0"
	}, {
		"createTime": "2021-01-29 14:01:55",
		"delFlag": 0,
		"deviceId": "deviceidc99999",
		"id": "pdlid209b",
		"pointAttribute": null,
		"pointIndex": 2,
		"pointName": "WifiRssi",
		"pointType": 1,
		"productId": "productid135",
		"uid": "uid011",
		"updateTime": "2021-01-29 14:01:55",
		"value": "100"
	}, {
		"createTime": "2021-01-29 14:01:25",
		"delFlag": 0,
		"deviceId": "deviceidc99999",
		"id": "pdlid6782a",
		"pointAttribute": null,
		"pointIndex": 4,
		"pointName": "HolidayFlag",
		"pointType": 1,
		"productId": "productid135",
		"uid": "uid011",
		"updateTime": "2021-01-29 14:01:25",
		"value": "0"
	}, {
		"createTime": "2021-01-29 14:01:25",
		"delFlag": 0,
		"deviceId": "deviceidc99999",
		"id": "pdlid2498",
		"pointAttribute": null,
		"pointIndex": 5,
		"pointName": "HolidayCnt",
		"pointType": 5,
		"productId": "productid135",
		"uid": "uid011",
		"updateTime": "2021-01-29 14:01:25",
		"value": "0"
	}, {
		"createTime": "2021-01-29 14:01:25",
		"delFlag": 0,
		"deviceId": "deviceidc99999",
		"id": "pdlid5aa6",
		"pointAttribute": null,
		"pointIndex": 9,
		"pointName": "HolidayStartTime",
		"pointType": 5,
		"productId": "productid135",
		"uid": "uid011",
		"updateTime": "2021-01-29 14:01:25",
		"value": "0"
	}, {
		"createTime": "2021-01-29 14:01:55",
		"delFlag": 0,
		"deviceId": "deviceidc99999",
		"id": "pdlidcbf8",
		"pointAttribute": null,
		"pointIndex": 7,
		"pointName": "NoFrostStatus",
		"pointType": 1,
		"productId": "productid135",
		"uid": "uid011",
		"updateTime": "2021-01-29 14:01:55",
		"value": "0"
	}],
```

## Zone Data

```

"pointDataList": [{
	"pointIndex": 11,
	"value": "0"
}, {
	"pointIndex": 3,
	"value": "12"
}, {
	"pointIndex": 4,
	"value": "0"
}, {
	"pointIndex": 13,
	"value": "1"
}, {
	"pointIndex": 10,
	"value": "1"
}, {
	"pointIndex": 14,
	"value": "205"
}, {
	"pointIndex": 8,
	"value": "0"
}, {
	"pointIndex": 7,
	"value": "0"
}, {
	"pointIndex": 5,
	"value": "192"
}, {
	"pointIndex": 9,
	"value": "0"
}, {
	"pointIndex": 6,
	"value": "200"
}],
```

### Point Type 

From observation there are 3 types of data used in the zone details point data. 

 * Temperature Data
 * Binary Flags (i.e. on / off)
 * Time Data (based on epoch)


| ID    | Data Type              |
| ----- | ---------------------- |
| 1     | Binary Toggle (on/off) |
| 4     | Epoch Timestamp        |
| 5     | Temperature Data       |

### Point Index

The point index is an integer that refers to the element is being controlled. The point index options are:

| Index  | Element           | Type  |
| ------ | ----------------- | ----- |
| 3      | TODO              | 0     |
| 4      | TODO              | 0     |
| 5      | Current Temp      | 4     |
| 6      | TODO              | 0     |
| 7      | TODO              | 0     |
| 8      | Boost On / Off    | 1     |
| 9      | Boost Off Time    | 4     |
| 10     | TODO              | 5     |
| 11     | TODO              | 0     |
| 13     | TODO              | 0     |
| 14     | Boost Target Temp | 4     |

### MQTT Binary Point Data

As previously mentioned the MQTT messages include a base64 binary encoded point data. The format of this tag, type, value in binary format. The format is:

1 Byte header, 1 Byte Index, 1 Byte Type, Between 1 and 4 Bytes Value.

The data in each type is:

 * Header - 00000000
 * Index  - The point index, e.g. 00001000 for Boost on / off.
 * Type   - The point type, e.g. 00000001 for binary toggle.
 * Value  - The point value, e.g. 00000001 for On in binary toggle type. 


In some cases the `pointData` value can include more that one type of data encoded in the same message.

Note: The header has always been observed as `0` and may be part of a 2 byte index, if it is possible to have a large index value.
