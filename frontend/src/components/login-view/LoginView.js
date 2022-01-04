import React, {useState} from 'react';
import { Navigate } from "react-router-dom";
import { NavigationBar } from "../NavigationBar";

export function LoginView(props) {
    const [name, setName] = useState(props.name);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [redirect, setRedirect] = useState(false);

    const submit = async (e) => {
        e.preventDefault();

        const response = await fetch('http://localhost:9999/authenticate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            credentials: 'include',
            body: JSON.stringify({
                username,
                password
            })
        });

        const content = await response.json();
        setRedirect(true);
        localStorage.setItem('token', content.accessToken)
        props.setName(content.accesToken);
    }

    if (redirect) {
        return <Navigate  
            to={{
                pathname: '/' 
            }}
        />   
    }

    return (
        <>
            <NavigationBar></NavigationBar>
            <form onSubmit={submit}>
                <h1 className="h3 mb-3 fw-normal">Please sign in</h1>
                <input type="username" className="form-control" placeholder="Username" required
                    onChange={e => setUsername(e.target.value)}
                />

                <input type="password" className="form-control" placeholder="Password" required
                    onChange={e => setPassword(e.target.value)}
                />

                <button className="w-100 btn btn-lg btn-primary" type="submit">Sign in</button>
            </form>
        </>
        
    );
}