import React, { Component, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import SearchResultDisplay from "../components/SearchResultDisplay"

import { eel } from "../eel.js";

export default function SelectionScreen(props) {
    console.log("SelectionScreen")
    console.log(props)

    const [searchKeywords, setSearchKeywords] = useState(props.searchKeywords);
    const [searchResults, setSearchResults] = useState(props.searchResults);
    const [selectedTerms, setSelectedTerms] = useState({})
    const [displayedIndex, setDisplayedIndex] = useState(0)
    const [displayedWord, setDisplayedWord] = useState(0);
    const [displayedTerm, setDisplayedTerm] = useState(0);
    const [isLoading, setIsLoading] = useState(true);

    const fetchData = async () => {
      await eel.get_selected()((selected) => {
        setSelectedTerms(selected)
        setIsLoading(false);
      })
      
    }

    useEffect(() => {
      fetchData();
    }, []);

    const changeDisplayed = (change) => {
      let newIndex = change + displayedIndex
      if (newIndex >= searchResults.length ) {
        newIndex = 0
      } else if (newIndex < 0) {
        newIndex = searchResults.length - 1
      }
      setDisplayedIndex(newIndex)
      setDisplayedWord(0)
      setDisplayedTerm(0)
    }

    if (isLoading) {
      return (<div>Loading...</div>)
    }

    
    return (
      <div>
        <div>
          <button onClick={() => changeDisplayed(-1)}>{"<-"}</button>
          <input
            className="searchBar"
            type="text"
            value={searchKeywords[displayedIndex]}
          />
          <button onClick={() => changeDisplayed(1)}>{"->"}</button>
        </div>
        <div>
          <div>
            <SearchResultDisplay 
              keyword={searchKeywords[displayedIndex]}
              searchResult={searchResults[searchKeywords[displayedIndex]]}
              displayedWord={displayedWord}
              displayedTerm={displayedTerm}
              selectedTerms={selectedTerms[searchKeywords[displayedIndex]]}
              setDisplayedWord={setDisplayedWord}
              setDisplayedTerm={setDisplayedTerm} 
            />
          </div>
        </div>
      </div>
    )

}