import { useState } from 'react'
import './App.css'
import Navbar from './components/navbar'
import Main from './components/main'
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Hitesh_sir_chat from './components/hitesh_sir_chat.jsx';
import Piyush_sir_chat from './components/piyush_sir_chat.jsx';



  const router = createBrowserRouter([
    {
      path: "/",
      element: (
        <>
        <Navbar />
        <Main />
        </>
      ),
    },
    {
      path: "/hitesh_sir",
      element: (
        <>
          <Navbar />
          <Hitesh_sir_chat />
        </>
      ),
    },
    {
      path: "/piyush_sir",
      element: (
        <>
          <Navbar />
          <Piyush_sir_chat />
        </>
      ),
    },
  ]);
function App() {

  return (
    <>
     <RouterProvider router={router}>
      
    </RouterProvider>
    </>
  )
}

export default App
