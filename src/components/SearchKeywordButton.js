import React, { Component } from "react";
import "./style.css";

export default class searchKeywordButton extends Component {

    render(){
        return(
            <div className="keywordButton" onClick={this.props.onClick}>
                {this.props.keyword}
            </div>
        )
    }

}
