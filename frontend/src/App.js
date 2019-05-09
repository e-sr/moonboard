import React  from 'react';
import './App.css';
import MoonAppBar from './components/AppBar'
import SearchDrawer from './components/SearchDrawer'
import ProblemTable from './components/ProblemTable'



const App = ()=>{
    return (
      <React.Fragment>
        <MoonAppBar/>
        <ProblemTable/>
        <SearchDrawer/>
      </React.Fragment>
    );
  }

export default App;

