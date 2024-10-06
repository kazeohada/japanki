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
    const [displayedWordIndex, setDisplayedWordIndex] = useState(0);
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

    if (isLoading) {
      return (<></>)
    }

    const changeDisplayedResult = (change) => {
      var newIndex = change + displayedResultIndex
      if (newIndex >= searchKeywords.length ) {
        newIndex = 0
      } else if (newIndex < 0) {
        newIndex = searchKeywords.length - 1
      }
      console.log(newIndex)
      setDisplayedResultIndex(newIndex)
      setDisplayedWordIndex(0)
      setDisplayedTermIndex(0)
    }

    const generateCards = () => {
      eel.generate_anki()();
    }
    
    return (
      <div style={{padding: "2% 5%"}}>
        <div class="selectionScreenComponent" >
          <button onClick={() => changeDisplayedResult(-1)}>{"<-"}</button>
          <input
            className="searchBar"
            type="text"
            value={searchKeywords[displayedResultIndex]}
          />
          <button onClick={() => changeDisplayedResult(1)}>{"->"}</button>
        </div>
        <div class="selectionScreenComponent" >
          <SearchResultDisplay 
            keyword={searchKeywords[displayedResultIndex]}
            searchResult={searchResults[searchKeywords[displayedResultIndex]]}
            displayedWordIndex={displayedWordIndex}
            displayedTermIndex={displayedTermIndex}
            selectedTerms={selectedTerms[searchKeywords[displayedResultIndex]]}
            setDisplayedWordIndex={setDisplayedWordIndex}
            setDisplayedTermIndex={setDisplayedTermIndex} 
            setSelectedTerms={setSelectedTerms}
          />
        </div>
        <div class="selectionScreenComponent" >
          <button onClick={generateCards}>
            Generate Cards
          </button>
        </div>
      </div>
    )

}