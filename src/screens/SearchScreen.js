import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import SearchKeywordButton from "../components/SearchKeywordButton";
import { eel } from "../eel.js";

export default function SearchScreen(props) {
  const navigate = useNavigate();

  // equivalent to constructor
  React.useEffect(() => {
    eel.hello_eel();
  }, []); // empty dependency array ensures this runs once when the component mounts

  const addSearchKey = (event) => {
    if (event.key === "Enter") {
      const word = event.target.value.trim();
      if (word) {
        props.setSearchKeywords((prevSearchKeywords) => [...prevSearchKeywords, word]);
        event.target.value = "";
      }
    }
  };

  const removeSearchKey = (index) => {
    props.setSearchKeywords((prevSearchKeywords) =>
        prevSearchKeywords.filter((_, i) => i !== index)
    );
  };

  const submitSearchKeywords = () => {
    if (props.searchKeywords.length > 0) {
        eel.search_keywords(props.searchKeywords)((results) => {
          props.setSearchResults(results);
          var userContinues = true;
          console.log(results)
          console.log(props.searchKeywords.some((keyword) => results[keyword].length === 0 ))
          if (props.searchKeywords.some((keyword) => results[keyword].length === 0 )) {
            console.log("oops")
            userContinues = window.confirm("Some results couldn't be found. Continue anyway?")
          }
          if (userContinues){
            navigate("/selection")
          }
        });
    }
  };

  return (
    <div  style={{padding: "2% 5%"}}>
      <input
        className="searchBar"
        type="text"
        placeholder="Search for words"
        onKeyDown={addSearchKey}
      />
      {props.searchKeywords.map((keyword, index) => (
        <SearchKeywordButton
          key={index}
          index={index}
          keyword={keyword}
          onClick={() => removeSearchKey(index)}
        />
      ))}
      <button onClick={submitSearchKeywords}>Search</button>
    </div>
  );
}
