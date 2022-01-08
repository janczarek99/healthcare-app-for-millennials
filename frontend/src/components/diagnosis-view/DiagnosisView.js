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

import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';

function TransitionUp(props) {
    return <Slide {...props} direction="up" />;
  }

export function DiagnosisView() {
    const token = localStorage.getItem('token');
    const [isLoggedIn, setIsLoggedIn] = useState(localStorage.getItem('isLoggedIn'));
    const [userPhotos, setUserPhotos] = useState(null);
    const [photoName, setPhotoName] = useState('')
    const [modelType, setModelType] = useState('')
    const [uploadedFile, setUploadedFile] = useState(null);
    const uploadBoxWidth = 450;

    const [isProcessing, setIsProcessing] = React.useState(false);
    const [hasUploaded, setHasUploaded] = React.useState(false)

    const [isPopUpOpen, setIsPopUpOpen] = useState(false);
    const [selectedPhoto, setSelectedPhoto] = useState(null);
    const [transition, setTransition] = React.useState(() => TransitionUp);

    const handleOpenPhoto = (document) => {
        setSelectedPhoto(document);
        setIsPopUpOpen(true);
    }

    
    const handleClosePhoto = () => {
        setIsPopUpOpen(false);
    }

    const handleModelTypeChange = (event) => {
        setModelType(event.target.value);
    };


    const handleClose = () => {
        setIsProcessing(false);
        setHasUploaded(false)
      };

    useEffect(() => {
        getPhotos();
    }, []);

    const getPhotos = async () => {
        const response = await fetch('https://healthcare-for-millennials-api.westeurope.azurecontainer.io/photos', {
            method: 'GET',
            headers: { 'Authorization': 'Bearer ' + token },
            credentials: 'include'

        });
        const content = await response.json()
        setUserPhotos(content);
    };

    const sendPhoto = async () => {

        setIsProcessing(true);

        var formdata = new FormData();
        formdata.append("uploadedFile", uploadedFile);
        formdata.append("photoName", photoName);
        formdata.append("modelType", modelType);
        const response = await fetch('https://healthcare-for-millennials-api.westeurope.azurecontainer.io/photos', {
            method: 'POST',
            headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') },
            body: formdata,
            credentials: 'include'

        });

        const content = await response.json();
        setHasUploaded(true);

        getPhotos();
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
                    <Alert severity="info" variant="filled" sx={{ width: '100%' }}>
                        Photo is being processed...
                    </Alert>
                </Snackbar>
                <Snackbar
                    open={hasUploaded}
                    onClose={handleClose}
                    TransitionComponent={transition}
                    key='2'
                >
                    <Alert severity="success" variant="filled" sx={{ width: '100%' }}>
                        Photo successfully uploaded!
                    </Alert>
                </Snackbar>
            </div>
            <Container maxWidth="lg">
                <Grid container spacing={2}>
                    <Grid item xs={6}>
                        {userPhotos ?
                            <CustomList keyword="photos" data={userPhotos} handleOpen={handleOpenPhoto}></CustomList>
                            : <Box sx={{
                                width: 350,
                                height: 100,
                                marginTop: "10px",
                                marginLeft: "10px"
                            }}>
                                <Grid container spacing={2}>
                                    <Grid item xs={8}>
                                        <h6>Loading photos</h6>
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
                                    <h5>Upload new photo</h5>
                                    <Grid container spacing={2}>
                                        <Grid item xs={12}>
                                            <input type="username" placeholder="Photo name" size="40" required
                                                onChange={e => setPhotoName(e.target.value)}
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

                                        <Grid item xs={12}>
                                            <FormControl component="fieldset">
                                                <FormLabel component="legend">Model type</FormLabel>
                                                <RadioGroup
                                                    aria-label="model_type"
                                                    name="controlled-radio-buttons-group"
                                                    value={modelType}
                                                    onChange={handleModelTypeChange}
                                                >
                                                    <FormControlLabel value="LUNG_CANCER" control={<Radio />} label="LUNG_CANCER" />
                                                    <FormControlLabel value="PNEUMONIA" control={<Radio />} label="PNEUMONIA" />
                                                    <FormControlLabel value="BRAIN_TUMOUR" control={<Radio />} label="BRAIN_TUMOUR" />
                                                </RadioGroup>
                                            </FormControl>
                                        </Grid>

                                        <Grid item xs={5}>
                                        </Grid>
                                        <Grid item xs={7}>
                                            <div className="send-button">
                                                <Button
                                                    className="upload_button"
                                                    component="span"
                                                    disabled={(photoName && uploadedFile && modelType) ? false : true}
                                                    onClick={(e) => sendPhoto()}
                                                    variant="contained"
                                                >
                                                    Upload photo
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
            {isPopUpOpen === true && <PopUp type={"photos"} data={selectedPhoto} text={selectedPhoto.modelResult} handleClose={handleClosePhoto}/>}
        </>
    );
}