console.log("product js connected");

// State Management
let currentPage = document.getElementById("page_num_id");
let total_pages=Math.floor(document.getElementById("total_pages").textContent);
let page_size= document.getElementById("page_size").textContent;
//1,2,3 the leftmost is the current_page
//2,3,4
const wrapper = document.getElementById('paginationWrapper');
const template = document.getElementById('pageTemplate');


function setupPagination(totalPages) {
    for(let i=totalPages;i>=2;i--){
        //true means clone children like button
        let parentNode=template.cloneNode(true);
        let childNode=parentNode.firstElementChild;
        childNode.removeAttribute("id");
        childNode.removeAttribute("href")
        childNode.setAttribute("id","li_"+i);
        childNode.textContent=i+"";
        childNode.setAttribute("data-page",`${i}`);
        template.insertAdjacentElement("afterend", parentNode);
    }
}

setupPagination(total_pages)

wrapper.addEventListener('click', async (e) => {
    // Check if the clicked element is a .page-link
    console.log(e)
    if (e.target.classList.contains('page-link')) {
        e.preventDefault();
        e.stopPropagation()
        const page = e.target.getAttribute('data-page');
        if (!page) return; // Ignore if it's the Prev/Next buttons (unless they have data-page)

        console.log(`Fetching data for page: ${page}`);
        await fetchProducts(page,page_size);
    }
});


async function fetchProducts(page,page_size) {
    try {
        // Helper to get cookie
        const token = document.cookie.split('; ')
            .find(row => row.startsWith('access_token='))
            ?.split('=')[1];

        const response = await fetch(`/inventory/products?page=${page}&size=${page_size}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Data received:", data);

            currentPage=page;
            updateTable(data,page,page_size);

        } else {
            console.error("Fetch failed", response.status);
        }
    } catch (error) {
        console.error("Network error:", error);
    }
}


function updateTable(products,page,page_size) {
    const tbody = document.getElementById('productTableBody');
    console.log("tbody",tbody);
    // 1. Clear existing rows
    tbody.innerHTML = "";

    count=page_size*(page-1);//10*20 for page 3
    // 2. Build new rows
    let counter=1
    counter+=count//20+1
    products.data.forEach(item => {
        const row = `
            <tr class="table-active">   
                <td>${counter}</td>  
               
                <td><a href="id/${item.product_id}/html">${item.product_name}</a></td>
                <td>${item.units_in_stock}</td>
                <td>${item.unit_price}</td>
                <td>${item.unit_on_order}</td>
                <td><a href="/supplier/${item.supplier_id}">${item.supplier_name}</a></td>
                <td><a href="/category/${item.category_id}">${item.category_name}</a></td>
<!--                <td>-->
<!--                <button onclick="window.location.href='/products/{{ user.id }}'" type="button"-->
<!--                class="btn btn-info">-->
<!--                Edit-->
<!--                </button>-->

            </tr>
        `;
        counter+=1;
        // 3. Insert into the table
        tbody.insertAdjacentHTML('beforeend', row);
    });
}