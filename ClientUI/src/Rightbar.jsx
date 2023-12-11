import React, { useEffect } from 'react';
import { 
  Collapse,
  Button,
  Paper,
  Box,
  Stack
} from '@mui/material';

import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import List from '@mui/material/List';
import Checkbox from '@mui/material/Checkbox';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import TextField from '@mui/material/TextField';
import { useState } from 'react';
import NumberInput from './Numberinput'
import { useSnackbar } from 'notistack';
import addSnackBar from './addSnackBar';
import MultipleDropDown from './MultipleDropDown';

const CLIENT_API_PORT = import.meta.env.VITE_CLIENT_API_PORT;

import "./rightbar.css"

const Rightbar = () => {
  const [showAvailableFile, setShowAvailableFile] = React.useState(false);
  const [fetchAbleFile, setFetchAbleFile] = useState(["file1", "file2", "file3"]);
  const [fetchFile, setFetchFile] = useState([]);
  const [clientName, setClientName] = useState('');
  const [checked, setChecked] = React.useState([]);

  // async function handleFetchRefresh () {
  //   const fileName = await fetchFile();
  //   console.log(fileName);
  //   const fetchResult = await Promise.all(fileName.map((item, index) => {
  //     const huh = fetchFileOwner(item).then((data) => {
  //       // console.log('fileowner', data);
  //       return {[item]: data};
  //     })
  //     // console.log('huh', huh);
  //     return huh;
  //   }))
  //   setFetchAbleFile(fetchResult);
  //   console.log(fetchResult);
  // }


  // async function handleFetchRefresh() {
  //   const fileName = await fetchFile();
  //   console.log(fileName);
  //   const fetchResult = await Promise.all(
  //     fileName.map(async (item, index) => {
  //       const data = await fetchFileOwner(item);
  //       console.log('fileowner', data);
  //       return data;
  //     })
  //   );
  //   console.log(fetchResult);
  // }

  async function handleFetchFileRefresh(){
    // return the file [file1, file2, file3]
    console.log('refresh');
    fetch(` http://127.0.0.1:${CLIENT_API_PORT}/fetch_from_server`,{
      method: 'GET',
      mode: 'cors',
    })
    .then(response => response.json())
    .then(data => {
      // console.log(data);
      console.log(data);
      if(data !== null && data.length !== 0)
      setFetchAbleFile(data);
      else
      setFetchAbleFile([]);

      return data;
    })
    // console.log(data);
  }

  async function fetchFileOwner (fName) {
    // return the file owner IP address and port {'address': IPAddress, 'port': Int}
    const data = await fetch(` http://127.0.0.1:${CLIENT_API_PORT}/fetch_file_owner/${fName}`,{
      method: 'GET',
      mode: 'cors',
    })
    .then(response => response.json())
    .then(data => {
      // console.log(data);
      // setFetchAbleFile(data);
      return data;
    })
    return data;
  }

  async function fetchFileFromOwner (fName, ownerAddress) {
    fetch(` http://127.0.0.1:${CLIENT_API_PORT}/fetch_from_client/${fName}/${ownerAddress.address}/${ownerAddress.port}`,{
      method: 'POST',
      mode: 'cors',
    }).then(response => response.json())
    .then(data => {
      if (data.download_status === 'success')
      addSnackBar({message: `Fetch ${fName} success`, variant: "success"});
      else
      addSnackBar({message: `Fetch ${fName} fail`, variant: "error"});
    })
  }

  async function handleFetchFile () {
    // Make a fetch request to fetch the file
    console.log('fetch File');
    console.log(fetchFile);
    fetchFile.map(async (fName, index) => {
      console.log(fName);
      const ownerAddress = await fetchFileOwner(fName)
      fetchFileFromOwner(fName, ownerAddress);
    })
  }

  async function startClient (clientName) {
    console.log(clientName);
    const data = await fetch(` http://127.0.0.1:${CLIENT_API_PORT}/start/${clientName}`,{
      method: 'POST',
      mode: 'cors',
    })
    .then(response => response.json())
    .then(data => {
      addSnackBar({message: `Start Client ${clientName} success`, variant: "success"});
    })
    .catch((error) => {
      addSnackBar({message: `Start Client ${clientName} fail`, variant: "error"});
    })
  }

  async function stopClient () {
    console.log(clientName);
    const data = await fetch(` http://127.0.0.1:${CLIENT_API_PORT}/exit`,{
      method: 'POST',
      mode: 'cors',
    })
  }

  
  useEffect(() => {
    async function fetchData () {
      const data = await handleFetchFileRefresh();
      // setFetchAbleFile(data);
    }
    fetchData();
  }, [])
  
  
    const handleToggle = (value, fName) => () => {
      const currentIndex = checked.indexOf(value);
      const newFetchFile = [...fetchFile];
      const newChecked = [...checked];
  
      if (currentIndex === -1) {
        newFetchFile.push(fName);
        newChecked.push(value);
      } else {
        newFetchFile.splice(currentIndex, 1);
        newChecked.splice(currentIndex, 1);
      }
      setFetchFile(newFetchFile);
      setChecked(newChecked);
    };




  return (
    // the right bar elevation
    <Paper className='left-bar' elevation={3} sx={{p:1 , display: 'flex', flexDirection:'column', maxWidth:'400px'}}>
      {/*
        Drop Down bar 
      */}
      <Paper elevation={3}>
      <Button className="dropdown-button" variant="contained" variant="text" onClick={() => {setShowAvailableFile(!showAvailableFile)}} sx={{fontSize: 18, width: `100%`, justifyContent: "space-between"}}>Fetchable file {showAvailableFile ? <KeyboardArrowDownIcon/> : <KeyboardArrowRightIcon/>}</Button>
      <Collapse in={showAvailableFile}>
        {/* <MultipleDropDown parentArray={fetchAbleFile} setParentArray={setFetchAbleFile}/> */}
        <List sx={{
            width: '100%',
            maxWidth: 360,
            bgcolor: 'background.paper',
            position: 'relative',
            overflow: 'auto',
            maxHeight: 300,
            '& ul': { padding: 0 },
          }}>
          {fetchAbleFile.map((fName, index) => {
            return (
              <ListItem key={index} disablePadding>
                <ListItemButton onClick={handleToggle(index, fName)}>
                  <ListItemText primary={fName} />
                  <Checkbox
                  edge="end"
                  checked={checked.indexOf(index) !== -1}
                />
                </ListItemButton>
              </ListItem>
            )
          })}
        </List>
      </Collapse>
      </Paper>

      {/*
        Refresh button
      */}
      <Box sx={{ml: 'auto'}}>
        <Button variant='contained' sx={{my: 2 }} onClick={() => handleFetchFileRefresh()} > Refresh </Button>
      </Box>


      {/*
        Discover and Ping button
      */}
      <Stack spacing={2} direction="row" sx={{ my: 2, ml: 'auto' }} >
        <Button variant='contained'  onClick={handleFetchFile}> Fetch </Button>
      </Stack>

      {/*
        Performance test
      */}

      {/* <NumberInput min={0} placeholder="Times"></NumberInput>
      <Box sx={{ml: 'auto'}}>
        <Button variant='contained' sx={{my: 2}}> Performance test</Button>
      </Box> */}

      {/*
        Start and close client
      */}

      <Box spacing={2} sx={{ml: 'auto', mt:'auto', width:`100%`}}>
        <TextField 
        // error
        // helperText="Incorrect entry."
        label="Client name"
        sx={{width: `100%`, mb: 2}}
        onChange={(e) => {setClientName(e.target.value)}}
        />
        <Stack spacing={2} direction={'row'} justifyContent={'space-between'} sx={{my: 2}}>
        <Button variant='contained' sx={{my: 2}} onClick={() => {startClient(clientName)}}> Start client </Button>
        <Button variant='outlined' sx={{my: 2}} onClick={stopClient}> Close client</Button>
        </Stack>
      </Box>
    </Paper>
  );
}

export default Rightbar;