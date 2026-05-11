console.log("product_detail conn");

supplier_select=document.getElementById('supplier_select');
category_select=document.getElementById('category_select');
supplier_body=document.getElementById('supplier_body');
category_body=document.getElementById('category_body')


async function fetchRecords(url) {
    try {
        // Helper to get cookie
        const token = document.cookie.split('; ')
            .find(row => row.startsWith('access_token='))
            ?.split('=')[1];

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Data received:", data);
            return data
            //Add your code here
            //updateTable();

        } else {
            console.error("Fetch failed", response.status);
        }
    } catch (error) {
        console.error("Network error:", error);
    }
}




const timeOut=async ()=>{
    let res=setTimeout(()=> "wait for 500ms",500);
    return res
}


// let debounceTimer
// supplier_select.addEventListener("change", () => {
//     // 1. Clear the previous timer immediately
//     clearTimeout(debounceTimer);
//
//     // 2. Start a new timer
//     debounceTimer = setTimeout(async () => {
//         console.log("User stopped changing for 500ms. Fetching...");
//         id=document.getElementById('supplier_select').value;
//         try {
//             const data = await fetchRecords(url=`/inventory/supplier/${id}`);
//             console.log("Records received:", data);
//             op=data;
//             updateTable(supplier_body,data)
//
//         } catch (err) {
//             console.error("Fetch failed:", err);
//         }
//
//     }, 500); // The delay
// });




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
            resolve(data);

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
    url=`/inventory/category/${id}`;
    try {
        data =await callDebouncer(url);
        console.log("data_k",data);
        updateTableCategory(category_body, data)
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


