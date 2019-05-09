import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import Paper from '@material-ui/core/Paper'
import SearchForm from './SearchComponent'
import { connect } from 'react-redux'
import { search_exit } from '../redux/actions'

const styles = theme => ({
    paper: {
        display:'flex',
        alignItems:'center',
        },
    container: {
        display: "flex",
        flexGrow: 1,
        width: '80%',
        margin:'1em'
        },
    });

const SearchDrawer = ({ open, classes}) => (
    <Drawer classes={classes} anchor="top" elevation ={2} open={open} >
        <div className={classes.container}>
            <SearchForm/>
        </div>
    </Drawer>
    );

export default connect((state) => ({open:state.search_open}))(withStyles(styles)(SearchDrawer));