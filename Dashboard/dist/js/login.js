const auth = firebase.auth();

auth.onAuthStateChanged(user => {
    if (user) {
      window.location.replace("index.html");
    } else {
        console.log('user logged out: ', user);
    }
  })

const loginForm = document.querySelector('#login-form');
loginForm.addEventListener('submit', (e) =>{
    e.preventDefault();

    //get user account
    const email = loginForm['email'].value;
    const password = loginForm['password'].value;

    auth.signInWithEmailAndPassword(email,password).then(cred => {
        loginForm.reset();
    })
    
})
 
