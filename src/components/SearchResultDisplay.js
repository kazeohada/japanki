import React, { Component, useState } from "react";

import SearchResultListItem from "./SearchResultListItem";
import WordDefinitionDisplay from "./WordDefinitionDisplay";

export default function SearchResultDisplay(props) {
    console.log("SearchResultDisplay")
    console.log(props)

    return (
        <div style={{ display: "flex", justifyContent: "center" }}>
            <div style={{flex: "1"}}>
                {props.searchResult.map((word, index) => (
                    <SearchResultListItem 
                        keyword={props.keyword}
                        word={word}
                        selectedTerms={props.selectedTerms}
                        index={index}
                        setDisplayedWord={props.setDisplayedWord}
                        setDisplayedTermIndex={props.setDisplayedTermIndex}
                    />
                ))}
            </div>
            <WordDefinitionDisplay 
                keyword={props.keyword}
                word={props.searchResult[props.displayedWord]}
                selectedTerms={props.selectedTerms}
                setSelectedTerms={props.setSelectedTerms}
                displayedTermIndex={props.displayedTermIndex}
                setDisplayedTermIndex={props.setDisplayedTermIndex}
            />
        </div>
    )
}