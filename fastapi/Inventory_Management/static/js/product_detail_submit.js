console.log("product detail on put/post");





var op;
document.getElementById('product_form').addEventListener('submit',async(e)=>{
    e.preventDefault();
    form=e.target;
    form.getElementsByTagName('button');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    //methodname,url,body
    // url=`/inventory/category/${id}` 405 error, i see what u tryna do.
    url=`/inventory/products/${id}`
    console.log("data is",data);
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