import React, { Component, useState } from "react";

import "./style.css";

export default function TermKanjiDefinition(props) {

    var kanji = props.kanji
    console.log(kanji)
 
    return (
        <div class="termKanjiListItem">
            <div class="termKanji" lang="ja">{kanji.Kanji}</div>
            <div class="termKanjiYomi">Kunyomi: <span lang="ja">{kanji.Kunyomi.map(kunyomi => kunyomi.Ending != "" ? (kunyomi.Kunyomi + "." + kunyomi.Ending) : kunyomi.Kunyomi).join("、")}</span></div>
            <div class="termKanjiYomi">Onyomi: <span lang="ja">{kanji.Onyomi.map(onyomi => onyomi.Onyomi).join("、")}</span></div>
            <div class="termKanjiDefinitions">{kanji.Definitions.join(", ")}</div>
        </div>
    )
}