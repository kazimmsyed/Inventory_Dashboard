let debounceTimer;

const usernameInput = document.getElementById('validationServerUsername');
const serverfeedback = document.getElementById("validationServerUsernameFeedback");

usernameInput.addEventListener('input', () => {
    clearTimeout(debounceTimer);

    debounceTimer = setTimeout(async () => {
        const username = usernameInput.value;

        // Using your logic: 4 characters or more to trigger check
        if (username.length <= 3) {
            usernameInput.classList.remove('is-invalid', 'is-valid');
            return;
        }

        try {
            const response = await fetch(`/auth/user/${username}`);
            const data = await response.json();

            if (data["available"]) {
                usernameInput.classList.remove('is-invalid');
                usernameInput.classList.add('is-valid');

                serverfeedback.textContent = 'Username is available!';
                serverfeedback.className = 'valid-feedback';
            } else {
                usernameInput.classList.remove('is-valid');
                usernameInput.classList.add('is-invalid');

                serverfeedback.textContent = 'Username is taken';
                serverfeedback.className = 'invalid-feedback';
            }
        } catch (error) {
            console.error("Network error:", error);
        }
    }, 500);
});


// pwd_1=document.getElementById('password_not_matched1')
// pwd_2=document.getElementById('password_not_matched2')
// exampleInputPassword1=document.getElementById('exampleInputPassword1')
// exampleInputPassword2=document.getElementById('exampleInputPassword2')
//
// exampleInputPassword2.addEventListener('change',async ()=>{
//     if(exampleInputPassword1.value!==exampleInputPassword2.value){
//         pwd_2.classList.add('is-invalid');
//         pwd_2.classList.remove('is-valid');
//     }
//    else{
//        pwd_2.classList.remove('is-invalid');
//        pwd_2.classList.add('is-valid');
//     }
//
// })

// register_validation.js
const pass1 = document.getElementById('exampleInputPassword1');
const pass2 = document.getElementById('exampleInputPassword2');
const feedback2 = document.getElementById('password_not_matched2');

const checkPasswords = () => {
    // Only validate if both fields have something in them
    if (pass1.value.length > 0 && pass2.value.length > 0) {
        if (pass1.value !== pass2.value) {
            // Apply Bootstrap error state
            pass2.classList.add('is-invalid');
            pass2.classList.remove('is-valid');
            feedback2.textContent = "Passwords do not match.";
            feedback2.className='invalid-feedback'; //Instead of toggling between the two, just assign.

        } else {
            // Apply Bootstrap success state
            pass2.classList.remove('is-invalid');
            pass2.classList.add('is-valid');
            feedback2.className='valid-feedback';


            feedback2.textContent = "Passwords matched";
        }
    } else {
        // Reset if fields are cleared
        pass2.classList.remove('is-invalid', 'is-valid');
    }
};

// Listen for typing on both fields
pass1.addEventListener('input', checkPasswords);
pass2.addEventListener('input', checkPasswords);