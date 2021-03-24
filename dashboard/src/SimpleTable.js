import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import Typography from '@material-ui/core/Typography';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

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
	}
	
	render(){
		var classes = PropTypes.object.isRequired;
		var response = this.props.response;
		if(response != null){
			console.log(response.status);
			console.log(typeof response);
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
					  <StyledTableCell>Fuzzy Match Score</StyledTableCell>
          			</TableRow>
					{response.responseList.map(n => (
					  <TableRow key={n.id}>
					  <TableCell>{n.video_id}</TableCell>
					  <TableCell><a href={n.video_url}>{n.video_url}</a></TableCell>
					  <TableCell>{n.video_location}</TableCell>
					  <TableCell>{n.start_frame}</TableCell>
					  <TableCell>{n.end_frame}</TableCell>
					  <TableCell>{n.score}</TableCell>
					</TableRow>
					))}
				  </TableBody>
				</Table>
			  </Paper>
			)
		}
		return(
			<Paper className={classes.root} id="resultsPaper">
		  </Paper>
		)
	}
}


export default withStyles(styles)(SimpleTable);