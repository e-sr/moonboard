import React,{useState,useEffect} from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { connect } from 'react-redux'
import MaterialTable from "material-table";
import  {Done} from '@material-ui/icons';
import {set_selected_problem} from '../redux/actions';


const styles = theme => ({
    root: {
        width: '100%',
        marginTop: theme.spacing.unit * 3,
    },
    table: {
        minWidth: 1020,
    },
    tableWrapper: {
        overflowX: 'auto',
    },
});

const Benchmark= (props) =>{
    if (props.benchmark) {
        return <Done/>;
    } else {
        return "No";    
    }
};


const ProblemTable_ = ({data, dispatch}) =>{
    const [selected, setSelected] = useState(null);
    useEffect(() => {dispatch(set_selected_problem(selected))});
    return (
    <div >
    <MaterialTable
    data={data}
    columns = {[
        {title: "Nome",render: rowData => rowData[1]},
        {title: "Grado",render: rowData => rowData[2]},
        {title: "Setter",render: rowData => rowData[3]},
        {title:"Benchmark" ,render: rowData => <Benchmark benchmark={rowData[4]}/> },
    ]}
    options={{
        //filterType: 'checkbox',
        pageSize: 5,
        filtering: false,
        search: false,
        sorting:true,
        toolbar:false,
        rowStyle: rowData => ({
            backgroundColor: (selected && selected.tableData.id === rowData.tableData.id) ? '#EEE' : '#FFF'
        }),
    }}
    onRowClick={(evt, selectedRow)  => {setSelected(selectedRow)}}
    onChangePage={(evt,)  => {setSelected(null)}}
    />
</div>)
};


const ProblemTable = connect(
    (state) => ({ data: state.problems }), 
    null
    )(withStyles(styles)(ProblemTable_));

ProblemTable.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(ProblemTable);


