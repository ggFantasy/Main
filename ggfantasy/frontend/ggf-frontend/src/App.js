import React from 'react';
import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";

import LiveMatch from './components/views/LiveMatch/index.jsx';

function App() {
  return (
      <div>
    <Router>
        <Route path='/Live' component={LiveMatch} />
    </Router>
    </div>
  );
}

export default App;
