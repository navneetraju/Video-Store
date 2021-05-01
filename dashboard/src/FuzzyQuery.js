import React from 'react';
import Button from '@material-ui/core/Button';

class FuzzyQuery extends React.Component {
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
		fetch('http://10.10.1.146:8000/api/query/?fuzzy=true', requestOptions)
		.then(response => response.json())
		.then(
			(response) => {
				this.props.loadingHandler(false);
				console.log("GOT RESPONSE");
				this.props.handler(response,null,true);
			},
			(error) => {
				this.props.loadingHandler(false);
				console.log("HANDLING ERROR");
				this.props.handler(null,error,true);
			}
		)
	}
	render(){
		return (
			<Button variant="contained" color="secondary" fullWidth="true" onClick={this.onClickHandler}>
						Run Fuzzy Query
			</Button>
		)
	}
}

export default FuzzyQuery;