import React from "react";
import { Nav, Navbar } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap"
import "./NavigationBar.css";

export function NavigationBar (){
    return (
        <div class="navbar">
            <Navbar bg="light" expand="lg" className="border border-dark">

                <LinkContainer to="/">
                    <Navbar.Brand>Healthcare for millenials</Navbar.Brand>
                </LinkContainer>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="mr-auto">
                        {/* <LinkContainer to="/about">
                            <Nav.Link>O projekcie</Nav.Link>
                        </LinkContainer> */}
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        </div>
    );
}