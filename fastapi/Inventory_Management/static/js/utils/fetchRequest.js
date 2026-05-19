async function fetchRecords(url,method_name='GET',payload) {
    try {
        // Helper to get cookie
        const token = document.cookie.split('; ')
            .find(row => row.startsWith('access_token='))
            ?.split('=')[1];

        let methods=['GET','POST','DELETE','PUT','PATCH']


        let requestOptions = {
        method: method_name,
        headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
        }
        };

    //Use the literal string 'body' as the key
        if (payload && method_name !== 'GET') {
        requestOptions.body = JSON.stringify(payload);
         }

        const response = await fetch(url,requestOptions
        );

        if (response.ok) {
            const data = await response.json();
            console.log("Data received:", data);
            return {"message":"success","response":data}
            //Add your code here
            //updateTable();

        } else {
            console.error("Fetch failed", response.status);
        // throw new Error(`HTTP Error: ${response.status} - ${response.statusText}`);
            return {"message":"failure","response":response.status}

        }
    } catch (error) {
        console.error("Network error:", error);
        return {"message":"failure","response":response.status}
    }
}

export {
    fetchRecords
}