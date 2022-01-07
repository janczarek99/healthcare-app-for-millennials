import React, { useState } from "react";
import { Navigate } from "react-router-dom";
import { NavigationBar } from "../NavigationBar";
import "./RegisterView.css";
import Snackbar from '@mui/material/Snackbar';
import Slide from '@mui/material/Slide';
import Alert from '@mui/material/Alert';

function TransitionUp(props) {
    return <Slide {...props} direction="up" />;
  }

export function RegisterView(props) {
  const [isLoggedIn, setIsLoggedIn] = useState(localStorage.getItem('isLoggedIn'));
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [transition, setTransition] = useState(() => TransitionUp);
  const [showError, setShowError] = useState(false);
  const [error, setError] = useState("");
  const [showSuccess, setShowSuccess] = useState(false);

  const openError = () => {
    setShowError(true);
    setTimeout(() => setShowError(false),2000)
  }

  const openSuccess = () => {
    setShowSuccess(true);
    setTimeout(() => setShowSuccess(false),2000)
  }

  const submit = async (e) => {
    e.preventDefault();
 
    const response = await fetch("http://localhost:9999/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username,
        password,
      }),
    });

    const content = await response.json();
    if (content.detail){
        console.log("FAILURE");
        console.log(content.detail);
        openError();
        switch (content.detail.title) {
            case "Cannot create user":
                setError("Cannot create user.");
                break;
            default:
                setError("Something went wrong, try again!");
        }
    } else {
        openSuccess();
    }
  };

  return (
    <>
      <NavigationBar isLoggedIn={isLoggedIn} />
      <div className="register-box">
        <form onSubmit={submit}>
          <h1 className="h3 mb-3 fw-normal">Create Account</h1>
          <input
            type="username"
            className="form-control"
            placeholder="Username"
            required
            minlength="6"
            onChange={(e) => setUsername(e.target.value)}
          />

          <input
            type="password"
            className="form-control"
            placeholder="Password"
            required
            minlength="10"
            onChange={(e) => setPassword(e.target.value)}
          />

          <button className="w-100 btn btn-lg btn-primary" type="submit">
            Register
          </button>
        </form>
      </div>
      <Snackbar
        open={showError}
        TransitionComponent={transition}
        key="1"
      >
        <Alert severity="error" variant="filled" sx={{ width: "100%" }}>
          {error}
        </Alert>
      </Snackbar>
      <Snackbar
        open={showSuccess}
        TransitionComponent={transition}
        key="2"
      >
        <Alert severity="success" variant="filled" sx={{ width: "100%" }}>
          Account created successfully!
        </Alert>
      </Snackbar>
    </>
  );
}
