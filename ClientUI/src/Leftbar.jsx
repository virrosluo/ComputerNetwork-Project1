import React, { useState, useEffect } from 'react';
import { 
  Collapse,
  Button,
  Paper,
  Box,
  TextField
} from '@mui/material';

import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import List from '@mui/material/List';
import Checkbox from '@mui/material/Checkbox';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import DeleteIcon from '@mui/icons-material/Delete';
import CloseIcon from '@mui/icons-material/Close';
import addSnackBar from './addSnackBar';
import "./leftbar.css"

const CLIENT_API_PORT = import.meta.env.VITE_CLIENT_API_PORT;

const Leftbar = () => {
  const [showAvailableFile, setShowAvailableFile] = React.useState(false);
  const [fileArray, setFileArray] = useState(["file1", "file2", "file3"])
  const [fileName, setFileName] = useState('');
  const [fileDirectory, setFileDirectory] = useState('');

  const handleDelete = (index, fname) => {
    const newFileArray = [...fileArray]
    fetch(` http://127.0.0.1:${CLIENT_API_PORT}/delete/${fname}`,{
      method: 'POST',
      mode: 'cors',
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      handleRefreshPublishedFile();
    })

    newFileArray.splice(index, 1)
    // setFileArray(newFileArray)
    addSnackBar({message: "Deleted", variant: "success"})
  }


  function handleRefreshPublishedFile () {
    fetch(` http://127.0.0.1:${CLIENT_API_PORT}/display`,{
      method: 'GET',
      mode: 'cors',
    })
    .then(response => response.json())
    .then(data => {
      // console.log(data);
      setFileArray(data);
    })
  }

  useEffect(() => {
    handleRefreshPublishedFile();
  }, [])

  const handleFileChange = (event) => {
    const fileInput = event.target;
    if (fileInput.files.length > 0) {
      const file = fileInput.files[0];
      setFileName(`${file.name}`);
    } else {
      setFileName('');
    }
  };

  function handlePublishFile(event){
    event.preventDefault();
    const form = event.target;
    const fileName = form.elements.publishFileName.value;
    const directory = form.elements.publishDirectory.value;
    fetch(` http://127.0.0.1:${CLIENT_API_PORT}/publish?` + new URLSearchParams({
      filepath: directory,
      new_fileName: fileName
  }),{
      method: 'POST',
      mode: 'cors',
      body: JSON.stringify({fileName, directory}),
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      handleRefreshPublishedFile();
    })

  }

  return (
    
    <Paper className='left-bar' elevation={1} sx={{p:1 , display: 'flex', flexDirection:'column'}} >
      {/* Your component content goes here */}
      <Paper elevation={3} sx={{mb:2}}>
      <Button 
      className="dropdown-button" 
      variant="text" 
      onClick={() => {setShowAvailableFile(!showAvailableFile)}} 
      sx={{fontSize: 18, width: `100%`, justifyContent: "space-between"}}
      >
      Published File 
      {showAvailableFile ? <KeyboardArrowDownIcon/> : <KeyboardArrowRightIcon/>}
      </Button>
      <Collapse in={showAvailableFile}>
        
          <List sx={{
            width: '100%',
            maxWidth: 360,
            bgcolor: 'background.paper',
            position: 'relative',
            overflow: 'auto',
            maxHeight: 300,
            '& ul': { padding: 0 },
          }}>
            {fileArray.map((item, index) => {
            return (
              <ListItem key={index} disablePadding>
                <ListItemButton>
                  <ListItemText primary={item} />
                  <DeleteIcon onClick={() => handleDelete(index, item)}/>
                </ListItemButton>
              </ListItem>
            )
          })}
        </List>
      </Collapse>
      {/* <Button variant='contained' sx={{m: 2}} > Refresh </Button> */}
      </Paper>
      <form onSubmit={handlePublishFile}>
      <TextField
        id="outlined-basic"
        label="File directory"
        variant="outlined"
        name='publishDirectory'
        onChange={(e) => setFileDirectory(e.target.value)}
        sx={{mb: 2, width: `100%`}}
      />
      <TextField
        label="New file name"
        variant="outlined"
        name='publishFileName'
        onChange={(e) => setFileName(e.target.value)}
        sx={{mb: 2, width: `100%`}}
      />
      {/* <input
        accept="image/*"
        style={{ display: 'none' }}
        id="raised-button-file"
        multiple
        type="file"
        name='publishFile'
        onChange={handleFileChange}
      />
      <label htmlFor="raised-button-file">
        <Button variant="raised" component="span" sx={{width: `100%`}}>
        {fileName ? fileName : 'Upload'}
        </Button>
      </label> */}
      <Box sx={{ml: 'auto', width: `100%`}}>
        <Button variant='contained' type='submit' sx={{my: 2, ml:'auto'}}> Publish </Button>
      </Box>
      </form>
    </Paper>
  );
};

export default Leftbar;
