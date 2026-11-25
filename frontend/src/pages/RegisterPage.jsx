import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

export default function RegisterPage() {

    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    async function handleRegister(event) 
    {
        event.preventDefault();

        setError("");
        setSuccess("");

        const response = await fetch("/api/auth",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify({
                    username,
                    password
                })
            }
        );

        if (response.ok) 
        {
            setSuccess("Registration successful");
            setTimeout(() => navigate("/"), 1000);
        }
        else 
        {
            const data = await response.json();
            setError(data.detail ?? "Registration failed");
        }
    }

    return (
        <div className="container">
            <div className="row justify-content-center mt-5">
                <div className="col-md-4">
                    <div className="card shadow">
                        <div className="card-header">
                            <h3>Create Account</h3>
                        </div>
                        <div className="card-body">
                            <form onSubmit={handleRegister}>
                                <div className="mb-3">
                                    <label className="form-label">Username</label>
                                    <input className="form-control"
                                           value={username}
                                           onChange={(e) => setUsername(e.target.value)}
                                           required/>
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Password</label>
                                    <input type="password"
                                           className="form-control"
                                           value={password}
                                           onChange={(e) => setPassword(e.target.value)}
                                           required/>
                                </div>
                                <button className="btn btn-success w-100">
                                    Register
                                </button>
                            </form>
                            {error && (
                                <div className="alert alert-danger mt-3">{error}</div>
                            )}
                            {success && (
                                <div className="alert alert-success mt-3">{success}</div>
                            )}
                            <div className="mt-3 text-center">
                                <Link to="/">Back to login</Link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}