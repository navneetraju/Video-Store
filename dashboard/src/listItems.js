import * as React from 'react';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import DashboardIcon from '@material-ui/icons/Dashboard';
import BubbleChart from '@material-ui/icons/BubbleChart';
import Storage from '@material-ui/icons/Storage'

function dashTransitionHandler(){
	window.location.href="./Dashboard.js"
}
function dbTransitionHandler(){
	window.location.href="./DatabaseImporter.js"
}
function graphTransitionHandler(){
	window.location.href="./Dashboard.js"
}
export const mainListItems = (
  <div>
    <ListItem button onClick={dashTransitionHandler}>
      <ListItemIcon>
        <DashboardIcon />
      </ListItemIcon>
      <ListItemText primary="Dashboard"/>
    </ListItem>
    <ListItem button>
      <ListItemIcon >
        <BubbleChart />
      </ListItemIcon>
      <ListItemText primary="Graph Visualizer" />
    </ListItem>
    <ListItem button>
      <ListItemIcon>
        <Storage />
      </ListItemIcon>
      <ListItemText primary="Database Importer" onClick={dbTransitionHandler}/>
    </ListItem>
  </div>
);

export const secondaryListItems = (
  <div>
  </div>
);
