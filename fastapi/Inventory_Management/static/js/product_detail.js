console.log("product_detail conn");


supplier_select=document.getElementById('supplier_select');
category_select=document.getElementById('category_select');
supplier_body=document.getElementById('supplier_body');
category_body=document.getElementById('category_body')
flag=true;

async function fetchRecords(url,method_name='GET',payload) {
    try {
        // Helper to get cookie
        const token = document.cookie.split('; ')
            .find(row => row.startsWith('access_token='))
            ?.split('=')[1];

        methods=['GET','POST','DELETE','PUT','PATCH']


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





//I want to return a promise instead of TimeOut since
// it immediatly gets resolved.
let debounceTimer;
const callDebouncer=async (url)=>{
    // 1. Clear the previous timer immediately
    clearTimeout(debounceTimer);

    // 2. Start a new timer
    return new Promise((resolve,reject)=>{
        setTimeout(async () => {
        console.log("User stopped changing for 500ms. Fetching...");

        try {
            const data = await fetchRecords(url);
            console.log("Records received:", data);
            resolve(data.response);

        } catch (err) {
            console.error("Fetch failed:", err);
            reject(err);
        }

        }, 500);
    })
}


supplier_select.addEventListener("change",async ()=>{
    id=supplier_select.value;
    url=`/inventory/supplier/${id}`;
    console.log("url",url)
    try {
        data =await callDebouncer(url);
        updateTable(supplier_body, data)

    }
    catch (e){
        console.log(e)
    }
});

category_select.addEventListener("change",async ()=>{
    id=category_select.value;
    ans=supplier_select.value;//Used only one once.

    url=`/inventory/category/${id}`;
    try {
        data =await callDebouncer(url);
        console.log("data_k",data);
        op=data
        updateTableCategory(category_body, data.res)
        updateSupplierSelect(supplier_select,op.data[0])
        if(flag){ //Run only once during setup.
        supplier_select.value=ans;
        flag=false;
        }
        supplier_select.dispatchEvent(new Event('change'));


    }
    catch (e){
        console.log(e)
    }
});


function updateTableCategory(tbody,data){
    category_body.innerHTML="";
    const row=`
            <tr>
            <th>Name</th>
            <td>${data.category_name}</td>
            </tr>
            
            <tr>
            <th>Description</th>
            <td>${data.description}</td>
            </tr>
    `
    tbody.innerHTML=row;

}

function updateSupplierSelect(select_stmt,data){
    supplier_select.innerHTML="";

    const optionsHTML = data.map(supplier => {
    return `<option value="${supplier.supplier_id}">${supplier.supplier_name}</option>`;
}).join('');
    supplier_select.innerHTML=optionsHTML;



}

function updateTable(tbody,data){
    tbody.innerHTML="";

        const row = `
                <tr>
              <th>Company</th>
                    <td>${data.company_name}</td>
                </tr>
                <tr>
                    <th>Contact</th>
                    <td>${data.contact_name}</td>
                </tr>
                <tr>
                    <th>Phone</th>
                    <td>${data.phone || 'None'} </td>
                </tr>  
                <tr>
                    <th>Postal Code</th>
                    <td>${data.postal_code || 'None'} </td>
                </tr>  
                <tr>
                    <th>Title</th>
                    <td>${data.contact_title}</td>
                </tr>
                <tr>
                    <th>Country</th>
                    <td>${data.country}</td>
                </tr>
                <tr>
                    <th>City</th>
                    <td>${data.city}</td>
                </tr>
                <tr>
                    <th>Region</th>
                    <td>${data.region || 'None'} </td>
                </tr>  
                
        `;
        tbody.innerHTML=row;

}


document.addEventListener("DOMContentLoaded", () => {
    supplier_select.dispatchEvent(new Event('change'));
    category_select.dispatchEvent(new Event('change'));
});


