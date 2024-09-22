import React, { Component, useState } from "react";

import SearchResultListItem from "./SearchResultListItem";
import WordDefinitionDisplay from "./WordDefinitionDisplay";

export default function SearchResultDisplay(props) {
    console.log(props.searchResult)

    const [selectedWord, setSelectedWord] = useState(0);

    return (
        <div style={{ display: "flex", justifyContent: "center" }}>
            <div style={{flex: "1"}}>
                {props.searchResult.result.map((word, index) => (
                    <SearchResultListItem 
                        word={word} 
                        index={index}
                        setParentSelectedWord={setSelectedWord}
                    />
                ))}
            </div>
            <WordDefinitionDisplay 
                word={props.searchResult.result[selectedWord]}
                selectedTerms={props.searchResult.selected} 
            />
        </div>
    )
}