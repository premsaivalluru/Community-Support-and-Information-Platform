function show_page(pageClass)
{
    document.querySelectorAll(".page").forEach(el => el.classList.remove("active"));
    const target = document.querySelector("." + pageClass);
    if (target)
    {
        target.classList.add("active");
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const register_send_otp_button = document.querySelector(".register-send-otp-btn");
if (register_send_otp_button)
{
    document.querySelector(".register-send-otp-btn").addEventListener("click",async () => {
    const phone = document.querySelector(".send-otp input").value;
    const response = await fetch ( '/register_phone_verify/', 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({"phone": phone})
        }
    );

    const data = await response.json();
    if (data.success) {
        alert(data.message)
        document.querySelector(".register-send-otp-btn").disabled=true;
        document.querySelector(".verify-otp input").disabled=false;
        document.querySelector(".register-otp-btn").disabled=false;
    }
    else {
        alert(data.message);
    }
}
);
}

const register_otp_button = document.querySelector(".register-otp-btn");
if (register_otp_button)
{
    document.querySelector(".register-otp-btn").addEventListener("click", async () => {
    document.querySelector(".register-send-otp-btn").disabled=true;
    const phone = document.querySelector(".send-otp input").value;
    const otp = document.querySelector(".verify-otp input").value;
    console.log(phone, otp)
    const response = await fetch ( '/register_phone_verify_otp/', 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({"phone": phone, "otp": otp})
        }
    );
    const data = await response.json();
    if (data.success)
    {
        alert(data.message)
    }
    else{
        alert(data.message)
        document.querySelector(".register-send-otp-btn").disabled=false;
    }
}
);
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".get-started-form");
    const btn  = document.querySelector(".get-started-button");

    if (form && btn)
    {
        function checkForm() {
        const inputs = form.querySelectorAll("input[type=text], input[type=password]");
        const agree = form.querySelector("input[name=agree]");
        const pass1 = form.querySelector("input[name=password1]");
        const pass2 = form.querySelector("input[name=password2]");
        btn.disabled = true;

        for (let input of inputs) {
            if (!input.value.trim() && !input.disabled) {
                return;
            }
        }

        if (!agree.checked) {
            return;
        }
        const fileInput = form.querySelector("input[type=file]");
        console.log(fileInput)
        if (!fileInput.files.length) {
            err = document.querySelector(".error-file")
            err.style.color = "red";
            err.textContent = "Please upload a profile photo!";
            return;
        }

        if (pass1.value !== pass2.value) {
            err = document.querySelector(".error-passwords")
            err.style.color = "red";
            err.textContent = "Passwords do not match!";
            return;
        }
        
        btn.disabled = false;
    }

    checkForm();
    form.addEventListener("input", checkForm);
    form.addEventListener("change", checkForm);
    }
});


document.addEventListener("DOMContentLoaded", () => {
    const header = document.querySelector(".home-page-header");
    const scrollBtn = document.querySelector(".get-started-btn");

    if (scrollBtn && header) {
        scrollBtn.addEventListener("click", () => {
            console.log("Header Found. Scrolling...");
            window.scrollTo({top: 0, behavior: 'smooth'});
        });
    }
});

const forgot_send_otp_btn = document.querySelector(".forgot-send-otp-btn");
if (forgot_send_otp_btn)
{
    forgot_send_otp_btn.addEventListener("click", async () => {
        const phone = document.querySelector(".forgot-form .phone-number input").value;
        const response = await fetch('/login_phone_verify/',
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({phone: phone})
            }
        );
    const data = await response.json();
    if (data.success)
    {
        alert(data.message);
        show_page('otp-verify');
    }
    else{
        alert(data.message);
    }
    });
}

const forgot_verify_otp_btn = document.querySelector(".forgot-verify-otp-btn");
if (forgot_verify_otp_btn)
{
    forgot_verify_otp_btn.addEventListener("click", async () => {
        const otp = document.querySelector(".verify-form .otp input").value;
        const response = await fetch('/login_phone_verify_otp/',
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({otp: otp})
            }
        );
        const data = await response.json();
        if (data.success)
        {
            alert(data.message);
            show_page('reset-password');
        }
        else
        {
            alert(data.message);
        }
    });
}

const menu_btn = document.querySelector(".menu-icon");
const menu_list = document.querySelector(".mobile-nav-links");
isButtonClicked = false;
if (menu_btn)
{
    menu_btn.addEventListener("click", () => {
        if (!isButtonClicked)
        {
            menu_list.style.display = "flex";
            isButtonClicked = false;
        }
    });
}

back_btn = document.querySelector(".fa-arrow-left")
if (back_btn)
{
    back_btn.addEventListener("click", () => {
        menu_list.style.display = "none";
    });
}

const loadMoreBtn = document.querySelector(".load-more-btn");
const posts = document.querySelectorAll('.posts-container');
const initialVisible = 9;

if (loadMoreBtn) {
    posts.forEach((post, index) => {
        if (index >= initialVisible) post.classList.add('hidden');
    });

    loadMoreBtn.addEventListener("click", () => {
        if (loadMoreBtn.textContent === "Load More") {
            posts.forEach(post => post.classList.remove('hidden'));
            loadMoreBtn.textContent = "See Less";
        } else {
            posts.forEach((post, index) => {
                if (index >= initialVisible) post.classList.add('hidden');
            });
            loadMoreBtn.textContent = "Load More";
        }
    });
}
const photo = document.querySelector(".user-photo")
if (photo)
{
    photo.addEventListener("change", function(event) {
        const file = event.target.files[0];
        const validExtensions = ['jpg', 'jpeg'];
        const fileExtension = file.name.split('.').pop().toLowerCase();
        if (!validExtensions.includes(fileExtension))
        {
            alert("Only .jpg files are allowed!!!");
            photo.value="";
            return;
        }
        photo.style.pointerEvents = "none";
        photo.style.opacity = "0.5";
    });
}