import { NavigationBar } from "../NavigationBar";
import { Navigate } from "react-router-dom";
import React, { useState, useEffect } from 'react';
import { Button } from "@mui/material";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box"
import Grid from "@mui/material/Grid"
import CustomList from "../CustomList";
import Container from '@mui/material/Container';
import Alert from '@mui/material/Alert';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';

import Snackbar from '@mui/material/Snackbar';
import Slide from '@mui/material/Slide';
import PopUp from "../PopUp";

function TransitionUp(props) {
  return <Slide {...props} direction="up" />;
}

export function DocumentsView() {
  const token = localStorage.getItem('token');
  const [isLoggedIn, setIsLoggedIn] = useState(localStorage.getItem('isLoggedIn'));
  const [uploadedFile, setUploadedFile] = useState(null);
  const [documentName, setDocumentName] = useState('')
  const [isFetching, setIsFetching] = useState(false);
  const [userDocuments, setUserDocuments] = useState(null);
  const uploadBoxWidth = 450;

  const [isProcessing, setIsProcessing] = React.useState(false);
  const [hasUploaded, setHasUploaded] = React.useState(false)
  const [transition, setTransition] = React.useState(() => TransitionUp);

  const [isPopUpOpen, setIsPopUpOpen] = useState(false);
  const [selectedDocument, setSelectedDocument] = useState(null);

  const handleClose = () => {
    setIsProcessing(false);
    setHasUploaded(false)
  };

  const handleOpenDocument = (document) =>{
    setSelectedDocument(document);
    setIsPopUpOpen(true);
  }

  const handleCloseDocument = () =>{
    setIsPopUpOpen(false);
  }

  const getDocuments = async () => {
    const response = await fetch('https://healthcare-for-millennials-api.westeurope.azurecontainer.io/documents', {
      method: 'GET',
      headers: { 'Authorization': 'Bearer ' + token },
      credentials: 'include'

    });
    const content = await response.json()
    setUserDocuments(content);
  };

  useEffect(() => {
    getDocuments();
  }, []);

  const sendDocument = async () => {

    setIsProcessing(true);

    setIsFetching(true);
    var formdata = new FormData();
    formdata.append("uploadedFile", uploadedFile);
    formdata.append("documentName", documentName);
    const response = await fetch('https://healthcare-for-millennials-api.westeurope.azurecontainer.io/documents', {
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') },
      body: formdata,
      credentials: 'include'

    });

    const content = await response.json();
    setHasUploaded(true);
    setIsFetching(false);
    getDocuments();
  };

  if (isLoggedIn === "false") {
    return <Navigate to="/login" />;
  }
  return (
    <>
      <NavigationBar isLoggedIn={isLoggedIn} />     
      <div>
      <Snackbar
        open={isProcessing}
        onClose={handleClose}
        TransitionComponent={transition}
        key='1'
      >
        <Alert severity="info" variant="filled"sx={{ width: '100%' }}>
          Document is being processed...
        </Alert>
      </Snackbar>
      <Snackbar
        open={hasUploaded}
        onClose={handleClose}
        TransitionComponent={transition}
        key='2'
      >
        <Alert severity="success" variant="filled"sx={{ width: '100%' }}>
          Document successfully uploaded!
        </Alert>
      </Snackbar>
    </div>
      <Container maxWidth="lg">
        <Grid container spacing={2}>
          <Grid item xs={6}>
            {userDocuments ?
              <CustomList keyword="documents" data={userDocuments} handleOpen={handleOpenDocument}></CustomList>
              : <Box sx={{
                width: 350,
                height: 100,
                marginTop: "10px",
                marginLeft: "10px"
              }}>
                <Grid container spacing={2}>
                  <Grid item xs={8}>
                    <h6>Loading documents</h6>
                  </Grid>
                  <Grid item xs={4}>
                    <CircularProgress size="15px" />
                  </Grid>
                </Grid>
              </Box>}
          </Grid>
          <Grid item xs={6}>
            <Box
              sx={{
                height: 100
              }}
            />
            <Card sx={{ maxWidth: 450 }}>
              <CardContent>
                <Box sx={{
                  width: uploadBoxWidth,
                  marginTop: "10px",
                  marginLeft: "10px"
                }}>
                  <h5>Upload new document</h5>
                  <Grid container spacing={2}>
                    <Grid item xs={12}>
                      <input type="username" placeholder="Document name" size="40" required
                        onChange={e => setDocumentName(e.target.value)}
                      />

                    </Grid>
                    <Grid item xs={3}>
                      <div className="choose_file_button">
                        <input
                          accept="image/*"
                          className="input"
                          style={{ display: "none" }}
                          id="contained-button-file"
                          type="file"
                          onChange={(e) => {
                            setUploadedFile(null);
                            setUploadedFile(e.target.files[0]);
                          }}
                        />
                        <label htmlFor="contained-button-file">
                          <Button variant="outlined" component="span" className="button">
                            Browse...
                          </Button>
                        </label>
                      </div>
                    </Grid>
                    <Grid item xs={9}>
                      {uploadedFile ? uploadedFile.name : "No file selected."}
                    </Grid>
                    <Grid item xs={5}>
                    </Grid>
                    <Grid item xs={7}>
                      <div className="send-button">
                        <Button
                          className="upload_button"
                          component="span"
                          disabled={(documentName && uploadedFile) ? false : true}
                          onClick={(e) => sendDocument()}
                          variant="contained"
                        >
                          Upload document
                        </Button>
                      </div>
                    </Grid>
                  </Grid>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
      {isPopUpOpen === true && <PopUp type={"documents"} data={selectedDocument} text={selectedDocument.ocredText} handleClose={handleCloseDocument}/>}
    </>
  );
}