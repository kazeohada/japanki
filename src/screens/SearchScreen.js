import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import SearchKeywordButton from "../components/SearchKeywordButton";
import { eel } from "../eel.js";

export default function SearchScreen(props) {
  const [searchKeywords, setSearchKeywords] = useState(props.searchKeywords);
  const [searchResults, setSearchResults] = useState(props.searchResults);
  const navigate = useNavigate();

  // equivalent to constructor
  React.useEffect(() => {
    eel.hello_eel();
  }, []); // empty dependency array ensures this runs once when the component mounts

  const addSearchKey = (event) => {
    if (event.key === "Enter") {
      const word = event.target.value.trim();
      if (word) {
        setSearchKeywords((prevSearchKeywords) => [...prevSearchKeywords, word]);
        event.target.value = "";
      }
    }
  };

  const removeSearchKey = (index) => {
    console.log("test");
    setSearchKeywords((prevSearchKeywords) =>
        prevSearchKeywords.filter((_, i) => i !== index)
    );
  };

  const submitSearchKeywords = () => {
    console.log("submit");
    if (searchKeywords.length > 0) {
        eel.search_keywords(searchKeywords)((results) => {
          setSearchResults(results);
          props.setParentSearchResults(results)
          navigate("/selection");
        });
    }
  };

  return (
    <div>
      <input
        className="searchBar"
        type="text"
        placeholder="Search for words"
        onKeyDown={addSearchKey}
      />
      {searchKeywords.map((keyword, index) => (
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
