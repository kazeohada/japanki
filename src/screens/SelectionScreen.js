import React, { Component, useState } from "react";
import { useNavigate } from "react-router-dom";

import SearchResultDisplay from "../components/SearchResultDisplay"

import { eel } from "../eel.js";

export default function SelectionScreen(props) {
    const [searchKeywords, setSearchKeywords] = useState(props.searchKeywords);
    const [searchResults, setSearchResults] = useState(props.searchResults);
    const [selectedTerms, setSelectedTerms] = useState([])
    const [displayedIndex, setDisplayedIndex] = useState(0)
    const navigate = useNavigate();
    console.log(searchResults);

    React.useEffect(() => {
      eel.hello_eel();
    }, []);

    const changeDisplayed = (change) => {
      let newIndex = change + displayedIndex
      if (newIndex >= searchResults.length ) {
        newIndex = 0
      } else if (newIndex < 0) {
        newIndex = searchResults.length - 1
      }
      setDisplayedIndex(newIndex);
    }

    
    return (
      <div>
        <div>
          <button onClick={() => changeDisplayed(-1)}>{"<-"}</button>
          <input
            className="searchBar"
            type="text"
            value={searchResults[displayedIndex].keyword}
          />
          <button onClick={() => changeDisplayed(1)}>{"->"}</button>
        </div>
        <div>
          <div>
            <SearchResultDisplay searchResult={searchResults[displayedIndex]} />
          </div>
        </div>
      </div>
    )

}