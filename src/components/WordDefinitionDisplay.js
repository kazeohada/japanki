import React, { Component } from "react";
import "./style.css";

export default function WordDefinitionDisplay(props) {
    console.log(props.word)
    console.log(props.selectedTerms)
    var displayedTerm = 0
    var terms = new Set()

    const japaneseTermText = (term, i) => {
        if (terms.has(props.word.Terms[i].Japanese )) {
            return
        }
        terms.add(props.word.Terms[i].Japanese)
        
        return (<span className={i === displayedTerm ? "bigTerm" : "smallTerm"}>{props.word.Terms[i].Japanese}</span>)
    }

    return (
        <div class="wordDefinitionBox">
            {props.word.Terms.map((term, index) => (
                japaneseTermText(term, index)
            ))}
            
        </div>
    )
}