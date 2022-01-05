import { NavigationBar } from "../NavigationBar";
import { Navigate} from "react-router-dom";
import React, {useState} from 'react';

export function DiagnosisView() {
    const token = localStorage.getItem('token');
    const [isLoggedIn, setIsLoggedIn] = useState(localStorage.getItem('isLoggedIn'));

    if (isLoggedIn === "false"){
        return <Navigate to="/login"/>;
    } 
    return (
        <>
            <NavigationBar isLoggedIn={isLoggedIn}/>
            diagnosis
        </>
      );
}