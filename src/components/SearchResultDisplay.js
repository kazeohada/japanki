import React, { Component, useState } from "react";

import SearchResultListItem from "./SearchResultListItem";
import WordDefinitionDisplay from "./WordDefinitionDisplay";

export default function SearchResultDisplay(props) {
    console.log(props.searchResult)


    return (
        <div style={{ display: "flex", justifyContent: "center" }}>
            <div style={{flex: "1"}}>
                {props.searchResult.result.map((word, index) => (
                    <SearchResultListItem 
                        word={word} 
                        index={index}
                        setDisplayedWord={props.setDisplayedWord}
                        setDisplayedTerm={props.setDisplayedTerm}
                    />
                ))}
            </div>
            <WordDefinitionDisplay 
                word={props.searchResult.result[props.displayedWord]}
                selectedTerms={props.searchResult.selected}
                displayedTerm={props.displayedTerm}
                setDisplayedTerm={props.setDisplayedTerm}
            />
        </div>
    )
}