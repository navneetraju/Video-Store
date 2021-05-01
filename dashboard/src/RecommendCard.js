import React from 'react';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/styles';
import PropTypes from 'prop-types';
import ErrorCard from './Cards/ErrorCard';
//import classes from '*.module.css';

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



class RecommendCard extends React.Component {
    constructor(props){
      super(props);
      this.setState({recommendations: this.props.response});
    }
    render(){
        
        const { classes } = this.props;
        console.log("Recommendation: ",this.props.response);
		if(this.props.error!=null){
			return(<ErrorCard error={this.props.error}/>);
		}
        if(this.state.recommendations!=null){
            if(this.state.recommendations.code === 200){
              console.log("Recommendation Response: ",this.props.response)
                return(
                    //{recommendations.map(n =>(
                      <CardDeck>
                        <Card className={classes.root}variant="outlined" style={{backgroundColor: "#ff5252", width:'18rem'}}>
				                  <CardContent>
				                    <Typography variant="h2" component="p">
					                      Video ID : {this.state.recommendations.video_id}
				                    </Typography>
				                    <Typography variant="h2" component="p">
					                      Video URL: <a href={this.state.recommendations.video_url} target="_blank" rel="noreferrer">{this.state.recommendations.video_url}</a>
				                    </Typography>
                            <Typography variant="h2" component="p">
                                Video Start Frame: {this.state.recommendations.start_frame}
                            </Typography>
                            <Typography variant="h2" component="p">
                                Video End Frame: {this.state.recommendations.end_frame}
                            </Typography>
				                  </CardContent>
			                  </Card>
                      </CardDeck>
                    //))
                  //}
                );
            }
        }
    }
}
export default RecommendCard;