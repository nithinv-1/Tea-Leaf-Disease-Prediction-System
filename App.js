import './App.css';

import {  BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import CameraComponent from './components/CaptureComponent';
import Navbar from './components/Navbar';
import ImageTable from './components/ImageTable';

function App() {
  return (
    <Router>
      <>
      <Navbar/>
      <Routes>
        <Route exact path="/" element={<CameraComponent/>}/>
        <Route exact path="/table" element={<ImageTable/>}/>
      </Routes>
      </>
    </Router>
  );
}

export default App;
