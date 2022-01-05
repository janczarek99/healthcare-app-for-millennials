import React, { useState, useEffect } from "react";
import { Nav, Navbar } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import "./NavigationBar.css";

export function NavigationBar(isLoggedIn) {
  return (
    <div className="navbar">
      <Navbar bg="light" expand="lg" className="border border-dark">
        <LinkContainer to="/">
          <Navbar.Brand>Healthcare for millenials</Navbar.Brand>
        </LinkContainer>
        {isLoggedIn['isLoggedIn'] === "true" ? (
          <LinkContainer to="/logout">
            <Navbar.Brand>Logout</Navbar.Brand>
          </LinkContainer>
        ) : (
          <LinkContainer to="/login">
            <Navbar.Brand>Login</Navbar.Brand>
          </LinkContainer>
        )}

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
