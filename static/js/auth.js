document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const pwd = form.querySelector('#password');
            const pwdConfirm = form.querySelector('#password_confirm');

            if (pwd) {
                if (pwd.value.length < 6) {
                    e.preventDefault();
                    alert('Password must be at least 6 characters long');
                    return;
                }

                if (pwdConfirm && pwd.value !== pwdConfirm.value) {
                    e.preventDefault();
                    alert('Passwords do not match');
                    return;
                }
            }
        });
    });
});
