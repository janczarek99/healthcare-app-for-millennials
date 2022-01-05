import { NavigationBar } from "../NavigationBar";
import { Navigate} from "react-router-dom";
import React, {useState, useEffect} from 'react';
import { Button } from "@mui/material";
import axios from "axios";

export function DocumentsView() {
    const token = localStorage.getItem('token');
    const [isLoggedIn, setIsLoggedIn] = useState(localStorage.getItem('isLoggedIn'));
    const [uploadedFile, setUploadedFile] = useState(null);
    const [documentName, setDocumentName] = useState('')
    const [isFetching, setIsFetching] = useState(false);
    const [userDocuments, setUserDocuments] = useState(null);

    const getDocuments = async () => {
        const response = await fetch('http://localhost:9999/documents', {
            method: 'GET',
            headers: {'Authorization': 'Bearer '+token},
            credentials: 'include'
            
        });
        const content = await response.json()
        console.log(content);
        setUserDocuments(content);
    };

    useEffect(() => {
        getDocuments();
      }, []);

    const sendDocument = async () => {
        setIsFetching(true);
        var formdata = new FormData();
        formdata.append("uploadedFile", uploadedFile);
        formdata.append("documentName", documentName);
        const response = await fetch('http://localhost:9999/documents', {
            method: 'POST',
            headers: {'Authorization': 'Bearer '+localStorage.getItem('token')},
            body: formdata,
            credentials: 'include'
            
        });

        const content = await response.json();
        console.log(content);

        setIsFetching(false);
        getDocuments();
      };

    if (isLoggedIn === "false"){
        return <Navigate to="/login"/>;
    } 
    return (
        <>
        <NavigationBar isLoggedIn={isLoggedIn}/>
        {userDocuments ? 
        <>
            <ol>
                {userDocuments.map((document) => (
                <li key={document.id} >{document.name}</li>
                ))}
            </ol>
        </> 
        : <></>}

        <input type="username" placeholder="Document name" required
                    onChange={e => setDocumentName(e.target.value)}
                />
        <div className="choose_file_button">
          <input
            accept="image/*"
            className="input"
            style={{ display: "none" }}
            id="contained-button-file"
            type="file"
            onChange={(e) => {
              console.log(e.target.files[0]);
              setUploadedFile(null);
              setUploadedFile(e.target.files[0]);
            }}
          />
          <label htmlFor="contained-button-file">
            <Button variant="outlined" component="span" className="button">
              Choose document
            </Button>
          </label>
        </div>

        <div className="send-button">
          <Button
            className="upload_button"
            component="span"
            disabled={uploadedFile ? false : true}
            onClick={(e) => sendDocument()}
            variant="contained"
          >
            Upload document
          </Button>
        </div>

        </>
      );
}