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
    const [displayedResultIndex, setDisplayedResultIndex] = useState(0)
    const [displayedWord, setDisplayedWord] = useState(0);
    const [displayedTermIndex, setDisplayedTermIndex] = useState(0);
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

    const changeDisplayedResult = (change) => {
      var newIndex = change + displayedResultIndex
      if (newIndex >= searchKeywords.length ) {
        newIndex = 0
      } else if (newIndex < 0) {
        newIndex = searchKeywords.length - 1
      }
      console.log(newIndex)
      setDisplayedResultIndex(newIndex)
      setDisplayedWord(0)
      setDisplayedTermIndex(0)
    }

    if (isLoading) {
      return (<></>)
    }

    
    return (
      <div>
        <div>
          <button onClick={() => changeDisplayedResult(-1)}>{"<-"}</button>
          <input
            className="searchBar"
            type="text"
            value={searchKeywords[displayedResultIndex]}
          />
          <button onClick={() => changeDisplayedResult(1)}>{"->"}</button>
        </div>
        <div>
          <div>
            <SearchResultDisplay 
              keyword={searchKeywords[displayedResultIndex]}
              searchResult={searchResults[searchKeywords[displayedResultIndex]]}
              displayedWord={displayedWord}
              displayedTermIndex={displayedTermIndex}
              selectedTerms={selectedTerms[searchKeywords[displayedResultIndex]]}
              setDisplayedWord={setDisplayedWord}
              setDisplayedTermIndex={setDisplayedTermIndex} 
              setSelectedTerms={setSelectedTerms}
            />
          </div>
        </div>
      </div>
    )

}