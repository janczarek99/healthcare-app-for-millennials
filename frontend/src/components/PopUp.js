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

  let description = "Document description:";
  if (type === "photos") {
    description = "Diagnosis:";
  }

  const getImage = async () => {
    const response = await fetch(
      "http://localhost:9999/" + type + "/" + data.id,
      {
        method: "GET",
        headers: { Authorization: "Bearer " + token },
        credentials: "include",
      }
    );
    const content = await response.json();

    setImage(content);
    console.log(content);
  };

  useEffect(() => {
    getImage();
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
        <Typography gutterBottom>{data.ocredText}</Typography>
      </DialogContent>
      <DialogActions>
        <Button autoFocus onClick={handleClose}>
          Close
        </Button>
      </DialogActions>
    </div>
  );
}
