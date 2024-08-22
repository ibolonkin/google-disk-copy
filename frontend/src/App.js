import React from "react";
import Login from "./components/Login/Login";
import { Route, Routes } from "react-router-dom";
import Registration from "./components/Registration/Registration";


function App() {
  return (
    <div className="App">

      <Routes>
        <Route path="/" element={<Registration/>}/>
        <Route path="/sign-in" element={<Login />}/>
      </Routes>
      
      
    </div>
  );
}

export default App;
