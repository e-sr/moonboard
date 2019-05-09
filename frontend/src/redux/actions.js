let nextTodoId = 0

export const  search_enter =  {
    type: 'SEARCH_ENTER',
    socket: {
        send: true
    }
}

export const  search_submit = (search_parameter) => ({
    type: 'SEARCH_SUBMIT',
    search_parameter: search_parameter,
    socket: {
        send: true
    }
})

export const search_param = (name,data) => ({
    type: 'SEARCH_PARAM',
    name: name,
    data:data,
})

export const  search_exit = {
    type: 'SEARCH_EXIT',

}

export const  search_results = {
    type: 'SEARCH_RESULTS',
}

export const view_problem = problem_id => ({
    type: 'VIEW_PROBLEM',
    problem_id
})

export const set_selected_problem = problem=> ({
    type: 'SET_SELECTED_PROBLEM',
    problem
})

export const  illuminate_problem = problem => ({
    type: 'ILLUMINATE_PROBLEM',
    problem,
    socket: {
        send: true
    }
})

export const  view = {
    type: 'VIEW_EXIT',
}


export const load_page = page => ({
    type: 'LOAD_PAGE',
    page
})
