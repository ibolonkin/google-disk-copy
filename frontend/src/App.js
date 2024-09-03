import React from "react";
import Login from "./components/Login/Login";
import { Route, Routes } from "react-router-dom";
import Registration from "./components/Registration/Registration";
import PrivateRoute from "./components/PrivateRoute/PrivateRoute";
import Main from "./components/Main/Main";


function App() {
  return (
    <div className="App">

        <Routes>
          <Route path="/" element={<Registration/>}/>
          <Route path="/login" element={<Login />}/>

          <Route path='/main' element={<PrivateRoute />}>
            <Route path='' element={<Main />} />
          </Route>
          
        </Routes>
       
    </div>
  );
}

export default App;
