console.log("product_detail conn");
import {fetchRecords} from "./utils/fetchRequest.js";

const supplier_select=document.getElementById('supplier_select');
const category_select=document.getElementById('category_select');
const supplier_body=document.getElementById('supplier_body');
const category_body=document.getElementById('category_body')
let flag=true;







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
    let id=supplier_select.value;
    let url=`/inventory/supplier/${id}`;
    console.log("url",url)
    try {
        const data =await callDebouncer(url);
        updateTable(supplier_body, data)

    }
    catch (e){
        console.log(e)
    }
});

category_select.addEventListener("change",async ()=>{
    let id=category_select.value;
    let ans=supplier_select.value;//Used only one once.

    let url=`/inventory/category/${id}`;
    try {
        let data =await callDebouncer(url);
        console.log("data_k",data);
        let op=data
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


