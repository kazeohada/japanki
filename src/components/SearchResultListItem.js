import React from "react";

import "./style.css";

export default function SearchResultListItem(props) {
    const maxTextLength = 75

    const japaneseText = () => {
        const textArray = []
        for (let i=0; i<props.word.Terms.length; i++){
            if (!textArray.includes(props.word.Terms[i].Japanese)){
                textArray.push(props.word.Terms[i].Japanese)
            }
            if (props.word.Terms[i].Reading != "" && !textArray.includes(props.word.Terms[i].Reading)) {
                textArray.push(props.word.Terms[i].Reading)
            }
        }
        const text = textArray.join("、")

        return text.length > maxTextLength ? `${text.slice(0, maxTextLength - 3)}...` : text
    }

    const defintionsText = () => {
        const textArray = []
        for (let i=0; i<props.word.Terms.length; i++) {
            for (let j=0; j<props.word.Terms[i].Meanings.length; j++){
                for (let k=0; k<props.word.Terms[i].Meanings[j].Definitions.length; k++){
                    if(!textArray.includes(props.word.Terms[i].Meanings[j].Definitions[k])){
                        textArray.push(props.word.Terms[i].Meanings[j].Definitions[k])
                    }
                }
            }
        }

        const text = textArray.join(", ")

        return text.length > maxTextLength ? `${text.slice(0, maxTextLength - 3)}...` : text
    }

    return (
        <div 
            lang="ja"
            class= {props.index == props.displayedWordIndex ? "listItem displayedListItem" : "listItem"}
            onClick={() => {
                props.setDisplayedWordIndex(props.index)
                props.setDisplayedTermIndex(0)
            }}
        >
            <div>{japaneseText()}</div>
            <div>{defintionsText()}</div>
        </div>
    )

}