import React, { useState } from "react";
import ReactDOM from 'react-dom';

import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import './App.css';

import SearchScreen from './screens/SearchScreen';
import SelectionScreen from './screens/SelectionScreen';




function App() {
  const [searchKeywords, setSearchKeywords] = useState([]);
  const [searchResults, setSearchResults] = useState([]);

  React.useEffect(() => {
    eel.hello_eel();
  }, []);

  const router = createBrowserRouter([
    {
        path: '/',
        element: <SearchScreen 
          searchKeywords={searchKeywords}
          searchResults={searchResults}
          setSearchKeywords={setSearchKeywords}
          setSearchResults={setSearchResults}
        />,
    },
    {
        path: '/selection',
        element: <SelectionScreen 
        searchKeywords={searchKeywords}
        searchResults={searchResults}
        setSearchKeywords={setSearchKeywords}
        setSearchResults={setSearchResults}
      />,
    }
  ]) //change to memory router??
  

  return (
    <div className="App">
      <header className="">
      </header>
      
    <React.StrictMode>
      <RouterProvider router={router} />
    </React.StrictMode>
    </div>
  );
}

export default App;
