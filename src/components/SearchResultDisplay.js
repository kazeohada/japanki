import React, { Component, useState } from "react";

export default function SearchResultDisplay(props) {

    return (
        <div>
            {props.searchResult.result[0].Terms[0].Japanese}
        </div>
    )
}