import React, { Component, useState } from "react";

import "./style.css";

export default function TermKanjiDefinition(props) {
 
    return (
        <div>
            <div lang="ja">{props.kanji.Kanji}</div>
            <div>Kunyomi: <span lang="ja">{props.kanji.Kunyomi.map(kunyomi => kunyomi.Ending != "" ? (kunyomi.Kunyomi + "." + kunyomi.Ending) : kunyomi.Kunyomi).join("、")}</span></div>
            <div>Onyomi: <span lang="ja">{props.kanji.Onyomi.map(onyomi => onyomi.Onyomi).join("、")}</span></div>
        </div>
    )
}