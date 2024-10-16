import React, { Component, useState } from "react";

import TermKanjiDefinition from "./TermKanjiDefinition";

import { eel } from "../eel.js";

import "./style.css";

export default function WordDefinitionDisplay(props) {
    console.log("WordDefinitionDisplay")
    console.log(props)
    
    var terms = new Set()
    var displayedTerm = props.word.Terms[props.displayedTermIndex]
    var selectedTermIDs = props.selectedTerms.map(term => term.Term_ID)
    var isSelected = selectedTermIDs.includes(displayedTerm.Term_ID)


    const japaneseTermText = (term, i) => {
        if (terms.has(term.Japanese)) {
            return (<></>)
        }
        terms.add(term.Japanese)
        
        return (
            <span lang="ja" 
                className={
                    (term.Japanese == displayedTerm.Japanese ? "bigTerm" : "smallTerm")
                    + " " +
                    (selectedTermIDs.includes(term.Term_ID) ? "selectedTerm" : "")
                } 
                onClick={() => {props.setDisplayedTermIndex(i)}}
            >
                {term.Japanese}
            </span>
        )
    }

    const readingTermText = (term, i) => {
        if (term.Japanese != displayedTerm.Japanese){
            return (<></>)
        }

        return (
            <span lang="ja" 
                className={
                    (i === props.displayedTermIndex ? "bigTerm" : "smallTerm")
                    + " " +
                    (selectedTermIDs.includes(term.Term_ID) ? "selectedTerm" : "")
                } 
                onClick={() => {props.setDisplayedTermIndex(i)}}
            >
                {term.Reading}
            </span>
        )
    }

    const toggleSelection = () => {
        if (isSelected) {
            // remove from list
            eel.remove_selected(displayedTerm, props.keyword)((newSelected) => props.setSelectedTerms(newSelected))
        } else {
            // add to list
            eel.add_selected(displayedTerm, props.keyword)((newSelected) => props.setSelectedTerms(newSelected))
        }
    }

    return (
        <div class="searchResultDisplayComponent">
            <div class="wordDefinitionBox japaneseBox">
                <div> 
                    {props.word.Terms.map((term, index) => (
                        japaneseTermText(term, index)
                    ))}
                </div>
                <div> 
                    {props.word.Terms.map((term, index) => (
                        readingTermText(term, index)
                    ))}
                </div>
            </div>
            <hr class="wordDefinitionHr"/>
            <div class ="wordDefinitionBox definitionBox">
                <div class="wordDefinitionBoxTitle">Definitions:</div>
                <div class="wordDefinitionBoxContent">
                    <ol>
                    {displayedTerm.Meanings.map((meaning, index) => (
                        <li>{meaning.Definitions.join(", ")}</li>
                    ))}
                    </ol>
                </div>
            </div>
            <hr class="wordDefinitionHr"/>
            <div class="wordDefinitionBox kanjiBox">
                <div class="wordDefinitionBoxTitle">
                    Kanji:
                </div>
                <div class="wordDefinitionBoxContent">
                    {displayedTerm.Kanji.map((kanji, index) => (
                        <TermKanjiDefinition kanji={kanji} />
                    ))}
                </div>
            </div>
            <hr class="wordDefinitionHr"/>
            <div class="wordDefinitonBox">
                <div class="wordDefinitionBoxContent">
                    <button onClick={toggleSelection}>
                        {isSelected ? "Unselect" : "Select"}
                    </button>
                </div>
            </div>
            
        </div>
    )
}