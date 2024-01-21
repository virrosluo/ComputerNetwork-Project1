import React from 'react';
import "./index.css"
import Leftbar from "./Leftbar"
import Rightbar from "./Rightbar"
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { 
  Typography,
  Box
 } from '@mui/material';
const theme1 = createTheme({
  typography: {
    button: {
      textTransform: "none"
    }
  }
});

function App() {
  return (
    <ThemeProvider theme={theme1}>
    <div className='grid-container'>
      <Leftbar />
      <Box sx={{p: 2}}>
        {/* Your component content goes here */}
        <Typography variant="h2">Client</Typography>
      </Box>
      <Rightbar />
    </div>
    </ThemeProvider>
  );
}

export default App;
