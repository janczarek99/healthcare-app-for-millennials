import {Container, Row, CardGroup} from "react-bootstrap";
import {CustomCard} from "../CustomCard";
import { NavigationBar } from "../NavigationBar";
import { Navigate} from "react-router-dom";
import React, {useState} from 'react';

export function HealthcareMainView() {
    const token = localStorage.getItem('token');
    const [isLoggedIn, setIsLoggedIn] = useState(localStorage.getItem('isLoggedIn'));

    if (isLoggedIn === "false"){
        return <Navigate to="/login"/>;
    } 

    return (
        <>
            <NavigationBar isLoggedIn={isLoggedIn}/>
            <Container >
                <Row className="justify-content-md-center">
                    <CardGroup>
                        <CustomCard title='Documents' to='/documents' width='25rem' src='/images/handwrites.jpg'/>
                        <CustomCard title='Medical diagnosis' to='/diagnosis' width='25rem' src='/images/xray.jpg'/>
                    </CardGroup>
                </Row>
            </Container>
        </>
      );
}