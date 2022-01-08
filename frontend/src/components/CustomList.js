import * as React from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemText from '@mui/material/ListItemText';
import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import FolderIcon from '@mui/icons-material/Folder';
import DeleteIcon from '@mui/icons-material/Delete';
import ListItemButton from '@mui/material/ListItemButton';


export default function CustomList(props) {
  const descLength = 60;

  return (
    <Box sx={{ 
        marginLeft: "10px",
        flexGrow: 1, maxWidth: 752 
        }}>
      <Grid item xs={12}>
        <Typography sx={{ mt: 4, mb: 2 }} variant="h6" component="div">
          Uploaded {props.keyword}
        </Typography>
        {props.data.length > 0 ? <></> : <h6>You don't have any {props.keyword}.</h6>}
        <List style={{ maxHeight: "70vh", overflow: 'auto' }}>
          {props.data.map((entry) => (
              <ListItem
              key={entry.id}
              secondaryAction={
                <IconButton edge="end" aria-label="delete">
                  <DeleteIcon />
                </IconButton>
              }
            >
              <ListItemAvatar>
                <Avatar>
                  <FolderIcon />
                </Avatar>
              </ListItemAvatar>
              <ListItemButton >
        <ListItemText 
          onClick={() => props.handleOpen(entry)}
          primary={entry.name}
          secondary={
            <React.Fragment>
              <Typography
                sx={{ display: 'inline' }}
                component="span"
                variant="body2"
                color="text.primary"
              >
              </Typography>
              {entry.ocredText ? entry.ocredText.substring(0, descLength) + '...' : entry.modelType}
            </React.Fragment>
          }
        />
      </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Grid>
    </Box>
  );
}
