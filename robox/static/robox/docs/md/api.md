#### `api/files/?barcode={barcode}`

Gets all files and their parsed data with the given barcode.

**Type:** get
**Media type:** application/json
**Success Response Format:**
    {
    	"count": #,
    	"next": url,
    	"previous": url,
    	"results": [
    		{
    			"barcode": string,
    			"format": strign,
    			"upload_time": datetime,
    			"data": [
    				{
    					"key": string,
    				}
    			]
    		}
    	]
    }

**Success Response Example:**
    {
    	{
    		"count": 23,
    		"next": null,
    		"previous": "http://127.0.0.1:8000/api/files/?limit=10&offset=5",
    		"results": [
    			{
    				"barcode": "cgap123",
    				"format": "xTen",
    				"upload_time": "2015-09-25T11:55:31.595789Z",
    				"data": [
    					{
    						"units": "ng/ul",
    						"value": "12.317",
    						"address": "A1",
    						"name": "concentration"
    					},
    					{
    						"units": "ng/ul",
    						"value": "8.49",
    						"address": "B1",
    						"name": "concentration"
    					},
    					...
    				]
    			},
    			...
    		]
    	}
    }
       
#### `api/files/`

Upload a set of files to a particular barcode and return their parsed data.

**Type:** post
**Media type:** application/json
**Body Format:**
    {
        "barcode": string
    }
    
**Files:**
Any number of files to be uploaded with any name of type `application/octet-stream`

**Success Response Format:**
    {
        "results": [
            {
                "barcode": string,
                "format": string,
                "upload_time": datetime,
                "data": [
                    {
                        "key": string,
                    }
                ]
            }
        ]
    }
		
	
**Success Response Example:**
    {
        {
            "count": 23,
            "next": null,
            "previous": "http://127.0.0.1:8000/api/files/?limit=10&offset=5",
            "results": [
                {
                    "barcode": "cgap123",
                    "format": "xTen",
                    "upload_time": "2015-09-25T11:55:31.595789Z",
                    "data": [
                        {
                            "units": "ng/ul",
                            "value": "12.317",
                            "address": "A1",
                            "name": "concentration"
                        },
                        {
                            "units": "ng/ul",
                            "value": "8.49",
                            "address": "B1",
                            "name": "concentration"
                        },
                        ...
                    ]
                },
                ...
            ]
        }
    }

**Error Status code:** 422
**Error Response Format:**
    {
        "error": "message",
        "barcode": "barcode",
    }
	
**Error Response Example:**

    {
        "error": "Invalid barcode",
        "barcode": "123456789",
    }
                    