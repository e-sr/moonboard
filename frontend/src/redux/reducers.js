const search_param_reducer = (search_param,action)=>{
    switch (action.type) {
        case 'SEARCH_PARAM':
            return Object.assign({}, search_param, { [action.name]: action.data });

        default:
            return search_param;
        }
    }

const rootReducer = (state , action) => {
    switch (action.type) {
        case "INIT":
            return Object.assign({}, state, {
                grades: action.grades,
                holds: action.holds,
                history: action.history,
                problems:action.problems,
                search_param:action.search_param
            })
        case 'SEARCH_RESULTS':
            return Object.assign({}, state, {
                problems: action.problems
            })
        case 'SEARCH_ENTER':
            return Object.assign({}, state, {
                search_open: true
            })
        case 'SEARCH_EXIT':
            return Object.assign({}, state, {
                search_open: false
            })
        case 'SEARCH_PARAM':
            return Object.assign({}, state, {
                search_param: search_param_reducer(state.search_param, action)
            })

        case 'SEARCH_SUBMIT':
            return Object.assign({}, state, {
                search_open: false
            })
        case 'SET_SELECTED_PROBLEM':
            return Object.assign({}, state, {
                selected_problem: action.problem
            })
        case 'HISTORY':
            return Object.assign({}, state, {
                history: action.history
            })
            
        default:
            return state
    }
}

export default rootReducer;
