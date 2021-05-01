import React from "react";
import "./App.css";
import PropTypes from "prop-types";


class YoutubeEmbed extends React.Component{
	state = {
		start: null
	  };
    constructor(props) {
        super(props);
		this.setState({start:this.props.start});
    }
    
    render() {
        var embedId = this.props.videoid;
		console.log('start',this.props.start);
        return (
        <div classname="video-responsive" style={{transform: 'translate(20%, 0%)'}}>
            <iframe
            width="700"
            height="350"
            src={'https://www.youtube.com/embed/'+embedId+'?start='+this.state.start}
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            title="Embedded youtube"
            />
            </div>
        );
    
    }

}
export default YoutubeEmbed;