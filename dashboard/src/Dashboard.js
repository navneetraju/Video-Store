import React from 'react';
import QueryDashboard from './QueryDashboard';
import GraphVisualizer from './GraphVisualizer';
import DataImporter from './DataImporter';
//import YoutubeEmbed from './YoutubeEmbed';
//import Recommendations from './Recommendations';


class Dashboard extends React.Component {
	state = {
		open: false,
		response: null,
		page: 'DASHBOARD',
	  };
	
	constructor(props){
		super(props);
		this.handler = this.handler.bind(this);
		this.pageHandler = this.pageHandler.bind(this);
		
	}

	
	handler(resp) {
		console.log(resp);
		this.setState({ response: resp });
	}

	pageHandler(nextpage) {
		this.setState({page: nextpage});
	}
	

  handleDrawerOpen = () => {
    this.setState({ open: true });
  };

  handleDrawerClose = () => {
    this.setState({ open: false });
  };

  render() {
	console.log(this.state.page);	
	var nextPage  = this.state.page;
	if(nextPage === "DASHBOARD"){
		//window.location.reload();
		return(<QueryDashboard pageHandler = {this.pageHandler}/>);
	}
	else if(nextPage === "GRAPH"){
		return(<GraphVisualizer pageHandler = {this.pageHandler}/>);
	}
	else {
		return(<DataImporter pageHandler = {this.pageHandler}/>)
	}
	
  }
}


export default Dashboard;