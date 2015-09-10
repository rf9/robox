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
>>>	       	{
>>>	           	"upload_time": "datetime",
>>>	           	"data": [
>>>	             		{
>>>	                 	"key": "value",
>>>	               	}
>>>					],
>>>	           	"file_type": "string",
>>>	           	"file": "urlpath",
>>>	       	}
>>>	   		],
>>>		}
>>>
>>>Examples:
>>>
>>>		
>>>		{
>>>			"barcode": "ABC001",
>>>	   		"files": [
>>>	       	{
>>>	          	"upload_time": "2015-09-09T12:14:05.350Z",
>>>	            	"data": [
>>>	             		{
>>>	                 	"value": "48.8164672349381",
>>>	                    "address": "A1",
>>>	                    "units": "nM",
>>>	                    "name": "concentration"
>>>	                },
>>>	                {
>>>	                    "value": "33.33333333333333",
>>>	                    "address": "A1",
>>>	                    "units": "%",
>>>	                    "name": "dilution"
>>>	                },
>>>	                {
>>>	                    "value": "54.134358195761",
>>>	                    "address": "B1",
>>>	                    "units": "nM",
>>>	                    "name": "concentration"
>>>	                },
>>>	                {
>>>	                    "value": "33.33333333333333",
>>>	                    "address": "B1",
>>>	                    "units": "%",
>>>	                    "name": "dilution"
>>>	                }
>>>	            ],
>>>	            "file_type": "wgs",
>>>	            "file": "/media/data/Caliper1_411709_PATH_1_3_2015-08-18_01-24-55_WellTable_neqrdbc.csv"
>>>	        }
>>>	    	],
>>>		}
>>>>
>>>
>>>		{
>>>			"barcode": "ABC002",
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
>>>	    	"barcode": "barcode"
>>>		}
>>>	
>>>Example:
>>>
>>>		{
>>>	    	"error": "Invalid barcode",
>>>	    	"barcode": "123456789"
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
>>>	    	"files": [
>>>	       	{
>>>	          	"upload_time": "datetime",
>>>	            	"data": [
>>>	             		{
>>>	                 	"key": "value"
>>>	                	}
>>>	          	],
>>>	            	"file_type": "string",
>>>	            	"file": "urlpath"
>>>	        	}
>>>	    	],
>>>	    	"barcode": "barcode"
>>>		}
>>>	
>>>Example:
>>>
>>>		{
>>>	   		"files": [
>>>	       	{
>>>	          	"upload_time": "2015-09-09T12:14:05.350Z",
>>>	            	"data": [
>>>	             		{
>>>	                 	"value": "48.8164672349381",
>>>	                    "address": "A1",
>>>	                    "units": "nM",
>>>	                    "name": "concentration"
>>>	                },
>>>	                {
>>>	                    "value": "33.33333333333333",
>>>	                    "address": "A1",
>>>	                    "units": "%",
>>>	                    "name": "dilution"
>>>	                },
>>>	                {
>>>	                    "value": "54.134358195761",
>>>	                    "address": "B1",
>>>	                    "units": "nM",
>>>	                    "name": "concentration"
>>>	                },
>>>	                {
>>>	                    "value": "33.33333333333333",
>>>	                    "address": "B1",
>>>	                    "units": "%",
>>>	                    "name": "dilution"
>>>	                }
>>>	            ],
>>>	            "file_type": "wgs",
>>>	            "file": "/media/data/Caliper1_411709_PATH_1_3_2015-08-18_01-24-55_WellTable_neqrdbc.csv"
>>>	       	}
>>>	    	],
>>>	    	"barcode": "ABC001"
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
>>>	   		"barcode": "barcode"
>>>		}
>>>	
>>>Example:
>>>
>>>		{
>>>	    	"error": "Invalid barcode",
>>>	    	"barcode": "123456789"
>>>		}
                    