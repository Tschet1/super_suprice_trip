const INITIAL_STATE = {};

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case 'set_value':
      return { ...state, [action.payload.prop]: action.payload.value };
    default:
      return state;
  }
};
