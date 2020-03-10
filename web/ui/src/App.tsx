import React from 'react';
import './App.css';
import 'antd/dist/antd.css';

import Event from "./components/Event";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Event></Event>
      </header>
    </div>
  );
}

export default App;
