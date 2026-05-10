const loginForm = document.getElementById('loginform');

if (loginForm) {
    loginForm.addEventListener('submit',async function (event) {
        event.preventDefault();

        // 1. Grab all data from the form
        const formData = new FormData(event.target);
            const payload = new URLSearchParams(formData);


        // 2. Convert it to "username=value&password=value" format
        //const payload = new URLSearchParams(formData);
        //         const payload2={
        //         username:event.target.elements.username.value,
        //         password:event.target.elements.password.value
        //         }
        //         console.log(payload2);

        console.log(payload.toString());

        try {
            const response = await fetch('/auth/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: payload
            });

            if (response.ok) {
                const data = await response.json();

                // Clear old session cookies
                if (typeof logout === "function") logout();

                // Save the new JWT access token
                document.cookie = `access_token=${data.access_token}; path=/; SameSite=Lax`;

                // Successful redirect to your product dashboard
                window.location.href = 'http://127.0.0.1:8000/inventory/products/html';
            } else {
                const errorData = await response.json();
                // FastAPI returns the error message in the 'detail' field
                alert(`Login Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error('Network Error:', error);
            alert('Could not connect to the server.');
        }
    });
}


function logout() {
        // Get all cookies
        const cookies = document.cookie.split(";");

        // Iterate through all cookies and delete each one
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i];
            const eqPos = cookie.indexOf("=");
            const name = eqPos > -1 ? cookie.substring(0, eqPos) : cookie;
            // Set the cookie's expiry date to a past date to delete it
            document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
        }

        // Redirect to the login page
        window.location.href = '/auth/login-page';
    };
