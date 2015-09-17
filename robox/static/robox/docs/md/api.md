### api/barcode/{barcode}/

>Gets all files and their parsed data with the given barcode.
>
>Type: get
>
>Responses
>
>>Success:
>>
>>>Media type: application/json
>>>
>>>Format:
>>>	 
>>>	    
>>>		{
>>>			"barcode": "barcode",
>>>			"files": [
>>>				{
>>>					"upload_time": "datetime",
>>>					"file_type": "string",
>>>					"file": "filename",
>>>					"data": [
>>>	             		{
>>>							"key": "value",
>>>						},
>>>					],
>>>				},
>>>	   		],
>>>		}
>>>
>>>Examples:
>>>
>>>		
>>>		{
>>>			"barcode": "2000001992852",
>>>	   		"files": [
>>>				{
>>>					"upload_time": "2015-09-11T13:55:28.475Z",
>>>					"file_type": "isc",
>>>					"file": "Caliper3_410370_ISC_1_5_2015-07-31_09-35-37_WellTable.csv"
>>>					"data": [
>>>	             		{
>>>							"value": "48.8164672349381",
>>>							"address": "A1",
>>>							"units": "nM",
>>>							"name": "concentration"
>>>						},
>>>						{
>>>							"value": "33.33333333333333",
>>>							"address": "A1",
>>>							"units": "%",
>>>							"name": "dilution"
>>>						},
>>>						{
>>>							"value": "54.134358195761",
>>>							"address": "B1",
>>>							"units": "nM",
>>>							"name": "concentration"
>>>						},
>>>						{
>>>							"value": "33.33333333333333",
>>>							"address": "B1",
>>>							"units": "%",
>>>							"name": "dilution"
>>>						}
>>>					],
>>>				}
>>>	    	],
>>>		}
>>>>
>>>
>>>		{
>>>			"barcode": "2000001992852",
>>>	    	"files": [],	    
>>>		}
>>
>>Error:
>>
>>>Status code: 422
>>>
>>>Media type: application/json
>>>
>>>Format:
>>>
>>>		{
>>>	    	"error": "message",
>>>	    	"barcode": "barcode",
>>>		}
>>>	
>>>Example:
>>>
>>>		{
>>>	    	"error": "Invalid barcode",
>>>	    	"barcode": "123456789",
>>>		}
>>>	 
       
### api/upload/
>Upload a set of files to a particular barcode and return their parsed data.
>
>Type: post
>
>Request
>
>>Arguments:
>>
>>>Parameters:
>>>
>>>>barcode: {string}
>>>
>>>File:
>>>>
>>>>Media type: multipart/form-data
>>>
>>>>Contents:
>>>>
>>>>>any_name: 
>>>>>>Media type: application/octet-stream
>>>>>
>>>>>any_name: 
>>>>>>Media type: application/octet-stream
>>>>>
>>>>>...
>
>Responses
>
>>Success:
>>
>>>Status code: 200
>>>
>>>Media type: application/json
>>>
>>>Format:
>>>
>>>		{
>>>			"barcode": "barcode",
>>>			"files": [
>>>				{
>>>					"file_type": "string",
>>>					"file": "filename",
>>>					"upload_time": "datetime",
>>>					"data": [
>>>						{
>>>							"key": "value"
>>>						},
>>>					],
>>>				},
>>>			],
>>>		}
>>>	
>>>Example:
>>>
>>>		{
>>>			"barcode": "2000001992852",
>>>			"files": [
>>>				{
>>>					"upload_time": "2015-09-09T12:14:05.350Z",
>>>					"file_type": "wgs",
>>>					"file": "Caliper3_410370_ISC_1_5_2015-07-31_09-35-37_WellTable.csv",
>>>					"data": [
>>>						{
>>>							"value": "48.8164672349381",
>>>							"address": "A1",
>>>							"units": "nM",
>>>							"name": "concentration"
>>>						},
>>>						{
>>>							"value": "33.33333333333333",
>>>							"address": "A1",
>>>							"units": "%",
>>>							"name": "dilution"
>>>						},
>>>						{
>>>							"value": "54.134358195761",
>>>							"address": "B1",
>>>							"units": "nM",
>>>							"name": "concentration"
>>>						},
>>>						{
>>>							"value": "33.33333333333333",
>>>							"address": "B1",
>>>							"units": "%",
>>>							"name": "dilution"
>>>						},
>>>					],
>>>				},
>>>			],
>>>		}
>>
>>Error:
>>
>>>Status code: 422
>>>
>>>Media type: application/json
>>>
>>>Format:
>>>
>>>		{
>>>	   		"error": "message",
>>>	   		"barcode": "barcode",
>>>		}
>>>	
>>>Example:
>>>
>>>		{
>>>	    	"error": "Invalid barcode",
>>>	    	"barcode": "123456789",
>>>		}
                    