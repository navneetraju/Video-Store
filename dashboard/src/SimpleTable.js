import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import ErrorCard from './Cards/ErrorCard';
import LinearProgress from '@material-ui/core/LinearProgress';
import Button from '@material-ui/core/Button';

const StyledTableCell = withStyles((theme) => ({
	head: {
	  backgroundColor: theme.palette.common.black,
	  color: theme.palette.common.white,
	},
	body: {
	  fontSize: 14,
	},
  }))(TableCell);

const styles = {
  root: {
    width: '100%',
    overflowX: 'auto',
  },
  table: {
    minWidth: 700,
  },
};

class SimpleTable extends React.Component{

		constructor(props){
			super(props);
			this.onClickHandler = this.onClickHandler.bind(this);
		}
		onClickHandler(videoid,start,end){
			this.props.videoHandler(videoid,start,end);
			console.log(videoid,start,end);
		}	
	render(){

		if(this.props.isLoading){
			return(
				<LinearProgress />
			)
		}
		var classes = PropTypes.object.isRequired;
		var response = this.props.response;
		var isRec = this.props.isRec;





		console.log("SIMPLE TABLE: ",this.props.error);
		if(this.props.error!=null){
			return(<ErrorCard error={this.props.error}/>);
		}
		console.log(response)
		if(response != null){


				if(isRec){
		
					console.log('Isrec',response[0].videos);
					return(
						<Paper className={classes.root} id="resultsPaper">
						<Table className={classes.table}>
						  <TableBody>
							  <TableRow>
							  <StyledTableCell>Video ID</StyledTableCell>
							  <StyledTableCell>Video URL</StyledTableCell>
							  <StyledTableCell>Video Location</StyledTableCell>
							  <StyledTableCell>Video Start Frame</StyledTableCell>
							  <StyledTableCell>Video End Frame</StyledTableCell>
							  </TableRow>
							{response[0].videos.map(n => (
							  <TableRow key={n.video_id}>
								<TableCell><Button onClick={()=>this.onClickHandler(n.video_id,n.start_frame,n.end_frame)}>{n.video_id}</Button></TableCell>
							  <TableCell><a href={"https://www.youtube.com/watch?v="+n.video_id} target="_blank"  rel="noreferrer">{"https://www.youtube.com/watch?v="+n.video_id}</a></TableCell>
							  <TableCell>Youtube</TableCell>
							  <TableCell>{n.start_frame}</TableCell>
							  <TableCell>{n.end_frame}</TableCell>
							</TableRow>
							))}
						  </TableBody>
						</Table>
					  </Paper>
					)
				}
			if(response.code === 200){
				var isFuzzy = this.props.isFuzzy;

				console.log(this.props.isFuzzy);
				if(isFuzzy){
					return(
						<Paper className={classes.root} id="resultsPaper">
						<Table className={classes.table}>
						  <TableBody>
							  <TableRow>
							  <StyledTableCell>Video ID</StyledTableCell>
							  <StyledTableCell>Video URL</StyledTableCell>
							  <StyledTableCell>Video Location</StyledTableCell>
							  <StyledTableCell>Video Start Frame</StyledTableCell>
							  <StyledTableCell>Video End Frame</StyledTableCell>
							  <StyledTableCell>Fuzzy Matched Score</StyledTableCell>
							  <StyledTableCell>Matched Tags</StyledTableCell>
							  </TableRow>
							{response.response.responseList.map(n => (
							  <TableRow key={n.id}>
							  <TableCell><Button onClick={()=>this.onClickHandler(n.video_id,n.start_frame,n.end_frame)}>{n.video_id}</Button></TableCell>
							  <TableCell><a href={n.video_url} target="_blank" rel="noreferrer">{n.video_url}</a></TableCell>
							  <TableCell>{n.video_location}</TableCell>
							  <TableCell>{n.start_frame}</TableCell>
							  <TableCell>{n.end_frame}</TableCell>
							  <TableCell>{Math.round(n.score * 1000) / 1000}</TableCell>
							  <TableCell>{n.tags.toString()}</TableCell>
							</TableRow>
							))}
						  </TableBody>
						</Table>
					  </Paper>
					)
				}
				else{
					return(
						<Paper className={classes.root} id="resultsPaper">
						<Table className={classes.table}>
						  <TableBody>
							  <TableRow>
							  <StyledTableCell>Video ID</StyledTableCell>
							  <StyledTableCell>Video URL</StyledTableCell>
							  <StyledTableCell>Video Location</StyledTableCell>
							  <StyledTableCell>Video Start Frame</StyledTableCell>
							  <StyledTableCell>Video End Frame</StyledTableCell>
							  </TableRow>
							{response.response.responseList.map(n => (
							  <TableRow key={n.id}>
								  <TableCell><Button onClick={()=>this.onClickHandler(n.video_id,n.start_frame,n.end_frame)}>{n.video_id}</Button></TableCell>
							  <TableCell><a href={n.video_url} target="_blank"  rel="noreferrer">{n.video_url}</a></TableCell>
							  <TableCell>{n.video_location}</TableCell>
							  <TableCell>{n.start_frame}</TableCell>
							  <TableCell>{n.end_frame}</TableCell>
							</TableRow>
							))}
						  </TableBody>
						</Table>
					  </Paper>
					)
				}


			}
			else if(response.code === 400){
				return(
					<ErrorCard message={response.message} code={response.code}/>
				);
			}
		}
		return(
			<Paper className={classes.root} id="resultsPaper">
		  </Paper>
		)
	}
}


export default withStyles(styles)(SimpleTable);