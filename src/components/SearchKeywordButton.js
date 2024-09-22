import React, { Component } from "react";
import "./style.css";

export default function searchKeywordButton(props) {
    return (
        <div className="keywordButton" onClick={props.onClick}>
            {props.keyword}
        </div>
    )
}
