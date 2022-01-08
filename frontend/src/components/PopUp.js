import React, { useState, useEffect } from "react";
import Button from "@mui/material/Button";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import Typography from "@mui/material/Typography";
import "./PopUp.css";

export default function PopUp(props) {
  const token = localStorage.getItem("token");
  const type = props.type;
  const data = props.data;
  const handleClose = props.handleClose;
  const [image, setImage] = useState(null);

  const [body, setBody] = useState(props.text);
  let description = "Document description:";

  const changeDiagnosisText = () => {
    const json = JSON.parse(body);
    var max = 0;
    var saved = "";
    for (var key in json){
      var value = json[key];
      if(value > max){
        saved = key;
        max = value;
      }
    }
    console.log(saved);
    if(saved === "Negative" || saved === "normal"){
      setBody("You are healthy.");
    } else {
      var diseaseName = saved.replace(/-/g, ' ');
      setBody(`You might have "${diseaseName}", please consult your specialist.`);
    }
  }

  const getImage = async () => {
    const response = await fetch(
      "https://healthcare-for-millennials-api.westeurope.azurecontainer.io/" + type + "/" + data.id,
      {
        method: "GET",
        headers: { Authorization: "Bearer " + token },
        credentials: "include",
      }
    );
    const content = await response.json();

    setImage(content);
  };

  useEffect(() => {
    getImage();
    if (type === "photos") {
      description = "Diagnosis:";
      changeDiagnosisText();
    }
  }, []);
  
  return (
    <div className="pop-up">
      <DialogTitle sx={{ m: 0, p: 2 }}>
        <IconButton
          aria-label="close"
          onClick={handleClose}
          sx={{
            position: "absolute",
            right: 8,
            top: 8,
            color: (theme) => theme.palette.grey[500],
          }}
        >
          <CloseIcon />
        </IconButton>
        {data.name}
      </DialogTitle>
      <div>
        <img className="image-container" alt="documentImage" src={image} />
      </div>

      <DialogContent dividers>
        <Typography
          variant="subtitle1"
          gutterBottom
          component="div"
          fontWeight="bold"
        >
          {description}
        </Typography>
        <Typography gutterBottom>{body}</Typography>
      </DialogContent>
      <DialogActions>
        <Button autoFocus onClick={handleClose}>
          Close
        </Button>
      </DialogActions>
    </div>
  );
}
