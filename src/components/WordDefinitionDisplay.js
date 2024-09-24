import React, { Component, useState } from "react";

import TermKanjiDefinition from "./TermKanjiDefinition";

import "./style.css";

export default function WordDefinitionDisplay(props) {
    const [displayedTerm, setDisplayedTerm] = useState(0);
    var terms = new Set()
    console.log(displayedTerm)
    console.log(props.word.Terms[displayedTerm].Meanings)

    const japaneseTermText = (term, i) => {
        if (terms.has(term.Japanese)) {
            return (<></>)
        }
        terms.add(term.Japanese)
        
        return (<span lang="ja" className={term.Japanese == props.word.Terms[displayedTerm].Japanese ? "bigTerm" : "smallTerm"} onClick={() => {setDisplayedTerm(i)}}>{term.Japanese}</span>)
    }

    const readingTermText = (term, i) => {
        if (term.Japanese != props.word.Terms[displayedTerm].Japanese){
            return (<></>)
        }

        return (<span lang="ja" className={i === displayedTerm ? "bigTerm" : "smallTerm"} onClick={() => {setDisplayedTerm(i)}}>{term.Reading}</span>)
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