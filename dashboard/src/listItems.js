import * as React from 'react';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import DashboardIcon from '@material-ui/icons/Dashboard';
import BubbleChart from '@material-ui/icons/BubbleChart';
import Storage from '@material-ui/icons/Storage'

export const mainListItems = (
  <div>
    <ListItem button>
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
      <ListItemText primary="Database Importer"/>
    </ListItem>
  </div>
);

