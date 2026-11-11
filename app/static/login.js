document.getElementById("loginForm").addEventListener("submit", async function(event)
{
    event.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const formData = new URLSearchParams();
        
    formData.append("username", username);
    formData.append("password", password);

    const response = await fetch(
        "/login",
        {
            method: "POST",
            headers: {
                "Content-Type":
                "application/x-www-form-urlencoded"
            },
            body: formData
        }
    );

    if(response.ok)
    {
        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        window.location.href = "/projects-page";
    }
    else
    {
        document.getElementById("error").innerText = "Invalid credentials";
    }
});