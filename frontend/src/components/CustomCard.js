import React from "react";
import { Card } from "react-bootstrap";
import {LinkContainer} from "react-router-bootstrap";

export class CustomCard extends React.Component {

    render() {
        return (
            <LinkContainer to={this.props.to}>
                <a style={{ cursor: 'pointer' }}>
                    <Card style={{ width: this.props.width }}>
                        <Card.Img variant="top" src={this.props.src} />
                        <Card.Body>
                            <Card.Title><h5>{this.props.title}</h5></Card.Title>
                        </Card.Body>
                    </Card>
                </a>
            </LinkContainer>
        );
    }
}