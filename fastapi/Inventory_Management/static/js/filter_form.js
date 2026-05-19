console.log("filter form connected");

filter_form=document.getElementById('filter_form');


const filter_func=  (e)=>{
    const filters = [];

    // Assuming you use a common class for filter rows
    const filterRows = e.target.querySelectorAll('.filter-row');

    filterRows.forEach(row => {
        const field = row.querySelector('[name="field"]').value;
        const operator = row.querySelector('[name="operator"]').value;
        const value = row.querySelector('[name="value"]').value;

        // Only add if the user actually filled it out
        if (field && operator && value) {
            filters.push({ field, operator, value });
        }
    });

    return { filters };
}

filter_form.addEventListener('submit',async(e)=>{
   e.preventDefault();
   payload=filter_func(e);


});
