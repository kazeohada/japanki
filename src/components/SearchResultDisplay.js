import React, { Component, useState } from "react";

import SearchResultListItem from "./SearchResultListItem";
import WordDefinitionDisplay from "./WordDefinitionDisplay";

export default function SearchResultDisplay(props) {
    console.log("SearchResultDisplay")
    console.log(props)

    return (
        <div class="searchResultBox">
            <div class="searchResultDisplayComponent" >
                {props.searchResult.map((word, index) => (
                    <SearchResultListItem 
                        keyword={props.keyword}
                        word={word}
                        selectedTerms={props.selectedTerms.filter((term) => term.Word_ID == word.Word_ID)}
                        index={index}
                        displayedWordIndex={props.displayedWordIndex}
                        setDisplayedWordIndex={props.setDisplayedWordIndex}
                        setDisplayedTermIndex={props.setDisplayedTermIndex}
                    />
                ))}
            </div>
            <WordDefinitionDisplay
                keyword={props.keyword}
                word={props.searchResult[props.displayedWordIndex]}
                selectedTerms={props.selectedTerms}
                setSelectedTerms={props.setSelectedTerms}
                displayedTermIndex={props.displayedTermIndex}
                setDisplayedTermIndex={props.setDisplayedTermIndex}
            />
        </div>
    )
}