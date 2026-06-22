
const feedback1 = document.getElementById('password_not_matched2');
const usernameInput1 = document.getElementById('validationServerUsername');
const registerForm = document.getElementById('register_form');


if (registerForm) {
        registerForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            if(feedback1.classList.contains('is-invalid') || usernameInput1.classList.contains('is-invalid')){
                alert("fields invalid");
                return;
            }

            const btn = event.target.querySelector('button[type="submit"]');
            btn.disabled = true; // Prevent double clicks
            btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Loading...';

            const form = event.target;
            // const formData = new FormData(form);
            // alert(formData.entries());
            // const data = Object.fromEntries(formData);
            //



            const payload = {
                email: registerForm.elements.exampleInputEmail1.value,
                username: registerForm.elements.validationServerUsername.value,
                first_name: registerForm.elements.first_name.value,
                last_name: registerForm.elements.last_name.value,
                role: "true",
                hashed_password: registerForm.elements.exampleInputPassword2.value
            };


            try {
                const response = await fetch('/auth/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    window.location.href = '/auth/login';
                } else {
                    // Handle error
                    const errorData = await response.json();
                    alert(`Error: ${errorData.message}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }


