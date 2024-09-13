import React, { Component } from "react";
import logo from "./logo.svg";
import "./App.css";
import SearchScreen from "./screens/SearchScreen.js";

import { eel } from "./eel.js";

class App extends Component {
  constructor(props) {
    super(props);
    eel.set_host("ws://localhost:8888");
    eel.hello();
  }
  render() {
    return (
      <div className="App">
        <header className="App-header">
        </header>
        <SearchScreen/>
      </div>
    );
  }
}

export default App;
