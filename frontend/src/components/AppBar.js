import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import  WbIncandescent from '@material-ui/icons/WbIncandescent';
import  Search from '@material-ui/icons/Search';
import  Info from '@material-ui/icons/Info';
import { connect } from 'react-redux';
import {search_enter,illuminate_problem} from '../redux/actions'


const styles = {
    grow: {
        flexGrow: 1,
    },
    menuButton: {
        marginLeft: -12,
        marginRight: 20,
    },
};

let MoonAppBar_ = ({ classes, onSearch,onInfo, onIlluminate, selectedProblem })=>{
    return (
        <AppBar position="static">
            <Toolbar>
                <IconButton className={classes.menuButton} onClick={onSearch} color="inherit" aria-label="Menu">
                    <Search/>
                </IconButton>
                <Typography variant="h6" color="inherit" className={classes.grow}>
                    Moonboardapp
                </Typography>
                <IconButton className={classes.menuButton} onClick={onInfo} disabled={!selectedProblem} color="inherit" aria-label="Menu">
                    <Info />
                </IconButton>
                <IconButton className={classes.menuButton} onClick={onIlluminate(selectedProblem)} disabled={!selectedProblem} color="inherit" aria-label="Menu">
                    <WbIncandescent />
                </IconButton>
            </Toolbar>
        </AppBar>
    );
}

//MoonAppBar_.propTypes = {
//    classes: PropTypes.object.isRequired,
//    onSearchClick: PropTypes.func.isRequired,
//};
//
const MoonAppBar__ = withStyles(styles)(MoonAppBar_);


const mapDispatchToProps = (dispatch) => ({
    onSearch: () => { dispatch(search_enter); },
    onInfo: () => {dispatch(illuminate_problem)},
    onIlluminate: (problem)=>() => { dispatch(illuminate_problem(problem))},

}
)
const MoonAppBar = connect(
    (state) =>({selectedProblem:state.selected_problem}),
    mapDispatchToProps,
) (MoonAppBar__)

export default MoonAppBar;
