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
import DesktopMacIcon from '@mui/icons-material/DesktopMac';
import MultipleDropDown from './MultipleDropDown';
import "./rightbar.css"

const SERVER_API_PORT = import.meta.env.VITE_SERVER_API_PORT

const Rightbar = () => {
  const [showAvailableFile, setShowAvailableFile] = React.useState(false);
  const [PCs, setPCs] = useState([]);
  const [discover, setDiscover] = useState([]);
  const [checked, setChecked] = React.useState([]);
  const [discoverDropDown, setDiscoverDropDown] = React.useState([]);

  function handleFetchRefresh() {
    fetch(` http://127.0.0.1:${SERVER_API_PORT}/getClient`,{
      mode: "cors", // no-cors, *cors, same-origin
    })
      .then(response => response.json())
      .then(data => {
        console.log(data)
        addSnackBar({ message: "Refreshed", variant: "success" })
        setPCs(data)
      })
      .catch(err => {
        console.log(err)
        addSnackBar({ message: "Failed to refresh", variant: "error" })
      })
  }

  function fetchPing(address, name, serverHandlerPort, clientHandlerPort) {
    fetch(` http://127.0.0.1:${SERVER_API_PORT}/ping_client?` + new URLSearchParams({
      address: address,
      name: name,
      serverHandlerPort: serverHandlerPort,
      clientHandlerPort: clientHandlerPort
    }),{
      method: "GET", // *GET, POST, PUT, DELETE, etc.
      mode: "cors", // no-cors, *cors, same-origin
    })
      .then(response => response.json())
      .then(data => {
        if (data.client_status === true)
          addSnackBar({ message: `Client ${name} is alive`, variant: "success" })
        else
          addSnackBar({ message: `Client ${name} is down`, variant: "error" })

      })
      .catch(err => {
        // console.log(err)
        addSnackBar({ message: `Client ${name} is no longer alive`, variant: "error" })
      })
  }

  function handleFetch() {
    console.log('fetched')
    PCs.forEach((item) => {
      if (checked.indexOf(item) !== -1)
        fetchPing(item.address, item.name, item.serverHandlerPort, item.clientHandlerPort)
    })
  }



  function fetchDiscover(address, name, serverHandlerPort, clientHandlerPort) {
    const data = fetch(` http://127.0.0.1:${SERVER_API_PORT}/discover_file?` + new URLSearchParams({
      address: address,
      name: name,
      serverHandlerPort: serverHandlerPort,
      clientHandlerPort: clientHandlerPort
    })
      , {
        method: "GET", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, *cors, same-origin
      })
      .then(response => response.json())
      .then(data => {
        addSnackBar({ message: "Discover success", variant: "success" })
        return data
      })
      .catch(err => {
        console.log(err)
        addSnackBar({ message: "Discover fail", variant: "error" })
      })
      return data;
  }

  function handleDiscover() {
    console.log('discovered');
    const promises = PCs.map((item) => {
      if (checked.indexOf(item) !== -1) {
        return fetchDiscover(item.address, item.name, item.serverHandlerPort, item.clientHandlerPort)
          .then((data) => {
            console.log(data);
            const key = item.address + ' ' + item.name;
            return { [key] : data };
          });
      }
      return null;
    });

    Promise.all(promises)
      .then((results) => {
        const newDiscover = results.filter((result) => result !== null);
        console.log('newdis', newDiscover);
        setDiscover(newDiscover);
      })
      .catch((err) => {
        console.log(err);
        addSnackBar({ message: "Discover failed", variant: "error" });
      });
  }

  async function handleStartServer() {
    // addSnackBar({ message: "Server started", variant: "success" })
    fetch(` http://127.0.0.1:${SERVER_API_PORT}/start`, {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
      mode: "cors", // no-cors, *cors, same-origin
      cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
      credentials: "same-origin", // include, *same-origin, omit
      headers: {
        // "Content-Type": "application/json",
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      redirect: "follow", // manual, *follow, error
      referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    })
      .then(response => response.json())
      .then(data => {
        console.log(data)
        addSnackBar({ message: "Server started", variant: "success" })
      })
      .catch(err => {
        console.log(err)
        addSnackBar({ message: "Server failed to start", variant: "error" })
      })
  }
  const handleDeleteServer = () => {
    addSnackBar({ message: "Server closed", variant: "warning" })
    fetch(` http://127.0.0.1:${SERVER_API_PORT}/exit`, {
      method: "POST", // *GET, POST, PUT, DELETE, etc.
      mode: "cors", // no-cors, *cors, same-origin
      cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
      credentials: "same-origin", // include, *same-origin, omit
      headers: {
        // "Content-Type": "application/json",
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      redirect: "follow", // manual, *follow, error
      referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    })
      .then(response => response.text())
      .then(data => {
        console.log(data)
        addSnackBar({ message: "Server closed", variant: "warning" })
      })
      .catch(err => {
        console.log(err)
        addSnackBar({ message: "Server failed to close", variant: "error" })
      })
  }


  useEffect(() => {
    handleFetchRefresh()
    handleFetch()
  }, []);

  const handleToggle = (value) => () => {
    const currentIndex = checked.indexOf(value);
    const newChecked = [...checked];

    if (currentIndex === -1) {
      newChecked.push(value);
    } else {
      newChecked.splice(currentIndex, 1);
    }

    setChecked(newChecked);
  };

  return (
    // the right bar elevation
    <Paper className='left-bar' elevation={3} sx={{ p: 1, display: 'flex', flexDirection: 'column', maxWidth: '400px' }}>
      {/*
        Drop Down bar 
      */}
      <Paper elevation={3}>
        <Button className="dropdown-button" variant="text" onClick={() => { setShowAvailableFile(!showAvailableFile) }} sx={{ fontSize: 18, width: `100%`, justifyContent: "space-between" }}>Connected PC{showAvailableFile ? <KeyboardArrowDownIcon /> : <KeyboardArrowRightIcon />}</Button>
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
            {PCs.map((item, index) => {
              return (
                <ListItem key={index} disablePadding>
                  <ListItemButton onClick={handleToggle(item)}>
                    <DesktopMacIcon sx={{ mr: 2 }} />
                    <ListItemText primary={item.name + ' ' + item.address} />
                    <Checkbox
                      edge="start"
                      checked={checked.indexOf(item) !== -1}
                      tabIndex={-1}
                      disableRipple
                      inputProps={{ 'aria-labelledby': item }}

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
      <Box sx={{ ml: 'auto' }}>
        <Button variant='contained' sx={{ my: 2 }} onClick={() => handleFetchRefresh()} > Refresh </Button>
      </Box>


      {/*
        Discover and Ping button
      */}
      <Stack spacing={2} direction="row" sx={{ my: 2, ml: 'auto' }} >
        <Button variant='contained' onClick={handleFetch}> Ping </Button>
        <Button variant='contained' onClick={handleDiscover}> Discover </Button>
      </Stack>

      { discover.length > 0 && <Paper elevation={3} >
        <MultipleDropDown parentArray={discover} setParentArray={setDiscover} />
      </Paper>}

      {/*
        Start and close client
      */}

      <Box spacing={2} sx={{ ml: 'auto', mt: 'auto', width: `100%` }}>
        {/* <TextField
          label="Port number"
          sx={{ width: `100%` }}
        /> */}
        <Stack spacing={2} direction={'row'} justifyContent={'space-between'} sx={{ my: 2 }}>
          <Button variant='contained' sx={{ my: 2 }} onClick={handleStartServer}> Start server </Button>
          <Button variant='outlined' sx={{ my: 2 }} onClick={handleDeleteServer}> Close server</Button>
        </Stack>
      </Box>
    </Paper>
  );
}

export default Rightbar;