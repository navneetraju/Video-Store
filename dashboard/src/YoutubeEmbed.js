import React from "react";
import "./App.css";
import PropTypes from "prop-types";


class YoutubeEmbed extends React.Component{
    constructor(props) {
        super(props);
    }
    
    render() {
        var embedId = this.props.videoid;
        return (
        <div classname="video-responsive">
            <iframe
            width="700"
            height="350"
            src={'https://www.youtube.com/embed/'+embedId}
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            title="Embedded youtube"
            />
            </div>
        );
    
    }

}
export default YoutubeEmbed;