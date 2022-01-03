import {Container, Row, CardGroup} from "react-bootstrap";
import {CustomCard} from "../CustomCard";
import { NavigationBar } from "../NavigationBar";

export function HeatlhcareMainView() {
    return (
        <>
            <NavigationBar></NavigationBar>
            <Container >
                <Row className="justify-content-md-center">
                    <CardGroup>
                        <CustomCard title='Electronic documents' to='/documents' width='25rem' src='/images/edocuments.jpg'/>
                        <CustomCard title='Handwrites' to='/handwrites' width='25rem' src='/images/handwrites.jpg'/>
                        <CustomCard title='Medical diagnosis' to='/diagnosis' width='25rem' src='/images/xray.jpg'/>
                    </CardGroup>
                </Row>
            </Container>
        </>
      );
}