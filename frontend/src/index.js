import React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import { createStore, applyMiddleware,compose } from 'redux'
import rootReducer from './redux/reducers'
import reduxWebsocket from 'react-redux-websocket';
import App from './App'
import WebFont from 'webfontloader'
import './index.css'

WebFont.load({
    google: {
        families: ['Roboto:300,500,700']
    }
});
const initialState = {
    search_open: false,
    grades: [],
    holds: [],
    search_param:{
        holds:[],
        grades:[],
        name:"",
        author:""
    },
    test_selected:[],
    search_results_id: [],
    page_id_index: [],
    page_data: [],
    history: [],
};

const ws = new WebSocket('ws://moonboard:6789/')
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const store = createStore(rootReducer, 
    initialState, 
    composeEnhancers(applyMiddleware(reduxWebsocket(ws))),
    )

render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById('root')
)