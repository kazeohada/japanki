import React, { Component, useState } from "react";

import TermKanjiDefinition from "./TermKanjiDefinition";

import "./style.css";

export default function WordDefinitionDisplay(props) {
    console.log("WordDefinitionDisplay")
    console.log(props)
    
    var terms = new Set()
    var displayedTerm = props.displayedTerm
    var selectedTermIDs = props.selectedTerms.map(term => term.Term_ID)


    const japaneseTermText = (term, i) => {
        if (terms.has(term.Japanese)) {
            return (<></>)
        }
        terms.add(term.Japanese)
        
        return (
            <span lang="ja" 
                className={
                    (term.Japanese == props.word.Terms[displayedTerm].Japanese ? "bigTerm" : "smallTerm")
                    + " " +
                    (selectedTermIDs.includes(term.Term_ID) ? "selectedTerm" : "")
                } 
                onClick={() => {props.setDisplayedTerm(i)}}
            >
                {term.Japanese}
            </span>
        )
    }

    const readingTermText = (term, i) => {
        if (term.Japanese != props.word.Terms[displayedTerm].Japanese){
            return (<></>)
        }

        return (
            <span lang="ja" 
                className={
                    (i === displayedTerm ? "bigTerm" : "smallTerm")
                    + " " +
                    (selectedTermIDs.includes(term.Term_ID) ? "selectedTerm" : "")
                } 
                onClick={() => {props.setDisplayedTerm(i)}}
            >
                {term.Reading}
            </span>
        )
    }

    return (
        <div class="wordDefinitionBox">
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
            <div>Definitions:</div>
            <div>
                <ol>
                {props.word.Terms[displayedTerm].Meanings.map((meaning, index) => (
                    <li>{meaning.Definitions.join(", ")}</li>
                ))}
                </ol>
            </div>
            <div>
                Kanji:
            </div>
            <div>
                {props.word.Terms[displayedTerm].Kanji.map((kanji, index) => (
                    <TermKanjiDefinition kanji={kanji} />
                ))}
            </div>
            
        </div>
    )
}