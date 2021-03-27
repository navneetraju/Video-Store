import React from 'react';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/styles';
import PropTypes from 'prop-types';

const styles = theme =>({
  root: {
    minWidth: 275,
  },
  bullet: {
    display: 'inline-block',
    margin: '0 2px',
    transform: 'scale(0.8)',
  },
  title: {
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
});

class ErrorCard extends React.Component{
	render(){
		const { classes } = this.props;
		var code = this.props.code;
		var error = this.props.error;
		console.log("ERROR TYPE",error);
		if(error!=null){
			return(
				<Card className={classes.root} variant="outlined" style={{backgroundColor: "#ff5252"}}>
				<CardContent>
				  <Typography variant="h5" component="h2">
					{"Unable to call metadata store system!"}
				  </Typography>
				  <Typography variant="body2" component="p">
					  Error Message: {error.message}
					<br />
				  </Typography>
				</CardContent>
			  </Card>
			)
		}
		if(code === 400){
			return (
				<Card className={classes.root} variant="outlined" style={{backgroundColor: "#ffc400"}}>
				  <CardContent>
					<Typography variant="h5" component="h2">
					  {"Bad query, please check below message for details !"}
					</Typography>
					<Typography variant="body2" component="p">
						{this.props.message}
					  <br />
					</Typography>
				  </CardContent>
				</Card>
			  );
		}
		else{
			return (
				<Card className={classes.root} variant="outlined" style={{backgroundColor: "#f44336"}}>
				  <CardContent>
					<Typography variant="h5" component="h2">
					  {"Internal server error, please try again later"}
					</Typography>
					<Typography variant="body2" component="p">
						{this.props.message}
					  <br />
					</Typography>
				  </CardContent>
				</Card>
			  );
		}

	}
}

ErrorCard.propTypes = {
	classes: PropTypes.object.isRequired,
  };

export default withStyles(styles)(ErrorCard);