import React, { useState } from "react";
import { Navigate } from "react-router-dom";
import { NavigationBar } from "../NavigationBar";
import "./LoginView.css";
import Snackbar from '@mui/material/Snackbar';
import Slide from '@mui/material/Slide';
import Alert from '@mui/material/Alert';

function TransitionUp(props) {
    return <Slide {...props} direction="up" />;
  }

export function LoginView(props) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [redirect, setRedirect] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(
    localStorage.getItem("isLoggedIn")
  );
  const [transition, setTransition] = useState(() => TransitionUp);
  const [showError, setShowError] = useState(false);
  const [error, setError] = useState("");
  const openError = () => {
    setShowError(true);
    setTimeout(() => setShowError(false),2000)
  }

  const submit = async (e) => {
    e.preventDefault();
 
    const response = await fetch("https://healthcare-for-millennials-api.westeurope.azurecontainer.io/authenticate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        username,
        password,
      }),
    });

    const content = await response.json();
    if (content.detail){
        console.log("FAILURE");
        openError();
        switch (content.detail.status) {
            case "Not found.":
                setError("User not found!");
                break;
            case "Forbidden.":
                setError("Wrong password!");
                break;
            default:
                setError("Something went wrong, try again!")
        }
    } else {
        setRedirect(true);
        localStorage.setItem("token", content.accessToken);
        localStorage.setItem("isLoggedIn", true);
    }
  };

  if (redirect === true) {
    return (
      <Navigate
        to={{
          pathname: "/",
        }}
      />
    );
  }

  return (
    <>
      <NavigationBar isLoggedIn={isLoggedIn} />
      <div className="login-box">
        <form onSubmit={submit}>
          <h1 className="h3 mb-3 fw-normal">Please sign in</h1>
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
            Sign in
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
    </>
  );
}
