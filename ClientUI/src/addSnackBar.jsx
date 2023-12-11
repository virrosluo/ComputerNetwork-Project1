import React from 'react';;
import { closeSnackbar, enqueueSnackbar } from 'notistack';
import CloseIcon from '@mui/icons-material/Close';
const action = snackbarId => (
  <>
    <CloseIcon onClick={() => { closeSnackbar(snackbarId) }}>
      Dismiss
    </CloseIcon>
  </>
);

export default function addSnackBar({message, variant}) {
  enqueueSnackbar(message, {
    action,
    variant: variant,
  })

}