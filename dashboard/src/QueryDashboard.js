import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Drawer from '@material-ui/core/Drawer';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import SimpleTable from './SimpleTable';
import Grid from '@material-ui/core/Grid';
import QueryEditor from './QueryEditor';
import SimpleQuery from './SimpleQuery';
import FuzzyQuery from './FuzzyQuery';
import YoutubeEmbed from './YoutubeEmbed';
//import Recommendations from './Recommendations';
//import RecommendCard from './RecommendCard';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import DashboardIcon from '@material-ui/icons/Dashboard';
import BubbleChart from '@material-ui/icons/BubbleChart';
import Storage from '@material-ui/icons/Storage';
import {createEditor }from "./index";

const drawerWidth = 240;

const styles = theme => ({
  root: {
    display: 'flex',
  },
  toolbar: {
    paddingRight: 24, // keep right padding when drawer closed
  },
  toolbarIcon: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 8px',
    ...theme.mixins.toolbar,
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    marginLeft: 12,
    marginRight: 36,
  },
  menuButtonHidden: {
    display: 'none',
  },
  title: {
    flexGrow: 1,
  },
  drawerPaper: {
    position: 'relative',
    whiteSpace: 'nowrap',
    width: drawerWidth,
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  drawerPaperClose: {
    overflowX: 'hidden',
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    width: theme.spacing.unit * 7,
    [theme.breakpoints.up('sm')]: {
      width: theme.spacing.unit * 9,
    },
  },
  appBarSpacer: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    padding: theme.spacing.unit * 3,
    height: '100vh',
    overflow: 'auto',
  },
  chartContainer: {
    marginLeft: -22,
  },
  tableContainer: {
    height: 320,
  },
  h5: {
    marginBottom: theme.spacing.unit * 2,
  },
});
function reloadPage() {
	console.log(document.getElementById("queryEditorDivision"));
   //this line is to watch the result in console , you can remove it later
   createEditor();	
    console.log("Refreshed"); 
}
class QueryDashboard extends React.Component {

  state = {
    open: false,
    response: null,
    error: null,
    loading: false,
    isFuzzy: false,
    videoid: null,
    start_frame: null,
    end_frame: null,
  };

  constructor(props) {
    super(props);
    this.handler = this.handler.bind(this);
    this.changePage = this.changePage.bind(this);
    this.loadingHandler = this.loadingHandler.bind(this);
    this.videoHandler = this.videoHandler.bind(this);
  }

  componentDidMount() {
    reloadPage();
  }

  changePage(something, event) {
    this.props.pageHandler(something);
  }

  handler(resp, err, isFuzzyB) {
    console.log('Response,err ', resp, err);
    this.setState({response: resp, error: err, isFuzzy: isFuzzyB});
  }

  loadingHandler(loadingBool) {
    this.setState({loading: loadingBool})
  }

  async videoHandler(id, start, end) {
    //this.setState({videoid: videoid, start_frame: start_frame, end_frame: end_frame});
    //this.props.recommendations(videoid, start_frame, end_frame);
    this.setState({videoid: id})
    var db_name = 'testing';
    const requestOptions = {
      method: 'GET',
      headers: {'Content-Type': 'application/json'},
      //body: JSON.stringify(requestBody)
    }
    //console.log(id);
    //console.log('start');
    const res = await fetch('http://127.0.0.1:8000/api/recommend/' + id + '/' + db_name + '/?start=' + String(start) + '&end=' + String(end), requestOptions)
    //const res = await fetch('http://10.10.1.146:8000/api/recommend/' + id + '/' + db_name + '/?start=' + String(start) + '&end=' + String(end), requestOptions)
    
    //console.log(res);
    const data = await res.json();
    this.setState({recommendationResponse: data, responseType: 'recommendationResponse'})
    console.log(this.state.recommendationResponse);

  }

  handleDrawerOpen = () => {
    this.setState({open: true});
  };

  handleDrawerClose = () => {
    this.setState({open: false});
  };

  render() {
    const {classes} = this.props;

    if (this.state.responseType === 'recommendationResponse') {
      return (
          <div className={classes.root}>
            <CssBaseline/>
            <AppBar
                position="absolute"
                className={classNames(classes.appBar, this.state.open && classes.appBarShift)}
            >
              <Toolbar disableGutters={!this.state.open} className={classes.toolbar}>
                <IconButton
                    color="inherit"
                    aria-label="Open drawer"
                    onClick={this.handleDrawerOpen}
                    className={classNames(
                        classes.menuButton,
                        this.state.open && classes.menuButtonHidden,
                    )}
                >
                  <MenuIcon/>
                </IconButton>
                <Typography
                    component="h1"
                    variant="h6"
                    color="inherit"
                    noWrap
                    className={classes.title}
                >
                  Dashboard
                </Typography>
              </Toolbar>
            </AppBar>
            <Drawer
                variant="permanent"
                classes={{
                  paper: classNames(classes.drawerPaper, !this.state.open && classes.drawerPaperClose),
                }}
                open={this.state.open}
            >
              <div className={classes.toolbarIcon}>
                <IconButton onClick={this.handleDrawerClose}>
                  <ChevronLeftIcon/>
                </IconButton>
              </div>
              <Divider/>
              <List>
                <div>
                  <ListItem button onClick={(event) => this.changePage("DASHBOARD", event)}>
                    <ListItemIcon>
                      <DashboardIcon/>
                    </ListItemIcon>
                    <ListItemText primary="Dashboard"/>
                  </ListItem>
                  <ListItem button onClick={(event) => this.changePage("GRAPH", event)}>
                    <ListItemIcon>
                      <BubbleChart/>
                    </ListItemIcon>
                    <ListItemText primary="Graph Visualizer"/>
                  </ListItem>
                  <ListItem button onClick={(event) => this.changePage("IMPORTER", event)}>
                    <ListItemIcon>
                      <Storage/>
                    </ListItemIcon>
                    <ListItemText primary="Database Importer"/>
                  </ListItem>
                </div>
              </List>
            </Drawer>
            <main className={classes.content}>
            <div className={classes.appBarSpacer}/>
              <div>
                <YoutubeEmbed videoid={this.state.videoid}/>
              </div>
              <br />
              <br />
              <Typography variant="h5" gutterBottom component="h2">
                Recommended Videos
              </Typography>
              <div className={classes.tableContainer}>

                <SimpleTable response={this.state.recommendationResponse} error={this.state.error} isLoading={this.state.loading}
                            isRec={true} isFuzzy={false} videoHandler={this.videoHandler}/>
              </div>
            </main>
          </div>
      );
    } else {
      return (
          <div className={classes.root}>
            <CssBaseline/>
            <AppBar
                position="absolute"
                className={classNames(classes.appBar, this.state.open && classes.appBarShift)}
            >
              <Toolbar disableGutters={!this.state.open} className={classes.toolbar}>
                <IconButton
                    color="inherit"
                    aria-label="Open drawer"
                    onClick={this.handleDrawerOpen}
                    className={classNames(
                        classes.menuButton,
                        this.state.open && classes.menuButtonHidden,
                    )}
                >
                  <MenuIcon/>
                </IconButton>
                <Typography
                    component="h1"
                    variant="h6"
                    color="inherit"
                    noWrap
                    className={classes.title}
                >
                  Dashboard
                </Typography>
              </Toolbar>
            </AppBar>
            <Drawer
                variant="permanent"
                classes={{
                  paper: classNames(classes.drawerPaper, !this.state.open && classes.drawerPaperClose),
                }}
                open={this.state.open}
            >
              <div className={classes.toolbarIcon}>
                <IconButton onClick={this.handleDrawerClose}>
                  <ChevronLeftIcon/>
                </IconButton>
              </div>
              <Divider/>
              <List>
                <div>
                  <ListItem button onClick={(event) => this.changePage("DASHBOARD", event)}>
                    <ListItemIcon>
                      <DashboardIcon/>
                    </ListItemIcon>
                    <ListItemText primary="Dashboard"/>
                  </ListItem>
                  <ListItem button onClick={(event) => this.changePage("GRAPH", event)}>
                    <ListItemIcon>
                      <BubbleChart/>
                    </ListItemIcon>
                    <ListItemText primary="Graph Visualizer"/>
                  </ListItem>
                  <ListItem button onClick={(event) => this.changePage("IMPORTER", event)}>
                    <ListItemIcon>
                      <Storage/>
                    </ListItemIcon>
                    <ListItemText primary="Database Importer"/>
                  </ListItem>
                </div>
              </List>
            </Drawer>
            <main className={classes.content}>
              <div className={classes.appBarSpacer}/>
              <Typography variant="h5" gutterBottom component="h2">
                Query Editor
              </Typography>
              <Grid container spacing={3}>
                <QueryEditor/>
                <Grid item xs={3}>
                  <SimpleQuery handler={this.handler} loadingHandler={this.loadingHandler}/>
                </Grid>
                <Grid item xs={3}>
                  <FuzzyQuery handler={this.handler} loadingHandler={this.loadingHandler}/>
                </Grid>
              </Grid>
              <br/>
              <br/>
              <Typography variant="h5" gutterBottom component="h2">
                Results
              </Typography>
              <div className={classes.tableContainer}>
                <SimpleTable response={this.state.response} error={this.state.error} isLoading={this.state.loading}
                             isFuzzy={this.state.isFuzzy} videoHandler={this.videoHandler}/>
              </div>
            </main>
          </div>
      );
    }
  }
}


QueryDashboard.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(QueryDashboard);