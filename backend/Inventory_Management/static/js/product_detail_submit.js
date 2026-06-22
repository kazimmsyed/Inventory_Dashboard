console.log("product detail on put/post");
import {fetchRecords} from "./utils/fetchRequest.js";
import {showToast} from "./utils/bs_toast.js";


document.getElementById('product_form').addEventListener('submit',async(e)=>{
    e.preventDefault();
    let form=e.target;
    // form.getElementsByTagName('button');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    data.reorder_level=parseInt(data.reorder_level);
    data.unit_on_order=parseInt(data.unit_on_order);
    let id=form.dataset.id;
    //methodname,url,body
    // url=`/inventory/category/${id}` 405 error, i see what u tryna do.
    let url=`/inventory/products/${id}`
    // console.log("data is",data);
    const result= await fetchRecords(url,'PUT',data);
    // console.log("res",result.message);
    if(result.message=="success"){
        console.log(result)
        showToast(`${result.response.product_name} updated successfully`, "success",e.target);
    }
    else{
        showToast("Error", "danger",e.target);
        console.log(result.status)
    }


})