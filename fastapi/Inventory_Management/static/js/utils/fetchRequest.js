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

        if (payload && method_name !== 'GET') {
        requestOptions.body = JSON.stringify(payload);
         }

        const response = await fetch(url,requestOptions
        );

        if (response.ok) {
            const data = await response.json();
            console.log("Data received:", data);
            return {"message":"success","status":response.status,"response":data}
        }
        else{
          const errorText = await response.text();
          throw new Error(`HTTP Error ${response.status}: ${errorText || response.statusText}`);
        }
    } catch (error) {
        console.error("Network error:", error);
        return {"message":"failure","status":response.status,"response":response.status}
    }
}

export {
    fetchRecords
}