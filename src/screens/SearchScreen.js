import React, { Component } from "react";

import SearchKeywordButton from "../components/SearchKeywordButton";

export default class SearchScreen extends Component {
    constructor(props) {
        super(props);
        this.state = {
          searchKeywords: []
        };
    }


    addSearchKey = (event) => {
        if (event.key == "Enter"){
            const word = event.target.value.trim();
            if (word) {
              this.setState((prevState) => ({
                searchKeywords: [...prevState.searchKeywords, word],
              }));
              event.target.value = "";
            }
        }
    }

    removeSearchKey = (index) => {
        console.log("test")
        var keywords = this.state.searchKeywords
        keywords.splice(index, 1)
        this.setState(() => ({
          searchKeywords: keywords
        }));
    }

    render(){
        return (
            <div>
                <input id="searchBar" type="text" placeholder="Search for words" onKeyDown={this.addSearchKey}/>
                { this.state.searchKeywords.map((keyword, index) => (
                    <SearchKeywordButton 
                        index = {index} 
                        keyword = {keyword}
                        onClick = {() => this.removeSearchKey(index)}
                    />
                    ))
                }
            </div>
        )
    }

}