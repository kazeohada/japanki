import React, { Component, useState } from "react";
import { useNavigate } from "react-router-dom";
import SearchResultListItem from "../components/SearchResultListItem.js";


import { eel } from "../eel.js";

export default function SelectionScreen(props) {
    const [searchKeywords, setSearchKeywords] = useState(props.searchKeywords);
    const [searchResults, setSearchResults] = useState(props.searchResults);
    const navigate = useNavigate();

    React.useEffect(() => {
      eel.hello_eel();
      console.log(searchResults)
    }, []);
    
    return (
      <div>
        <h1>Selection Screen</h1>
        {/* {
          searchResults.map((result, index) => (
          <SearchResultListItem
            index={index}
            keyword={result[0]}
            onClick={() => removeSearchKey(index)}
          />
        ))} */}
      </div>

    )

}