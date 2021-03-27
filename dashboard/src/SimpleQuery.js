import React from 'react';
import Button from '@material-ui/core/Button';

class SimpleQuery extends React.Component {
	constructor(props){
		super(props);
		this.onClickHandler = this.onClickHandler.bind(this);
	}
	onClickHandler(){
		this.props.loadingHandler(true);
		const requestBody = {
			'query': window.editor.getValue()
		}
		const requestOptions = {
			method: 'POST', 
			headers: {'Content-Type':'application/json'},
			body: JSON.stringify(requestBody)
		}
		console.log(window.editor.getValue());
		fetch('http://127.0.0.1:8000/api/query/?fuzzy=false', requestOptions)
		.then(response => response.json())
		.then(
			(response) => {
				this.props.loadingHandler(false);
				console.log("GOT RESPONSE");
				this.props.handler(response,null,false);
			},
			(error) => {
				this.props.loadingHandler(false);
				console.log("HANDLING ERROR");
				this.props.handler(null,error,false);
			}
		)
		//var mockResponse = JSON.parse('{"status":200,"responseList":[{"video_id":"Q-fBSX6lE-Q","video_url":"https:\/\/www.youtube.com\/watch?v=Q-fBSX6lE-Q#00m00s","video_location":"Youtube","start_frame":"10","end_frame":"20","score":1,"tags":["amusement_ride"]},{"video_id":"E65cVBcCjAs","video_url":"https:\/\/www.youtube.com\/watch?v=E65cVBcCjAs#00m00s","video_location":"Youtube","start_frame":"27","end_frame":"37","score":1,"tags":["acting"]},{"video_id":"zbhfmZGbsy4","video_url":"https:\/\/www.youtube.com\/watch?v=zbhfmZGbsy4#00m06s","video_location":"Youtube","start_frame":"206","end_frame":"216","score":1,"tags":["art"]},{"video_id":"QQrjXf4IPIk","video_url":"https:\/\/www.youtube.com\/watch?v=QQrjXf4IPIk#00m00s","video_location":"Youtube","start_frame":"2","end_frame":"12","score":1,"tags":["adventure"]}]}');
	}
	render(){
		return (
			<Button variant="contained" color="primary" fullWidth="true" onClick={this.onClickHandler}>
						Run Simple Query
			</Button>
		)
	}
}

export default SimpleQuery;