document.getElementById("registerForm").addEventListener("submit", async function(event)
{
    event.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const response = await fetch(
        "/auth",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password })
        }
    );

    if(response.ok)
    {
        window.location.href = "/";
    }
    else
    {
        document.getElementById("error").innerText = "Registration failed. Please try again.";
    }
});