import React from 'react'
import {
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Collapse,
  Box
} from '@mui/material';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import {useState} from 'react'

export default function MultipleDropDown({parentArray, setParentArray}) {
  // console.log("Parent Array:", parentArray)
  const [secondDropDown, setSecondDropDown] = React.useState([]);
  // const [array, setArray] = [array, setArray];
  const [array, setArray] = [parentArray, setParentArray];

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


  return (<List sx={{
    width: '100%',
    maxWidth: 360,
    bgcolor: 'background.paper',
    position: 'relative',
    overflow: 'auto',
    maxHeight: 300,
    '& ul': { padding: 0 },
  }}>
    {array.map((item, index) => {
      const name = Object.keys(item)[0];
      const userArray = item[name];
      {/* console.log("Name:", name);
      console.log("User Array:", userArray); */}
    return (
      <Box key={index}>
      <ListItem key={index + item} disablePadding>
        <ListItemButton onClick={() => handleSecondDropDown(name + index)}>
          <ListItemText primary={name} />
          {secondDropDown.indexOf(name + index) !== -1 ? <KeyboardArrowDownIcon/> : <KeyboardArrowRightIcon/>}
        </ListItemButton>
      </ListItem>
      <Collapse in={secondDropDown.indexOf(name + index) !== -1}>
        <List>
          {userArray.map((user, index) => {
            return (
              <ListItem key={index + name} >
                <ListItemButton>
                  <ListItemText primary={user} />
                </ListItemButton>
              </ListItem>
            )
          })}
        </List>
      </Collapse>
      </Box>
    )
  })}
</List>)
}