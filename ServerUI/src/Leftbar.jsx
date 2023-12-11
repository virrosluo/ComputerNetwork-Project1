import React, { useState } from 'react';
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
import MultipleDropDown from './MultipleDropDown';
const SERVER_API_PORT = import.meta.env.VITE_SERVER_API_PORT

const Leftbar = () => {
  const [showAvailableFile, setShowAvailableFile] = React.useState(false);
  const [array, setArray] = useState(	[]);

  const [secondDropDown, setSecondDropDown] = React.useState([]);

  
  
  const [fileName, setFileName] = useState('');
  
  const handleSecondDropDown = (value)  => {
    const currentIndex = secondDropDown.indexOf(value);
    console.log(secondDropDown);
    const newSecondDropDown = [...secondDropDown];

    if (currentIndex === -1) {
      newSecondDropDown.push(value);
    } else {
      newSecondDropDown.splice(currentIndex, 1);
    }

    setSecondDropDown(newSecondDropDown);
  };


  function handleFileRefresh () {
    fetch(`http://127.0.0.1:${SERVER_API_PORT}/display`,{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      setArray(data)
      addSnackBar({message: "File Refreshed", variant: "success"})
    })
    .catch(err => {
      console.log(err)
      addSnackBar({message: "Failed to refresh", variant: "error"})
    })}

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
      Available file 
      {showAvailableFile ? <KeyboardArrowDownIcon/> : <KeyboardArrowRightIcon/>}
      </Button>
      <Collapse in={showAvailableFile}>
        <MultipleDropDown parentArray={array} setParentArray={setArray}/>
          
      </Collapse>
      {/* <Button variant='contained' sx={{m: 2}} > Refresh </Button> */}
      </Paper>
      <Box sx={{ml: 'auto'}}>
        <Button variant='contained' sx={{my: 2}} onClick={handleFileRefresh}> Refresh </Button>
      </Box>
    </Paper>
  );
};

export default Leftbar;
