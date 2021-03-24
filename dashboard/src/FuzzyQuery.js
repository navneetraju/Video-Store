import React from 'react';
import Button from '@material-ui/core/Button';

class FuzzyQuery extends React.Component {
	onClickHandler(){
		console.log(window.editor.getValue());
	}
	render(){
		return (
			<Button variant="contained" color="secondary" fullWidth="true" onClick={this.props.handler}>
						Run Fuzzy Query
			</Button>
		)
	}
}

export default FuzzyQuery;